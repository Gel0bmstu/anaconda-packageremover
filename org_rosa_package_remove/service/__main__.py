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

"""The __main__.py file of a service is what runs as the service. See also the files:
data/*.service
"""

from pyanaconda.modules.common import init
init()  # must be called before importing the service code

# pylint:disable=wrong-import-position
from org_rosa_package_remove.service.package_remove import PackageRemove
with open('/tmp/debug.log', 'a+') as f:
    f.write('call "run" service in __main__\n')
service = PackageRemove()
service.run()