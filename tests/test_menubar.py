#!/usr/bin/env python3

import unittest
from unittest.mock import MagicMock

from .widget_tester import WidgetTester

from asciimatics.event import MouseEvent
from asciimatics.scene import Scene
from asciimatics.screen import Screen, Canvas
from asciimatics.widgets import Frame, MenuBar

canvas_default = '''\
+--------------------------------------+
|file  edit                            |
|                                      O
|                                      |
|                                      |
|                                      |
|                                      |
|                                      |
|                                      |
+--------------------------------------+
'''

canvas_file_clicked = '''\
+--------------------------------------+
|file  edit                            |
|+----+                                O
||open|                                |
|+----+                                |
|                                      |
|                                      |
|                                      |
|                                      |
+--------------------------------------+
'''

canvas_edit_clicked = '''\
+--------------------------------------+
|file  edit                            |
|      +-----+                         O
|      |copy |                         |
|      |paste|                         |
|      +-----+                         |
|                                      |
|                                      |
|                                      |
+--------------------------------------+
'''


class TestMenuBar(WidgetTester):

    def click_and_check(self, scene, canvas, event, clicked, expeced_canvas):
        self.clicked = 0
        self.process_mouse(scene, event)
        self.assertEqual(self.clicked, clicked)

        for effect in scene.effects:
            effect.update(0)
        self.assert_canvas_equals(canvas, expeced_canvas)

    def test_menu_bar(self):
        """
        Check PopupMenu widget works as expected.
        """

        # Simple function to test which item is selected.
        def click(x):
            self.clicked = self.clicked or x

        # Now set up the Frame ready for testing
        screen = MagicMock(spec=Screen, colours=8, unicode_aware=False)
        scene = Scene([], duration=-1)
        canvas = Canvas(screen, 10, 40, 0, 0)
        form = Frame(canvas, canvas.height, canvas.width)

        # Reset for test
        self.clicked = 0

        menus = [
            ('file', [
                ('open', lambda: click('open')),
            ]),
            ('edit', [
                ('copy', lambda: click('copy')),
                ('paste', lambda: click('paste')),
            ]),
        ]

        menu_bar = MenuBar(frame=form, menus=menus)
        form.add_layout(menu_bar)
        form.fix()
        scene.add_effect(form)
        scene.reset()

        for effect in scene.effects:
            effect.update(0)
        self.assert_canvas_equals(canvas, canvas_default)

        self.click_and_check(scene, canvas, [(1, 1, MouseEvent.LEFT_CLICK)], 0,
                             canvas_file_clicked)

        self.click_and_check(scene, canvas, [(7, 7, MouseEvent.LEFT_CLICK)], 0,
                             canvas_default)

        self.click_and_check(scene, canvas, [(1, 1, MouseEvent.LEFT_CLICK)], 0,
                             canvas_file_clicked)

        self.click_and_check(scene, canvas, [(3, 3, MouseEvent.LEFT_CLICK)],
                             'open', canvas_default)

        self.click_and_check(scene, canvas, [(8, 1, MouseEvent.LEFT_CLICK)], 0,
                             canvas_edit_clicked)

        self.click_and_check(scene, canvas, [(8, 4, MouseEvent.LEFT_CLICK)],
                             'paste', canvas_default)

        self.click_and_check(scene, canvas, [(7, 7, MouseEvent.LEFT_CLICK)], 0,
                             canvas_default)



if __name__ == '__main__':
    unittest.main()
