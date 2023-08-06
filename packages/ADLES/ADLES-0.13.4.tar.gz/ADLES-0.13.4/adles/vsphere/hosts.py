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

from pyVmomi import vim

from adles.vsphere.vsphere_utils import wait_for_task


# TODO: edit vswitch, edit portgroup
class Host:
    """ Represents an ESXi host in a VMware vSphere environment. """
    __version__ = "0.3.0"

    def __init__(self, host):
        self._log = logging.getLogger('Host')
        self.host = host
        self.name = str(host.name)
        self.config = host.config

    def reboot(self, force=False):
        """
        Reboots the host
        :param force: Force a reboot even if the host is not in maintenance mode
        """
        self._log.warning("Rebooting host %s", self.name)
        wait_for_task(self.host.RebootHost_Task(force=bool(force)))

    def shutdown(self, force=False):
        """
        Shuts down the host
        :param force: Force a reboot even if the host is not in maintenance mode
        """
        self._log.warning("Shutting down host %s", self.name)
        wait_for_task(self.host.ShutdownHost_Task(force=bool(force)))

    def enter_maintenance_mode(self, timeout=0, spec=None):
        """
        Enter maintenance mode
        :param timeout: Seconds to wait [default: 0]
        :param spec: Actions to be taken upon entering maintenance mode (HostMaintenanceSpec)
        """
        self._log.warning("%s is entering maintainence mode", self.name)
        wait_for_task(self.host.EnterMaintenanceMode_Task(timeout=int(timeout),
                                                          maintenanceSpec=spec))

    def exit_maintenance_mode(self, timeout=0):
        """
        Exit maintenance mode
        :param timeout: Seconds to wait [default: 0]
        """
        self._log.info("%s is exiting maintainence mode", self.name)
        wait_for_task(self.host.ExitMaintenanceMode_Task(timeout=int(timeout)))

    def create_vswitch(self, name, num_ports=512):
        """
        Creates a vSwitch
        :param name: Name of the vSwitch to create
        :param num_ports: Number of ports the vSwitch should have [default: 512]
        """
        self._log.info("Creating vSwitch %s with %d ports on host %s", name, num_ports, self.name)
        vswitch_spec = vim.host.VirtualSwitch.Specification()
        vswitch_spec.numPorts = int(num_ports)
        try:
            self.host.configManager.networkSystem.AddVirtualSwitch(name, vswitch_spec)
        except vim.fault.AlreadyExists:
            self._log.error("vSwitch %s already exists on host %s", name, self.name)

    def create_portgroup(self, name, vswitch_name, vlan=0, promiscuous=False):
        """
        Creates a portgroup
        :param name: Name of portgroup to create
        :param vswitch_name: Name of vSwitch on which to create the port group
        :param vlan: VLAN ID of the port group [default: 0]
        :param promiscuous: Put portgroup in promiscuous mode [default: False]
        """
        self._log.info("Creating PortGroup %s on vSwitch %s on host %s", name, vswitch_name,
                       self.name)
        self._log.debug("VLAN ID: %d \t Promiscuous: %s", vlan, promiscuous)

        spec = vim.host.PortGroup.Specification()
        spec.name = name
        spec.vlanId = int(vlan)
        spec.vswitchName = vswitch_name
        policy = vim.host.NetworkPolicy()
        policy.security = vim.host.NetworkPolicy.SecurityPolicy()
        policy.security.allowPromiscuous = bool(promiscuous)
        policy.security.macChanges = False
        policy.security.forgedTransmits = False
        spec.policy = policy

        try:
            self.host.configManager.networkSystem.AddPortGroup(spec)
        except vim.fault.AlreadyExists:
            self._log.error("PortGroup %s already exists on host %s", name, self.name)
        except vim.fault.NotFound:
            self._log.error("vSwitch %s does not exist on host %s", vswitch_name, self.name)

    def delete_network(self, name, network_type):
        """
        Deletes the named network from the host
        :param name: Name of the vSwitch to delete
        :param network_type: Type of the network to remove ("vswitch" | "portgroup")
        """
        self._log.info("Deleting %s '%s' from host '%s'", network_type, name, self.name)
        try:
            if network_type.lower() == "vswitch":
                self.host.configManager.networkSystem.RemoveVirtualSwitch(name)
            elif network_type.lower() == "portgroup":
                self.host.configManager.networkSystem.RemovePortGroup(name)
        except vim.fault.NotFound:
            self._log.error("Tried to remove %s '%s' that does not exist from host '%s'",
                            network_type, name, self.name)
        except vim.fault.ResourceInUse:
            self._log.error("%s '%s' can't be removed because there are vNICs associated with it",
                            network_type, name)

    def get_info(self):
        """
        Get information about the host
        :return: Formatted String with host information
        """
        return str(self.config)  # TODO: host information much like get_info()

    def get_net_item(self, object_type, name):
        """
        Retrieves a network object of the specified type and name from a host
        :param object_type: Type of object to get: (portgroup | vswitch | proxyswitch | vnic | pnic)
        :param name: Name of network object [default: first object found]
        :return: The network object
        """
        if name:
            return self.get_net_obj(object_type, name)
        else:
            return self.get_net_objs(object_type)[0]

    def get_net_obj(self, object_type, name, refresh=False):
        """
        Retrieves a network object of the specified type and name from a host
        :param object_type: Type of object to get: (portgroup | vswitch | proxyswitch | vnic | pnic)
        :param name: Name of network object
        :param refresh: Refresh the host's network system information [default: False]
        :return: The network object
        """
        objs = self.get_net_objs(object_type=object_type, refresh=refresh)
        obj_name = name.lower()
        if objs is not None:
            for obj in objs:
                if object_type == "portgroup" or object_type == "proxyswitch":
                    if obj.spec.name.lower() == obj_name:
                        return obj
                elif object_type == "pnic" or object_type == "vnic":
                    if obj.device.lower() == obj_name:
                        return obj
                elif obj.name.lower() == obj_name:
                    return obj
        return None

    def get_net_objs(self, object_type, refresh=False):
        """
        Retrieves all network objects of the specified type from the host
        :param object_type: Type of object to get: (portgroup | vswitch | proxyswitch | vnic | pnic)
        :param refresh: Refresh the host's network system information [default: False]
        :return: list of the network objects
        """
        if refresh:
            self.host.configManager.networkSystem.RefreshNetworkSystem()  # Pick up recent changes
        net_type = object_type.lower()
        if net_type == "portgroup":
            objects = self.host.configManager.networkSystem.networkInfo.portgroup
        elif net_type == "vswitch":
            objects = self.host.configManager.networkSystem.networkInfo.vswitch
        elif net_type == "proxyswitch":
            objects = self.host.configManager.networkSystem.networkInfo.proxySwitch
        elif net_type == "vnic ":
            objects = self.host.configManager.networkSystem.networkInfo.vnic
        elif net_type == "pnic ":
            objects = self.host.configManager.networkSystem.networkInfo.pnic
        else:
            self._log.error("Invalid type %s for get_net_objs", object_type)
            return None
        return list(objects)

    def __str__(self):
        return str(self.name)

    def __hash__(self):
        return hash(self.host)

    def __eq__(self, other):
        return self.name == other.name

    def __ne__(self, other):
        return not self.__eq__(other)


# TODO: implement
class Cluster:
    """ Represents a cluster of ESXi hosts in a VMware vSphere environment. """
    __version__ = "0.1.0"

    def __init__(self):
        self._log = logging.getLogger('Cluster')
