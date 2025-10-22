# SPDX-License-Identifier: LGPL-2.1-or-later

from .PySide import QtWidgets , QtCore

import FreeCADGui

import matplotlib.pyplot as plt

from matplotlib.backends.backend_qt import NavigationToolbar2QT
from matplotlib._pylab_helpers import Gcf
from matplotlib.backend_bases import FigureManagerBase , FigureCanvasBase


class PlotWidget ( QtWidgets.QWidget ):

    def __init__ ( self , manager , close_foo = None ):

        super(PlotWidget,self).__init__(manager.mdi)

        self.close_foo = close_foo
        self.manager = manager

    def closeEvent ( self , * args ):

        self.manager.close_foo()

        super(PlotWidget,self).closeEvent( * args )


class FigureManager ( FigureManagerBase ):

    all_widgets = []

    def __init__ ( self , canvas , num ):

        super().__init__(canvas,num)

        self.mw = FreeCADGui.getMainWindow()
        self.mdi = self.mw.findChild(QtWidgets.QMdiArea)
        self.widget = PlotWidget(self)
        self.widget.setLayout(QtWidgets.QHBoxLayout())
        self.mdi.addSubWindow(self.widget)
        self.widget.layout().addWidget(self.canvas)
        self.widget.show()

        FigureManager.all_widgets.append(self.widget)

        self.toolbar = NavigationToolbar2QT(self.canvas, self.widget, False)
        self.toolbar.setOrientation(QtCore.Qt.Vertical)
        self.widget.layout().addWidget(self.toolbar)
        self.canvas.set_widget_name = self.set_widget_name

    def show(self):
        self.canvas.draw_idle()

    def set_widget_name(self):
        if not self.widget.windowTitle() and plt.gca().get_title():
            self.widget.setWindowTitle(plt.gca().get_title())

    def close_foo(self):
        try:
            Gcf.destroy(self)
        except AttributeError:
            pass

class FigureCanvas ( FigureCanvasBase ):

    def draw_idle(self):

        super().draw_idle()

        # if hasattr(self,'set_widget_name'):
        #     self.set_widget_name()
