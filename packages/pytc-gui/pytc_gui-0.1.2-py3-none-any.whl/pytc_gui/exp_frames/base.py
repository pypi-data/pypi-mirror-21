from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

import pytc
import inspect

class Experiments(QWidget):
    """
    Experiment box widget
    """

    def __init__(self, name, parent):

        super().__init__()

        self._name = name
        self._fitter = parent._fitter
        self._slider_list = parent._slider_list
        self._global_var = parent._global_var
        self._global_tracker = parent._global_tracker
        self._connectors_seen = parent._connectors_seen
        self._global_connectors = parent._global_connectors
        self._plot_frame = parent._plot_frame

        self.layout()

    @property
    def name(self):
        """
        """
        return self._name

    def layout(self):
        """
        """
        self._main_layout = QVBoxLayout(self)
        self._header_layout = QHBoxLayout()

        # Construct the header for the experiment
        self._name_label = QLabel(self._name)

        # Button to hide and show advanced options for the experiment
        self._show_options_button = QPushButton("Show Sliders", self)
        self._show_options_button.clicked.connect(self.slider_popup)

        # Button to remove experiment
        self._remove_name = "Remove"
        self.exp_widgets()
        
        self._remove_button = QPushButton(self._remove_name, self)
        self._remove_button.clicked.connect(self.remove)

        # add exp name, remove and show sliders buttons to layout
        self._header_layout.addWidget(self._name_label)
        self._header_layout.addStretch(1)
        self._header_layout.addWidget(self._show_options_button)
        self._header_layout.addWidget(self._remove_button)
        self._header_layout.addStretch(2)

        self._main_layout.addLayout(self._header_layout)

        # Create empty box for any required parameters
        self._req_box = QFrame()
        self._req_layout = QVBoxLayout()
        self._req_box.setLayout(self._req_layout)
        self._main_layout.addWidget(self._req_box)

        # Create divider    
        self._divider = QFrame()
        self._divider.setFrameShape(QFrame.HLine)
        self._main_layout.addWidget(self._divider)

        self.setFixedHeight(110)

    def exp_widgets(self):
        """
        for changing local/global specific items
        """
        pass

    def remove(self):
        """
        """
        pass

    def slider_popup(self):
        """
        show window containing sliders
        """
        pass

            