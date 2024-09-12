from PySide import QtCore, QtWidgets

import FreeCADGui

import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backend_bases import FigureManagerBase
from matplotlib.backends.backend_qt5agg import FigureCanvas as FigCan
from matplotlib.backends.backend_qt5agg import FigureManager as FigMan
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT, ToolbarQt
from matplotlib import backend_tools, cbook
from matplotlib._pylab_helpers import Gcf


class PlotWidget(QtWidgets.QWidget):
    def __init__(self, manager, close_foo=None):
        super(PlotWidget, self).__init__(manager.mdi)
        self.manager = manager
        self.close_foo = close_foo

    def closeEvent(self, *args):
        self.manager.close_foo()
        super(PlotWidget, self).closeEvent(*args)


class FigureManager(FigureManagerBase):
    all_widgets = []
    def __init__(self, canvas, num):
        super().__init__(canvas, num)
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

class FigureCanvas(FigCan):
    def draw_idle(self):
        super().draw_idle()
        if hasattr(self, "set_widget_name"):
            self.set_widget_name()
