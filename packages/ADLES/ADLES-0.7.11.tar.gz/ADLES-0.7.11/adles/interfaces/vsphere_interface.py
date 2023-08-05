# -*- coding: utf-8 -*-

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging
from sys import exit

import adles.vsphere.folder_utils as futils
import adles.vsphere.vm_utils as vm_utils
import adles.vsphere.vsphere_utils as vutils
from adles.utils import pad
from adles.vsphere import Vsphere
from adles.vsphere.network_utils import create_portgroup, get_net_obj


class VsphereInterface:
    """ Generic interface for the VMware vSphere platform """

    __version__ = "0.7.2"

    # Names/prefixes
    master_prefix = "(MASTER) "
    master_root_name = "MASTER_FOLDERS"

    # Values at which to warn or error when exceeded
    # TODO: make these per-instance and configurable in spec?
    thresholds = {
        "folder": {
            "warn": 25,
            "error": 50},
        "service": {
            "warn": 50,
            "error": 70}
    }

    def __init__(self, infrastructure, logins, spec):
        """
        NOTE: it is assumed that the infrastructure and spec are both valid,
        and thus checks on key existence and types are not performed for REQUIRED elements.
        :param infrastructure: Dict of infrastructure information
        :param logins: Dict of infrastructure logins
        :param spec: Dict of a parsed specification
        """
        logging.debug("Initializing VsphereInterface %s", VsphereInterface.__version__)
        self.spec = spec
        self.metadata = spec["metadata"]
        self.services = spec["services"]
        self.networks = spec["networks"]
        self.folders = spec["folders"]
        self.infra = infrastructure

        self.master_folder = None
        self.template_folder = None
        self.net_table = {}  # Used to do lookups of Base/Generic networks during deployment
        self.vlan_tag_tracker = 2000  # Tracker to ensure networks get unique VLAN tags

        # Instantiate the vSphere vCenter server instance class
        self.server = Vsphere(datacenter=infrastructure["datacenter"],
                              username=logins["user"],
                              password=logins["pass"],
                              hostname=logins["host"],
                              port=int(logins["port"]),
                              datastore=infrastructure["datastore"])

        # TODO: expand on this + put in infrastructure spec
        self.host = self.server.get_host()

        # Instantiate and initialize Groups
        self.groups = self._init_groups()

        # Set the server root folder
        if "server-root" in infrastructure:
            self.server_root = self.server.get_folder(infrastructure["server-root"])
            if not self.server_root:
                logging.error("Could not find server-root folder '%s'",
                              infrastructure["server-root"])
                exit(1)
        else:
            self.server_root = self.server.datacenter.vmFolder  # Default to Datacenter VM folder
        logging.info("Server root folder: %s", self.server_root.name)

        # Set environment root folder
        if "folder-name" not in self.metadata:
            self.root_name = self.metadata["name"]
            self.root_path = ""
            self.root_folder = futils.traverse_path(self.server_root, self.root_name)
        else:
            from os.path import split
            self.root_path, self.root_name = split(self.metadata["folder-name"])
            self.root_folder = futils.traverse_path(self.server_root, self.metadata["folder-name"])
        logging.debug("Environment root folder name: %s", self.root_name)
        if not self.root_folder:  # Create if it's not found
            parent = futils.traverse_path(self.server_root, self.root_path)
            self.root_folder = self.server.create_folder(self.root_name, parent)
        logging.info("Environment root folder: %s", self.root_folder.name)

        # Set default vSwitch name
        if "vswitch" in infrastructure:
            self.vswitch_name = infrastructure["vswitch"]
        else:  # TODO: is this a good default?
            from pyVmomi import vim
            self.vswitch_name = self.server.get_item(vim.Network).name

        logging.debug("Finished initializing VsphereInterface")

    def _init_groups(self):
        """
        Instantiate and initialize Groups
        :return: Dict of Groups
        """
        from adles.group import Group, get_ad_groups
        groups = {}

        # Instantiate Groups
        for name, config in self.spec["groups"].items():
            if "instances" in config:  # Template groups
                groups[name] = []
                for i in range(1, config["instances"] + 1):
                    groups[name].append(Group(name=name, group=config, instance=i))
            else:  # Standard groups
                groups[name] = Group(name=name, group=config)

        # Initialize Active Directory-type Group user names
        ad_groups = get_ad_groups(groups)
        for g in ad_groups:
            res = self.server.get_users(belong_to_group=g.ad_group, find_users=True)
            if res is not None:
                for r in res:
                    if r.group is True:  # Reference: pyvmomi/docs/vim/UserSearchResult.rst
                        logging.error("Result '%s' is not a user", str(r))
                    else:
                        g.users.append(r.principal)
                g.size = (len(g.users) if len(g.users) > 1 else 1)  # Set the size, default to 1
            else:
                logging.error("Could not initialize AD-group %s", str(g.ad_group))

        if hasattr(self.server.user_dir, "domainList"):
            logging.debug("Domains on server: %s", str(self.server.user_dir.domainList))

        return groups

    def create_masters(self):
        """ Exercise Environment Master creation phase """

        # Get folder containing templates
        self.template_folder = futils.traverse_path(self.server_root,
                                                    self.infra["template-folder"])
        if not self.template_folder:
            logging.error("Could not find template folder in path '%s'",
                          self.infra["template-folder"])
            return
        else:
            logging.debug("Found template folder: '%s'", self.template_folder.name)

        # Create master folder to hold base service instances
        self.master_folder = self.server.create_folder(
            VsphereInterface.master_root_name, self.root_folder)
        logging.info("Created master folder '%s' under folder '%s'",
                     VsphereInterface.master_root_name, self.root_name)

        # Create PortGroups for networks
        # Networks
        #   Create folder to hold portgroups (for easy deletion later)
        #   Create portgroup instances (ensure appending pad() to end of names)
        #   Create generic-networks
        #   Create base-networks
        # TODO: networks
        for net in self.networks:  # Iterate through the base types
            self._create_master_networks(net_type=net, default_create=True)

        # Create Master instances
        # TODO: Apply master-group permissions [default: group permissions]
        self._master_parent_folder_gen(self.folders, self.master_folder)

        # Output fully deployed master folder tree to debugging
        logging.debug(futils.format_structure(
            futils.enumerate_folder(self.root_folder)))

    def _master_parent_folder_gen(self, folder, parent):
        """
        Generates parent-type Master folders
        :param folder: Dict with the folder tree structure as in spec
        :param parent: Parent vim.Folder
        """
        if type(folder) != dict:
            logging.error("Invalid type '%s' for parent Master folder: %s",
                          type(folder).__name__, str(folder))
            return

        group = None
        master_group = None

        # We have to check every item, as they could be either keywords or sub-folders
        for sub_name, sub_value in folder.items():
            if sub_name == "instances":
                pass  # Instances don't matter for the Master phase
            elif sub_name == "description":
                pass  # NOTE: may use Tags or Custom Attributes to add descriptions to objects
            elif sub_name == "group":
                group = self._get_group(sub_value)
            elif sub_name == "master-group":
                master_group = self._get_group(sub_value)
            else:
                folder_name = VsphereInterface.master_prefix + sub_name
                new_folder = self.server.create_folder(folder_name, create_in=parent)

                if "services" in sub_value:  # It's a base folder
                    logging.info("Generating Master base-type folder %s", sub_name)
                    self._master_base_folder_gen(sub_name, sub_value, new_folder)
                else:  # It's a parent folder, recurse
                    logging.info("Generating Master parent-type folder %s", sub_name)
                    self._master_parent_folder_gen(sub_value, parent=new_folder)

        # TODO: apply master group permissions
        if master_group is None:
            master_group = group  # Since group is required, we can safely assume it's been set

    def _master_base_folder_gen(self, folder_name, folder_dict, parent):
        """
        Generates base-type Master folders
        :param folder_name: Name of the base folder
        :param folder_dict: Dict with the base folder tree as in spec
        :param parent: Parent vim.Folder
        """
        if type(folder_dict) != dict:
            logging.error("Invalid type '%s' for base Master folder '%s'",
                          type(folder_dict).__name__, folder_name)
            return

        # Set the group to apply permissions for
        # TODO: apply permissions
        if "master-group" in folder_dict:
            master_group = self._get_group(folder_dict["master-group"])
        else:
            master_group = self._get_group(folder_dict["group"])

        # Create Master instances
        for sname, sconfig in folder_dict["services"].items():
            if not self._is_vsphere(sconfig["service"]):
                logging.debug("Skipping non-vsphere service '%s'", sname)
                continue

            logging.info("Creating Master instance '%s' from service '%s'",
                         sname, sconfig["service"])

            vm = self._clone_service(parent, sconfig["service"])

            if not vm:
                logging.error("Failed to create Master instance '%s' in folder '%s'",
                              sname, folder_name)
                continue  # Skip to the next service

            # NOTE: management interfaces matter here!
            self._configure_nics(vm, networks=sconfig["networks"])  # Configure VM NICs

            # Post-creation snapshot
            vm_utils.create_snapshot(vm, "initial mastering snapshot",
                                     "Beginning of Master configuration")

    def _clone_service(self, folder, service_name):
        """
        Retrieves and clones a service into a master folder
        :param folder: vim.Folder to clone into
        :param service_name: Name of the service to clone
        :return: The service vim.VirtualMachine instance
        """
        if not self._is_vsphere(service_name):
            logging.debug("Skipping non-vsphere service '%s'", service_name)
            return None

        config = self.services[service_name]

        logging.debug("Cloning service '%s'", service_name)
        vm_name = VsphereInterface.master_prefix + service_name

        # Find the template that matches the service definition
        template = futils.traverse_path(self.template_folder, config["template"])
        if not template:
            logging.error("Could not find template '%s' for service '%s'",
                          config["template"], service_name)
            return None

        # Clone the template to create the Master instance
        vm_utils.clone_vm(template, folder=folder, name=vm_name,
                          clone_spec=self.server.gen_clone_spec())

        # Get new cloned instance
        vm = futils.traverse_path(folder, vm_name)
        if vm:
            logging.debug("Successfully cloned service '%s' to folder '%s'",
                          service_name, folder.name)
            if "note" in config:  # Set VM note if specified
                vm_utils.set_note(vm, note=config["note"])
            return vm
        else:
            logging.error("Failed to clone VM '%s' for service '%s'", vm_name, service_name)
            return None

    def _create_master_networks(self, net_type, default_create):
        """
        Creates a network as part of the Master creation phase
        :param net_type: Top-level type of the network (unique | generic | base)
        :param default_create: Whether to create networks if they don't already exist
        """
        self.host.configManager.networkSystem.RefreshNetworkSystem()  # Pick up any recent changes

        for name, config in self.networks[net_type].items():
            logging.info("Creating %s", net_type)
            exists = get_net_obj(host=self.host, object_type="portgroup", name=name, refresh=False)
            if exists:
                logging.debug("PortGroup '%s' already exists on host '%s'", name, self.host.name)
            else:  # NOTE: if monitoring, we want promiscuous=True
                logging.warning("PortGroup '%s' does not exist on host '%s'", name, self.host.name)
                if default_create:
                    logging.debug("Creating portgroup '%s' on host '%s'", name, self.host.name)
                    if "vlan" in config:  # Set the VLAN from the config
                        vlan = int(config["vlan"])
                        if vlan >= 2000:  # It hath strayed into ye dangerous global land
                            logging.warning("Potential VLAN conflict for network: %s", name)
                    else:  # Set VLAN using current "global" unique value
                        vlan = self.vlan_tag_tracker
                        self.vlan_tag_tracker += 1  # Increment VLAN tracker
                    vswitch = (config["vswitch"] if "vswitch" in config else self.vswitch_name)
                    create_portgroup(name=name, host=self.host, vswitch_name=vswitch,
                                     vlan=vlan, promiscuous=False)

    def _configure_nics(self, vm, networks):
        """
        Configures Network Interfaces for a service instance
        :param vm: vim.VirtualMachine
        :param networks: List of networks to configure
        """
        logging.debug("Editing NICs for VM '%s'", vm.name)
        num_nics = len(list(vm.network))
        num_nets = len(networks)
        nets = networks  # Copy the passed variable so we can edit it later

        # Ensure number of NICs on VM matches number of networks configured for the service
        # Note that monitoring interfaces will be counted and included in the networks list
        if num_nics > num_nets:     # Remove excess interfaces
            diff = int(num_nics - num_nets)
            logging.debug("VM '%s' has %d extra NICs, removing...", vm.name, diff)
            for i, nic in zip(range(1, diff + 1), reversed(range(num_nics))):
                vm_utils.delete_nic(vm, nic_number=nic)

        elif num_nics < num_nets:   # Create missing interfaces
            diff = int(num_nets - num_nics)
            logging.debug("VM '%s' is deficient %d NICs, adding...", vm.name, diff)
            for i in range(diff):   # Add NICs to VM and pop them from the list of networks
                nic_model = ("vmxnet3" if vm_utils.has_tools(vm) else "e1000")
                vm_utils.add_nic(vm, network=self.server.get_network(network_name=nets.pop()),
                                 model=nic_model)
            num_nets = len(networks)

        # Edit the interfaces
        # NOTE: any NICs that were added earlier shouldn't be affected by this
        # TODO: traverse folder to get network?
        for net, i in zip(networks, range(1, num_nets + 1)):
            vm_utils.edit_nic(vm, nic_number=i,
                              port_group=self.server.get_network(net), summary=net)

    def deploy_environment(self):
        """ Exercise Environment deployment phase """

        # Get the master folder root
        self.master_folder = futils.traverse_path(self.root_folder,
                                                  VsphereInterface.master_root_name)
        if self.master_folder is None:
            logging.error("Could not find Master folder '%s'. "
                          "Please ensure the  Master Creation phase has been run "
                          "and the folder exists before attempting Deployment",
                          VsphereInterface.master_root_name)
            exit(1)
        logging.debug("Master folder name: %s\tPrefix: %s",
                      self.master_folder.name, VsphereInterface.master_prefix)

        # Verify and convert to templates
        # This is to ensure they are preserved throughout creation and execution of exercise
        logging.info("Converting Masters to Templates")
        self._convert_and_verify(folder=self.master_folder)
        logging.info("Finished converting Masters to Templates")

        # Create base-networks (TODO)

        # Deployment
        #   Create folder structure
        #   Apply permissions
        #   Clone instances
        # TODO: Need to figure out when/how to apply permissions
        # TODO: Base + Generic networks
        # TODO: ensure base + generic have unique VLANs

        logging.info("Deploying environment...")
        self._deploy_parent_folder_gen(spec=self.folders, parent=self.root_folder, path="")
        logging.info("Finished deploying environment")

        # Output fully deployed environment tree to debugging
        logging.debug(futils.format_structure(futils.enumerate_folder(self.root_folder)))

    def _convert_and_verify(self, folder):
        """
        Converts masters to templates before deployment.
        This also ensures they are powered off before being cloned.
        :param folder: vim.Folder
        """
        logging.debug("Converting Masters in folder '%s' to templates", folder.name)
        for item in folder.childEntity:
            if vutils.is_vm(item):
                # Cleanly power off VM before converting to template
                if vm_utils.powered_on(item):
                    vm_utils.change_vm_state(item, "off", attempt_guest=True)

                # Take a snapshot to allow reverts to start of exercise
                vm_utils.create_snapshot(item, "Start of exercise",
                                         "Beginning of deployment phase, post-master configuration")

                # Convert master to template
                vm_utils.convert_to_template(item)
                logging.debug("Converted Master '%s' to Template. Verifying...", item.name)

                # Check if it successfully converted to a snapshot
                if not vm_utils.is_template(item):
                    logging.error("Master '%s' did not convert to template", item.name)
                else:
                    logging.debug("Verified!")
            elif vutils.is_folder(item):  # Recurse into sub-folders
                self._convert_and_verify(item)
            else:
                logging.debug("Unknown item found while converting Masters to templates:"
                              " %s", str(item))

    def _deploy_parent_folder_gen(self, spec, parent, path):
        """
        Generates parent-type folder trees
        :param spec: Dict with folder specification
        :param parent: Parent vim.Folder
        :param path: Folders path at the current level
        """
        if type(spec) != dict:
            logging.error("Invalid type '%s' for parent-type folder '%s'\nPath: %s",
                          type(spec).__name__, str(spec), str(path))
            return

        group = None

        for sub_name, sub_value in spec.items():
            if sub_name == "instances":
                pass  # The instances have already been handled
            elif sub_name == "description":
                pass  # NOTE: may use Tags or Custom Attributes to add descriptions to objects
            elif sub_name == "group":
                group = self._get_group(sub_value)
            elif sub_name == "master-group":
                pass  # Not applicable for Deployment phase
            else:
                num_instances, prefix = self._instances_handler(spec=spec, obj_name=sub_name,
                                                                obj_type="folder")

                # Create instances of the parent folder
                logging.debug("Deploying parent-type folder '%s'", sub_name)
                for i in range(num_instances):
                    # If prefix is undefined or there's a single instance, use the folder's name
                    instance_name = (sub_name if prefix == "" or num_instances == 1 else prefix)

                    # If multiple instances, append padded instance number
                    instance_name += (pad(i) if num_instances > 1 else "")

                    # Create a folder for the instance
                    new_folder = self.server.create_folder(instance_name, create_in=parent)

                    if "services" in sub_value:  # It's a base folder
                        self._deploy_base_folder_gen(folder_name=sub_name, folder_dict=sub_value,
                                                     parent=new_folder,
                                                     path=self._path(path, sub_name))
                    else:  # It's a parent folder
                        self._deploy_parent_folder_gen(parent=new_folder, spec=sub_value,
                                                       path=self._path(path, sub_name))
        # TODO: apply group permissions

    def _deploy_base_folder_gen(self, folder_name, folder_dict, parent, path):
        """
        Generates folder tree for deployment stage
        :param folder_name: Name of the folder
        :param folder_dict: Dict of items in the folder
        :param parent: Parent vim.Folder
        :param path: Folders path at the current level
        """
        if type(folder_dict) != dict:
            logging.error("Invalid type '%s' for base-type folder '%s'\nPath: %s",
                          type(folder_dict).__name__, str(folder_name), str(path))
            return

        # Set the group to apply permissions for
        # TODO: apply permissions
        group = self._get_group(folder_dict["group"])

        # Get number of instances and check if it exceeds configured limits
        num_instances, prefix = self._instances_handler(spec=folder_dict, obj_name=folder_name,
                                                        obj_type="folder")

        # TODO: base + generic networks

        # Create instances
        logging.info("Deploying base-type folder '%s'", folder_name)
        for i in range(num_instances):
            # If no prefix is defined or there's only a single instance, use the folder's name
            instance_name = (folder_name if prefix == "" or num_instances == 1 else prefix)

            # If multiple instances, append padded instance number
            instance_name += (pad(i) if num_instances > 1 else "")

            if num_instances > 1:  # Create a folder for the instance
                new_folder = self.server.create_folder(instance_name, create_in=parent)
            else:  # Don't duplicate folder name for single instances
                new_folder = parent

            # Use the folder's name for the path, as that's what matches the Master version
            logging.info("Generating services for base-type folder instance '%s'", instance_name)
            self._deploy_gen_services(services=folder_dict["services"], parent=new_folder,
                                      path=self._path(path, folder_name))

    def _deploy_gen_services(self, services, parent, path):
        """
        Generates the services in a folder
        :param services: The "services" dict in a folder
        :param parent: Parent vim.Folder
        :param path: Folders path at the current level
        """
        # Enumerate networks in folder
        #   Create generic networks
        #   Create next instance of a base network and increment base counter for folder
        if type(services) != dict:
            logging.error("Invalid type '%s' for services '%s'\nPath: %s",
                          type(services).__name__, str(services), str(path))
            return

        # Aggregate all networks
        aggregate_nets = []
        for _, value in services.items():
            aggregate_nets.extend(value["networks"])
        services_nets = set(aggregate_nets)  # Remove duplicates
        local_net_table = {}

        for net in services_nets:
            net_type = self._determine_net_type(net)
            if net_type == "generic-networks":  # Append net number to the name
                if net not in self.net_table:
                    self.net_table[net] = 1
                else:
                    self.net_table[net] += 1
                net_name = net + " GENERIC " + pad(self.net_table[net])
                local_net_table[net] = net_name
            elif net_type == "base-networks":  # TODO: fully implement
                if net not in self.net_table:
                    self.net_table[net] = 1
                else:
                    self.net_table[net] += 1
                net_name = net + " BASE " + pad(self.net_table[net])
                local_net_table[net] = net_name

        # TODO: network creation function for generic networks + base networks

        # Iterate through the services
        for service_name, value in services.items():
            # Ignore non-vsphere services
            if not self._is_vsphere(value["service"]):
                logging.debug("Skipping non-vsphere service '%s'", service_name)
                continue
            logging.info("Generating service '%s' in folder '%s'", service_name, parent.name)

            # Get number of instances for the service and check if it exceeds configured limits
            num_instances, prefix = self._instances_handler(spec=value, obj_name=service_name,
                                                            obj_type="service")

            # Get the Master template instance to clone from
            service = futils.traverse_path(self.master_folder, self._path(path, value["service"]))
            if service is None:  # Check if the lookup was successful
                logging.error("Could not find Master instance for service '%s' in this path:\n%s",
                              value["service"], path)
                continue  # Skip to the next service

            # TODO: implement table lookup for NIC configuration (make as a function)
            # We can use _configure_nics, but we'll need to modify the dict
            # first to account for naming collisions
            # nets = value["networks"]

            # Clone the instances of the service from the master
            for i in range(num_instances):
                instance_name = prefix + service_name + (" " + pad(i) if num_instances > 1 else "")
                vm_utils.clone_vm(vm=service, folder=parent, name=instance_name,
                                  clone_spec=self.server.gen_clone_spec())
                # vm = futils.traverse_path(parent, instance_name)
                # if vm:
                #    self._configure_nics(vm=vm, networks=nets)
                # else:
                #    logging.error("Could not find cloned instance '%s' in folder '%s'",
                #                  instance_name, service_name, parent.name)

    @staticmethod
    def _path(path, name):
        """
        Generates next step of the path for deployment of masters
        :param path:
        :param name:
        :return:
        """
        return str(path + '/' + VsphereInterface.master_prefix + name)

    def _instances_handler(self, spec, obj_name, obj_type):
        """
        Determines number of instances and optional prefix using specification
        :param spec: Dict of folder
        :param obj_name: Name of the thing being handled
        :param obj_type: Type of the thing being handled (folder | service)
        :return: (Number of instances, Prefix)
        """
        # TODO: move this into base Interface class
        num = 1
        prefix = ""
        if "instances" in spec:
            if type(spec["instances"]) == int:
                num = int(spec["instances"])
            else:
                if "prefix" in spec["instances"]:
                    prefix = str(spec["instances"]["prefix"])

                if "number" in spec["instances"]:
                    num = int(spec["instances"]["number"])
                elif "size-of" in spec["instances"]:
                    size_of = spec["instances"]["size-of"]
                    # TODO: template group size resolution
                    # if size_of[-2:] == ' X':
                    #     num = int(self._get_group(size_of[:-2])) # Lookup
                    num = int(self._get_group(size_of).size)
                    if num < 1:  # WORKAROUND FOR AD-GROUPS
                        num = 1
                else:
                    logging.error("Unknown instances specification: %s", str(spec["instances"]))
                    num = 0

        # Check if the number of instances exceeds the configured thresholds for the interface
        if num > self.thresholds[obj_type]["error"]:
            logging.error("%d instances of %s '%s' is beyond the configured %s threshold of %d",
                          num, obj_type, obj_name, self.__name__,
                          self.thresholds[obj_type]["error"])
            raise Exception("Threshold exception")
        elif num > self.thresholds[obj_type]["warn"]:
            logging.warning("%d instances of %s '%s' is beyond the configured %s threshold of %d",
                            num, obj_type, obj_name, self.__name__,
                            self.thresholds[obj_type]["warn"])

        return num, prefix

    def _get_group(self, group_name):
        """
        Provides a uniform way to get information about normal groups and template groups
        :param group_name: Name of the group
        :return: Group object
        """
        from adles.group import Group
        if group_name in self.groups:
            g = self.groups[group_name]
            if isinstance(g, Group):    # Normal groups
                return g
            elif isinstance(g, list):   # Template groups
                return g[0]
            else:
                logging.error("Unknown type for group '%s': %s", str(group_name), str(type(g)))
        else:
            logging.error("Could not get group '%s' from VsphereInterface groups", group_name)

    def _is_vsphere(self, service_name):
        """
        Checks if a service instance is defined as a vSphere service
        :param service_name: Name of the service to lookup in list of defined services
        :return: bool
        """
        # TODO: make "template" and other platform identifiers global 'constants'
        if service_name not in self.services:
            logging.error("Could not find service %s in the list of defined services", service_name)
        elif "template" in self.services[service_name]:
            return True
        return False

    def _determine_net_type(self, network_label):
        """
        Determines the type of a network
        :param network_label: Name of the network
        :return: Type of the network
        """
        for net_name, net_value in self.networks.items():
            if network_label in net_value:
                return net_name
        return ""

    def cleanup_masters(self, network_cleanup=False):
        """ Cleans up any master instances"""

        # TODO: look at getorphanedvms in pyvmomi-community-samples for how to do this
        # Get the folder to cleanup in
        master_folder = futils.find_in_folder(self.root_folder, self.master_root_name)
        logging.info("Found master folder '%s' under folder '%s', proceeding with cleanup...",
                     master_folder.name, self.root_folder.name)

        # Recursively descend from master folder, destroying anything with the prefix
        futils.cleanup(folder=master_folder, vm_prefix=self.master_prefix,
                       recursive=True, destroy_folders=True, destroy_self=True)

        # Cleanup networks (TODO: use network folders to aid in this, during creation phase)
        if network_cleanup:
            pass

    def cleanup_environment(self, network_cleanup=False):
        """ Cleans up a deployed environment """

        # Get the root environment folder to cleanup in
        enviro_folder = self.root_folder

        # TODO: ensure master folder is skipped

        # Cleanup networks (TODO: use network folders to aid in this, during creation phase)
        if network_cleanup:
            pass
