# SPDX-License-Identifier: LGPL-2.1-or-later
# SPDX-FileNotice: Part of the Plot addon.

from FreeCAD.Plot import Plot # type: ignore
from PySide6 import QtWidgets , QtCore
from FreeCAD import Gui , Qt


translate = Qt.translate

Toolbar_Title = translate('Plot','Plot')

commands = [
    'Plot_SaveFig' ,
    'Plot_Axes' ,
    'Plot_Series' ,
    'Plot_Grid' ,
    'Plot_Legend' ,
    'Plot_Labels' ,
    'Plot_Positions'
]


def createToolbar ( workbench : Gui.Workbench ):

    workbench.appendToolbar(Toolbar_Title,commands)

    listenForActivation()


def getToolbar ():

    window = Gui.getMainWindow()

    widgets = window.children()

    for widget in widgets:

        if not isinstance(widget,QtWidgets.QToolBar):
            continue

        if widget.objectName() != Toolbar_Title:
            continue

        return widget

    return None


def listenForActivation ():

    def update ():

        plot = Plot.getPlot()

        active = bool( plot )

        toolbar = getToolbar()

        if toolbar :
            toolbar.setEnabled(active)


    Plot.getMdiArea().subWindowActivated.connect(update)

    QtCore.QTimer.singleShot(100,update)
