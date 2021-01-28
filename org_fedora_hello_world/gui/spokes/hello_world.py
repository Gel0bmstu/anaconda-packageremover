#
# Copyright (C) 2013  Red Hat, Inc.
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
# Red Hat Author(s): Vratislav Podzimek <vpodzime@redhat.com>
#

"""Module with the HelloWorldSpoke class."""

import logging

import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Pango

from pyanaconda.ui.gui import GUIObject
from pyanaconda.ui.gui.spokes import NormalSpoke
from pyanaconda.ui.common import FirstbootSpokeMixIn

# the path to addons is in sys.path so we can import things from org_fedora_hello_world
from org_fedora_hello_world.categories.hello_world import HelloWorldCategory
from org_fedora_hello_world.constants import HELLO_WORLD, PACKAGES_LIST_FILE_PATH, REMOVABLE_PACKAGES_FILE_PATH

log = logging.getLogger(__name__)

# export only the spoke, no helper functions, classes or constants
__all__ = ["HelloWorldSpoke"]

# import gettext
# _ = lambda x: gettext.ldgettext("hello-world-anaconda-plugin", x)

# will never be translated
_ = lambda x: x
N_ = lambda x: x


class HelloWorldSpoke(FirstbootSpokeMixIn, NormalSpoke):
    """
    Class for the Hello world spoke. This spoke will be in the Hello world
    category and thus on the Summary hub. It is a very simple example of a unit
    for the Anaconda's graphical user interface. Since it is also inherited form
    the FirstbootSpokeMixIn, it will also appear in the Initial Setup (successor
    of the Firstboot tool).


    :see: pyanaconda.ui.common.UIObject
    :see: pyanaconda.ui.common.Spoke
    :see: pyanaconda.ui.gui.GUIObject
    :see: pyanaconda.ui.common.FirstbootSpokeMixIn
    :see: pyanaconda.ui.gui.spokes.NormalSpoke
    """
    ### class attributes defined by API ###

    # list all top-level objects from the .glade file that should be exposed
    # to the spoke or leave empty to extract everything
    builderObjects = ["helloWorldSpokeWindow", "buttonImage"]

    # the name of the main window widget
    mainWidgetName = "helloWorldSpokeWindow"

    # name of the .glade file in the same directory as this source
    uiFile = "hello_world.glade"

    # category this spoke belongs to
    category = HelloWorldCategory

    # spoke icon (will be displayed on the hub)
    # preferred are the -symbolic icons as these are used in Anaconda's spokes
    icon = "face-cool-symbolic"

    # title of the spoke (will be displayed on the hub)
    title = N_("_Packet Chose")

    ### methods defined by API ###
    def __init__(self, data, storage, payload):
        """
        :see: pyanaconda.ui.common.Spoke.__init__
        :param data: data object passed to every spoke to load/store data
                     from/to it
        :type data: pykickstart.base.BaseHandler
        :param storage: object storing storage-related information
                        (disks, partitioning, bootloader, etc.)
        :type storage: blivet.Blivet
        :param payload: object storing packaging-related information
        :type payload: pyanaconda.packaging.Payload
        """
        NormalSpoke.__init__(self, data, storage, payload)

        self._hello_world_module = HELLO_WORLD.get_proxy()

    def initialize(self):
        """
        The initialize method that is called after the instance is created.
        The difference between __init__ and this method is that this may take
        a long time and thus could be called in a separated thread.

        :see: pyanaconda.ui.common.UIObject.initialize
        """
        NormalSpoke.initialize(self)
        self._entry = self.builder.get_object("textLines")

    def refresh(self):
        """
        The refresh method that is called every time the spoke is displayed.
        It should update the UI elements according to the contents of
        self.data.

        :see: pyanaconda.ui.common.UIObject.refresh
        """
        self._print_packages(self._hello_world_module.Lines)

    def apply(self):
        """
        The apply method that is called when the spoke is left. It should
        update the D-Bus service with values set in the GUI elements.
        """
        rows = self._entry.get_children()
        pkgs_to_remove = []
        for row in rows:
            grid_list = row.get_children()
            grid = grid_list[0]

            pkg_name = grid.get_child_at(0, 0)
            check = grid.get_child_at(1, 0)
            if check.get_active():
                pkgs_to_remove.append(pkg_name.get_text())

        self._hello_world_module.SetLines(pkgs_to_remove)

    def execute(self):
        """
        The execute method that is called when the spoke is left. It is
        supposed to do all changes to the runtime environment according to
        the values set in the GUI elements.
        """
        # nothing to do here
        # old_rows = self._entry.get_children()
        # for r in old_rows:
        #     self._entry.remove(r)

    def _print_packages(self, pkgs_list):
        for name in pkgs_list:
            row = Gtk.ListBoxRow()
            grd = Gtk.Grid()

            grd.set_column_homogeneous(False)
            grd.set_row_homogeneous(False)
            grd.insert_row(0)
            grd.insert_column(0)

            row.add(grd)

            label = Gtk.Label(valign=Gtk.Align.FILL)
            label.set_use_markup(True)
            label.set_markup('<big>{}</big>'.format(name))
            label.set_selectable(False)
            label.set_line_wrap(True)
            label.set_hexpand(True)
            label.set_vexpand(True)
            label.set_justify(Gtk.Justification.LEFT)
            # label.set_valign(Gtk.Align.FILL)
            label.set_halign(Gtk.Align.START)
            label.props.margin_left = 10

            checkbox = Gtk.CheckButton()
            checkbox.props.margin_right = 20
            checkbox.props.valign = Gtk.Align.CENTER

            grd.attach(label, 0, 0, 1, 1)
            grd.attach(checkbox, 1, 0, 1, 1)

            self._entry.add(row)

    @property
    def ready(self):
        """
        The ready property that tells whether the spoke is ready (can be visited)
        or not. The spoke is made (in)sensitive based on the returned value.

        :rtype: bool
        """
        # this spoke is always ready
        return True

    @property
    def completed(self):
        """
        The completed property that tells whether all mandatory items on the
        spoke are set, or not. The spoke will be marked on the hub as completed
        or uncompleted acording to the returned value.

        :rtype: bool
        """
        return True

    @property
    def mandatory(self):
        """
        The mandatory property that tells whether the spoke is mandatory to be
        completed to continue in the installation process.

        :rtype: bool
        """
        # this is an optional spoke that is not mandatory to be completed
        return False

    @property
    def status(self):
        """
        The status property that is a br_grid_click_handlerief string describing the state of the
        spoke. It should describe whether all values are set and if possible
        also the values themselves. The returned value will appear on the hub
        below the spoke's title.

        :rtype: str
        """

        return _('Select packages to remove on installed system')

    # def _grid_click_handler(self, row, mock):
    #     grid_list = row.get_children()
    #     check = grid_list[0]

    #     with open('/tmp/checkbox.log', 'w') as f: 
    #         if check.get_active():
    #             f.write('Checkbox setted to False')
    #             check.set_active(False)
    #         else:
    #             f.write('Checkbox setted to True')
    #             check.set_active(True)