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

import adles.utils as utils
from adles.vsphere.vsphere_utils import wait_for_task


class Folder:
    """ Represents a VMware vSphere Folder instance. """
    __version__ = "0.1.0"

    def __init__(self, folder, host):
        self._log = logging.getLogger('Folder')
        self.folder = folder
        self.name = folder.name
        self.host = host

    def move_into(self, entity_list):
        """
        Moves a list of managed entities into the named folder.
        :param folder: vim.Folder object with type matching the entity list
        :param entity_list: List of vim.ManagedEntity
        """
        wait_for_task(self.folder.MoveIntoFolder_Task(entity_list))

    def __str__(self):
        return str(self.name)

    def __hash__(self):
        return hash(self.folder)

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.name == other.name

    def __ne__(self, other):
        return not self.__eq__(other)
