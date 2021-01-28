#
# Copyright (C) 2020 Red Hat, Inc.
#
# This copyrighted material is made available to anyone wishing to use,
# modify, copy, or redistribute it subject to the terms and conditions of
# the GNU General Public License v.2, or (at your option) any later version.
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY expressed or implied, including the implied warranties of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General
# Public License for more details.  You should have received a copy of the
# GNU General Public License along with this program; if not, write to the
# Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301, USA.  Any Red Hat trademarks that are incorporated in the
# source code or documentation are not subject to the GNU General Public
# License and may only be used or replicated with the express permission of
# Red Hat, Inc.
#
import logging

from pyanaconda.core.configuration.anaconda import conf
from pyanaconda.core.dbus import DBus
from pyanaconda.core.signal import Signal
from pyanaconda.modules.common.base import KickstartService
from pyanaconda.modules.common.containers import TaskContainer

from org_fedora_hello_world.constants import HELLO_WORLD, PACKAGES_LIST_FILE_PATH
from org_fedora_hello_world.service.hello_world_interface import HelloWorldInterface
from org_fedora_hello_world.service.installation import HelloWorldConfigurationTask, \
    HelloWorldInstallationTask
from org_fedora_hello_world.service.kickstart import HelloWorldKickstartSpecification

log = logging.getLogger(__name__)


class HelloWorld(KickstartService):
    """The HelloWorld D-Bus service.

    This class parses and stores data for the Hello world addon.
    """

    def __init__(self):
        super().__init__()
        self._remove = []
        self._list = []

        self.remove_pkgs_changed = Signal()

    def publish(self):
        """Publish the module."""
        TaskContainer.set_namespace(HELLO_WORLD.namespace)
        DBus.publish_object(HELLO_WORLD.object_path, HelloWorldInterface(self))
        DBus.register_service(HELLO_WORLD.service_name)

    @property
    def kickstart_specification(self):
        """Return the kickstart specification."""
        return HelloWorldKickstartSpecification

    def process_kickstart(self, data):
        """Process the kickstart data."""
        log.debug("Processing kickstart data...")
        self._list = data.addons.org_fedora_hello_world.list
        self._remove = data.addons.org_fedora_hello_world.remove

    def setup_kickstart(self, data):
        """Set the given kickstart data."""
        log.debug("Generating kickstart data...")
        data.addons.org_fedora_hello_world.list = self._list
        data.addons.org_fedora_hello_world.remove = self._remove

    @property
    def list(self):
        """Lines of the hello world file."""
        self._get_packages_list()
        return self._list

    def set_pkgs_to_remove(self, pkgs):
        self._remove = pkgs
        self.remove_pkgs_changed.emit()

    def configure_with_tasks(self):
        """Return configuration tasks.

        The configuration tasks are run at the beginning of the installation process.

        Anaconda's code automatically calls the ***_with_tasks methods and
        stores the returned ***Task instances to later execute their run() methods.
        """
        task = HelloWorldConfigurationTask()
        return [task]

    def install_with_tasks(self):
        """Return installation tasks.

        The installation tasks are run at the end of the installation process.

        Anaconda's code automatically calls the ***_with_tasks methods and
        stores the returned ***Task instances to later execute their run() methods.
        """
        task = HelloWorldInstallationTask(
            conf.target.system_root,
            self._remove)
        return [task]

    def _get_packages_list(self):
        pkgs = []
        with open(PACKAGES_LIST_FILE_PATH) as pkgs_list:
            try:
                for pkg in pkgs_list:
                    if pkg.strip() != "" and pkg[0] != "#":
                        pkgs.append(pkg.strip())

                self._list = sorted(pkgs)

            except Exception as e:
                log.error('Unable to process removable pakgs file.')
                return

        log.debug('Packages list from {} getted succeessfully.'.format(PACKAGES_LIST_FILE_PATH))