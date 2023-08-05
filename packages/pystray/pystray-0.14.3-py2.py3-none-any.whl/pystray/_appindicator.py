# coding=utf-8
# pystray
# Copyright (C) 2016-2017 Moses Palmér
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option) any
# later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import os
import tempfile

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

gi.require_version('AppIndicator3', '0.1')
from gi.repository import AppIndicator3 as AppIndicator

from ._util.gtk import GtkIcon, mainloop
from ._util import serialized_image
from . import _base


class Icon(GtkIcon):
    # We expand the menu on primary button click, and we do not even support
    # empty menus
    HAS_DEFAULT_ACTION = False

    def __init__(self, *args, **kwargs):
        super(Icon, self).__init__(*args, **kwargs)

        self._appindicator = None
        self._appindicator_icon_path = None

        if self.icon:
            self._update_icon()

    @mainloop
    def _show(self):
        self._appindicator = AppIndicator.Indicator.new(
            self.name,
            '',
            AppIndicator.IndicatorCategory.APPLICATION_STATUS)

        self._appindicator.set_status(AppIndicator.IndicatorStatus.ACTIVE)
        self._appindicator.set_icon(self._appindicator_icon_path)
        self._appindicator.set_menu(
            self._menu_handle or self._create_default_menu())

    @mainloop
    def _hide(self):
        self._appindicator = None

    @mainloop
    def _update_icon(self):
        self._remove_appindicator_icon()
        self._update_appindicator_icon()
        if self._appindicator:
            self._appindicator.set_icon(self._appindicator_icon_path)

    @mainloop
    def _update_title(self):
        self._appindicator.set_title(self.title)

    def _create_menu_handle(self):
        menu = super(Icon, self)._create_menu_handle()

        if self._appindicator:
            self._appindicator.set_menu(menu or self._create_default_menu())

        return menu

    def _finalize(self):
        del self._appindicator

    def _remove_appindicator_icon(self):
        """Removes the temporary file used for the *AppIndicator*.
        """
        try:
            if self._appindicator_icon_path:
                os.unlink(self._appindicator_icon_path)
                self._appindicator_icon_path = None
        except:
            pass

    def _update_appindicator_icon(self):
        """Updates the *AppIndicator* icon.

        This method will update :attr:`_appindicator_icon_path` and create a new
        image file.

        If an *AppIndicator* icon is already set, call
        :meth:`_remove_appindicator_icon` first to ensure that the old file is
        removed.
        """
        self._appindicator_icon_path = tempfile.mktemp()
        with open(self._appindicator_icon_path, 'wb') as f:
            self.icon.save(f, 'PNG')

    def _create_default_menu(self):
        """Creates a :class:`Gtk.Menu` from the default menu entry.

        :return: a :class:`Gtk.Menu`
        """
        menu = Gtk.Menu.new()
        if self.menu is not None:
            menu.append(self._create_menu_item(next(
                menu_item
                for menu_item in self.menu.items
                if menu_item.default)))
        else:
            menu.append(self._create_menu_item(
                _base.MenuItem(self.name, lambda _: None)))
        menu.show_all()

        return menu
