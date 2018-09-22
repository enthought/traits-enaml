import unittest

import pandas

from traits_enaml.widgets.data_frame_table import QDataFrameTableView
from traits_enaml.testing.gui_test_assistant import GuiTestAssistant


class TestQDataFrameTableWidget(GuiTestAssistant, unittest.TestCase):

    def setUp(self):
        GuiTestAssistant.setUp(self)
        self.data_frame = pandas.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]})

    def tearDown(self):
        self.data_frame = None
        GuiTestAssistant.tearDown(self)

    def test_show(self):
        widget = QDataFrameTableView.from_data_frame(self.data_frame)
        with self.event_loop():
            widget.show()
        with self.delete_widget(widget):
            widget.deleteLater()


if __name__ == "__main__":
    unittest.main()
