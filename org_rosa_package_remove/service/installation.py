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

"""
This module contains tasks of the D-Bus service.

A task - Task subclass - performs actual work such as manipulating files.
Tasks run in threads so as not to block communication with the service
process. All installation and configuration jobs must be represented as Tasks.

Tasks can be used in multiple situations. Generally there are three kinds
of tasks:
  * Configuration task - runs at start on installation.
  * Installation task - runs at end of installation.
  * Calculation task - runs whenever code makes it run.

The difference between the three kinds is where they come from - configuration
and installation tasks are returned by specific methods in the service's main
class, so they are run at pre-defined times.

Every kind of task has the run() method that performs the actual work.
"""

import logging
from os.path import normpath, join as joinpath

from pyanaconda.modules.common.task import Task

from org_rosa_package_remove.constants import REMOVABLE_PACKAGES_FILE_PATH

log = logging.getLogger(__name__)


class PackageRemoveConfigurationTask(Task):
    """The PackageRemove configuration task.

    This task runs before the installation starts.
    """

    @property
    def name(self):
        return "Configure PackageRemove"

    def run(self):
        """The run method performs the actual work.

        No actions happen in this addon.
        """
        log.info("Running configuration task.")


class PackageRemoveInstallationTask(Task):
    """The PackageRemove installation task.

    This task runs at end of installation.
    """

    def __init__(self, sysroot, pkgs):
        super().__init__()
        self._sysroot = sysroot
        self._pkgs = pkgs

    @property
    def name(self):
        return "Install RemovablePackages"

    def run(self):
        """The run method performs the actual work."""
        log.info("Running installation task.")
        package_remove_file_path = normpath(joinpath(self._sysroot, REMOVABLE_PACKAGES_FILE_PATH))
        log.debug("Writing removable pkgs to: %s", package_remove_file_path)

        with open(package_remove_file_path, "w") as f:
            for pkg in self._pkgs:
                f.write('{}\n'.format(pkg))
