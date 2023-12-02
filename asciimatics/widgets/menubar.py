"""This module implements a menu bar widget"""
from asciimatics.widgets.layout import Layout
from asciimatics.widgets.button import Button
from asciimatics.widgets.divider import Divider
from asciimatics.widgets.popupmenu import PopupMenu


class MenuBar(Layout):
    """
    A widget for displaying a menu bar.
    """

    def __init__(self, frame, menus, has_border=True):
        """
        :param frame: The Frame being used for this menu.
        :param menus: a list of menus to be displayed in the bar.
        :param have_borders: Whether the menus have border boxes when displayed. Defaults to True.

        The menus parameter is a list of 2-tuples, which define the text to be displayed in
        the menu and the function to call when that menu item is clicked.  For example:

            menus = [("File", file_menu), ("Edit", edit_menu), ("help", help_menu)]

        The second parameter in each tuple is itself a list of 2-tuples, which define the
        text to be displayed in the menu and the function to call when that menu item is
        clicked.  For example:

            file_menu = [("Open", file_open), ("Save", file_save), ("Close", file_close)]
        """

        self._has_border = has_border

        menu_widths = [len(x[0]) + 2 for x in menus]
        menu_widths.append(frame.screen.width - sum(menu_widths))

        super().__init__(columns=menu_widths, fill_frame=False, gutter=1)

        self._frame = frame

        self._menu_items = {}
        for column, (menu_name, menu_items) in enumerate(menus):
            menu = Button(
                text=menu_name,
                on_click=lambda menu_name=menu_name: self._activate_menu(
                    menu_name),
                name=menu_name,
                add_box=False,
                tab_stop=True,
            )

            self.add_widget(widget=menu, column=column)

            self._menu_items[menu_name] = menu_items

    def _activate_menu(self, menu_name):
        menu = self.find_widget(menu_name)
        (x, y) = menu.get_location()

        popup = PopupMenu(
            screen=self._frame.screen,
            menu_items=self._menu_items[menu_name],
            x=x,
            y=y + 1,
            has_border=self._has_border,
        )
        popup.palette = self._frame.palette

        self._frame._scene.add_effect(popup)

    def update_menu_items(self, menu_name, menu_items):
        if menu_name not in self._menu_items.keys():
            raise KeyError(
                f'Cannot add new menu with update_menu_items: {menu_name}')
        self._menu_items[menu_name] = menu_items
