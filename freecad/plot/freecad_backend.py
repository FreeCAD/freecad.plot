# SPDX-License-Identifier: LGPL-2.1-or-later


from matplotlib.backends.backend_qt import NavigationToolbar2QT
from matplotlib._pylab_helpers import Gcf
from matplotlib.backend_bases import FigureManagerBase , FigureCanvasBase
from matplotlib.pyplot import gca
from .PySide import QtWidgets , QtCore
from FreeCAD import Gui


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

        self.mw = Gui.getMainWindow()

        self.mdi = self.mw.findChild(QtWidgets.QMdiArea)

        self.widget = PlotWidget(self)
        self.widget.setLayout(QtWidgets.QHBoxLayout())

        if self.mdi :
            self.mdi.addSubWindow(self.widget)

        layout = self.widget.layout()

        if not layout :
            return

        layout.addWidget(self.canvas) # type: ignore

        self.widget.show()

        FigureManager.all_widgets.append(self.widget)

        self.toolbar = NavigationToolbar2QT(self.canvas,self.widget,False)
        self.toolbar.setOrientation(QtCore.Qt.Orientation.Vertical)

        layout.addWidget(self.toolbar)

        self.canvas.set_widget_name = self.set_widget_name # type: ignore


    def show ( self ):
        self.canvas.draw_idle()


    def set_widget_name ( self ):

        if self.widget.windowTitle() :
            return

        title = gca().get_title()

        if title :
            self.widget.setWindowTitle(title)


    def close_foo ( self ):

        try:
            Gcf.destroy(self)
        except AttributeError:
            pass


class FigureCanvas ( FigureCanvasBase ):

    def draw_idle ( self ):

        super().draw_idle()

        self.set_widget_name()


    def set_widget_name ( self ):
        pass
