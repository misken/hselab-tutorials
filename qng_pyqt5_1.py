#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
qng_pyqt5_1.py - hselab PyQt5 example

A simple PyQt5 widget for exploring Erlang B and C queueing models.

Author: misken
Website: hselab.org
Last edited: August 2017
"""


import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QWidget, QSlider, QLabel,
                             QGridLayout, QVBoxLayout, QHBoxLayout,
                             QApplication)

import qng


class ErlangCalc(QWidget):
    """
    Simple Erlang B and Erlang C calculator.

    It's implemented as a Qt Widget and so we use QWidget as the base class.
    """

    def __init__(self):
        """
        Construct an ErlangCalc object.
        """

        # Call the parent class constructor.
        super().__init__() # Python3 lets us avoid super(Example, self).

        # Initialize and display the user interface
        self.initUI()

    def initUI(self):
        """
        Creates the user interface and displays it.
        """

        # Create rho slider widget and set min and max values
        self.sld_rho = QSlider(Qt.Horizontal)
        self.sld_rho.setMinimum(0)
        self.sld_rho.setMaximum(100)
        self.sld_rho.setValue(70)

        # Create server slider widget and set min and max values
        self.sld_numservers = QSlider(Qt.Horizontal)
        self.sld_numservers.setMinimum(0)
        self.sld_numservers.setMaximum(100)
        self.sld_numservers.setValue(10)

        # Create labels for sliders and their values
        rho = self.sld_rho.value() / 100
        rho_slider_val = '{:.2f}'.format(rho)
        numservers_slider_val = '{:d}'.format(self.sld_numservers.value())

        lbl_rho = QLabel("Traffic Intensity")
        self.lbl_rho_value = QLabel(rho_slider_val)

        lbl_numservers = QLabel("Number of servers")
        self.lbl_numservers_value = QLabel(numservers_slider_val)

        # Create a label and a label widget to show Erlang B and C value
        self.lbl_erlangb_value = QLabel("0.00")
        lbl_erlangb = QLabel("Erlang B")

        self.lbl_erlangc_value = QLabel("0.00")
        lbl_erlangc = QLabel("Erlang C")

        # Create grid layouts to hold the various widgets. The main layout
        # will contain the traffic and erlang grids.
        grid_main = QVBoxLayout()
        grid_traffic = QVBoxLayout()
        grid_rho = QHBoxLayout()
        grid_numservers = QHBoxLayout()
        grid_traffic.addLayout(grid_rho)
        grid_traffic.addLayout(grid_numservers)
        grid_erlang = QGridLayout()

        # Since grid_traffic and grid_erlang are not top-level layouts,
        # need to add them to parent layout before adding anything to them.
        # See http://doc.qt.io/qt-5/qgridlayout.html#details
        grid_main.addLayout(grid_traffic)
        grid_main.addLayout(grid_erlang)

        # Now add the widgets to their respective grid layouts
        grid_rho.addWidget(lbl_rho)
        grid_rho.addWidget(self.sld_rho)
        grid_rho.addWidget(self.lbl_rho_value)

        grid_numservers.addWidget(lbl_numservers)
        grid_numservers.addWidget(self.sld_numservers)
        grid_numservers.addWidget(self.lbl_numservers_value)

        # Since the erlang grid is a QGridLayout, we specify row
        # and column numbers within which to place the widgets.
        grid_erlang.addWidget(lbl_erlangb, 0, 0)
        grid_erlang.addWidget(self.lbl_erlangb_value, 0, 1)
        grid_erlang.addWidget(lbl_erlangc, 1, 0)
        grid_erlang.addWidget(self.lbl_erlangc_value, 1, 1)

        # Set the layout for the ErlangCalc widget
        self.setLayout(grid_main)

        # Hook up slider to a sliderchange function
        self.sld_rho.valueChanged.connect(self.sliderchange)
        self.sld_numservers.valueChanged.connect(self.sliderchange)

        # Position and size the widget (x, y, width, height)
        self.setGeometry(300, 300, 650, 350)
        # Set window title
        self.setWindowTitle('Erlang Calculator')
        # Display the ErlangCalc widget
        self.show()

    def sliderchange(self):
        """
        Update widget display when either slider value changes
        """
        # Compute traffic intensity based on integer slider value
        rho = self.sld_rho.value() / 100
        load = self.sld_numservers.value() * rho

        # Create formatted string to display
        rho_slider_val = '{:.2f}'.format(rho)
        numservers_slider_val = '{:d}'.format(self.sld_numservers.value())
        # Set the text property of the traffic value label
        self.lbl_rho_value.setText(rho_slider_val)
        self.lbl_numservers_value = QLabel(numservers_slider_val)

        # Compute erlang values - Erlang C only valid for rho < 1.
        erlangb = '{:0.3f}'.format(qng.erlangb(load, self.sld_numservers.value()))
        if rho < 1:
            erlangc = '{:0.3f}'.format(qng.erlangc(load, self.sld_numservers.value()))
        else:
            erlangc = 'NA'

        self.lbl_erlangb_value.setText(erlangb)
        self.lbl_erlangc_value.setText(erlangc)


if __name__ == '__main__':
    # All Qt apps need a QApplication object
    app = QApplication(sys.argv)
    # Create a new ErlangCalc widget
    ex = ErlangCalc()
    # Bail when user closes widget
    sys.exit(app.exec_())