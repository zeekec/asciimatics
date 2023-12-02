from datetime import date
import unittest

from asciimatics.event import KeyboardEvent, MouseEvent


class WidgetTester(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None
        self.epoch_date = str(date.fromtimestamp(0))

    def _canvas_to_string(self, canvas):
        output = ""
        for y in range(canvas.height):
            for x in range(canvas.width):
                char, _, _, _ = canvas.get_from(x, y)
                output += chr(char)
            output += "\n"
        return output

    def assert_canvas_equals(self, canvas, expected):
        """
        Assert output to canvas is as expected.
        """
        output = self._canvas_to_string(canvas)
        self.assertEqual(output, expected)

    @staticmethod
    def process_keys(form, values, separator=None):
        """
        Inject a set of key events separated by a common key separator.
        """
        for new_value in values:
            if isinstance(new_value, int):
                form.process_event(KeyboardEvent(new_value))
            else:
                for char in new_value:
                    form.process_event(KeyboardEvent(ord(char)))
            if separator:
                form.process_event(KeyboardEvent(separator))

    @staticmethod
    def process_mouse(form, values):
        """
        Inject a set of mouse events.
        """
        for x, y, buttons in values:
            form.process_event(MouseEvent(x, y, buttons))
