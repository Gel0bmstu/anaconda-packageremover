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

from org_fedoraproject_package_remove.constants import PACKAGE_REMOVE, PACKAGES_LIST_FILE_PATH
from org_fedoraproject_package_remove.service.package_remove_interface import PackageRemoveInterface
from org_fedoraproject_package_remove.service.installation import PackageRemoveConfigurationTask, \
    PackageRemoveInstallationTask
from org_fedoraproject_package_remove.service.kickstart import PackageRemoveKickstartSpecification

log = logging.getLogger(__name__)

__all__ = ["PackageRemove"]

class PackageRemove(KickstartService):
    """The PackageRemove D-Bus service.

    This class parses and stores data for the Package remove addon.
    """

    def __init__(self):
        super().__init__()
        self._remove = []
        self._list = []

        with open('/tmp/debug.log', 'a+') as f:
            f.write('init PackageRemove service: {}\n'.format(self._remove))

        self.remove_pkgs_changed = Signal()

    def publish(self):
        """Publish the module."""
        with open('/tmp/debug.log', 'a+') as f:
            f.write('Publish PackageRemove module: {}\n{}\n{}\n'.format(
                PACKAGE_REMOVE.namespace,
                PACKAGE_REMOVE.object_path,
                PACKAGE_REMOVE.service_name
            ))
        TaskContainer.set_namespace(PACKAGE_REMOVE.namespace)
        DBus.publish_object(PACKAGE_REMOVE.object_path, PackageRemoveInterface(self))
        DBus.register_service(PACKAGE_REMOVE.service_name)

    @property
    def kickstart_specification(self):
        """Return the kickstart specification."""
        return PackageRemoveKickstartSpecification

    def process_kickstart(self, data):
        """Process the kickstart data."""
        log.debug("Processing kickstart data...")
        self._list = data.addons.org_fedoraproject_package_remove.list
        self._remove = data.addons.org_fedoraproject_package_remove.remove

    def setup_kickstart(self, data):
        """Set the given kickstart data."""
        log.debug("Generating kickstart data...")
        data.addons.org_fedoraproject_package_remove.list = self._list
        data.addons.org_fedoraproject_package_remove.remove = self._remove

    @property
    def list(self):
        """Lines of the package remove file."""
        self._get_packages_list()
        return self._list

    def set_pkgs_to_remove(self, pkgs):
        self._remove = pkgs
        self.remove_pkgs_changed.emit()

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

    def configure_with_tasks(self):
        """Return configuration tasks.

        The configuration tasks are run at the beginning of the installation process.

        Anaconda's code automatically calls the ***_with_tasks methods and
        stores the returned ***Task instances to later execute their run() methods.
        """
        with open('/tmp/debug.log', 'a+') as f:
            f.write('configure_with_tasks\n')

        return [PackageRemoveConfigurationTask()]

    def install_with_tasks(self):
        """Return installation tasks.

        The installation tasks are run at the end of the installation process.

        Anaconda's code automatically calls the ***_with_tasks methods and
        stores the returned ***Task instances to later execute their run() methods.
        """
        with open('/tmp/debug.log', 'a+') as f:
            f.write('install_with_tasks\n')

        return [
            PackageRemoveInstallationTask(
                sysroot=conf.target.system_root,
                pkgs=self._remove)
        ] 