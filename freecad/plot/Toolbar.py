# SPDX-License-Identifier: LGPL-2.1-or-later

from FreeCAD import Gui , Qt


translate = Qt.translate

Toolbar_Title = translate('Plot','Plot edition tools')
Menu_Title = translate('Plot','Plot')

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
    workbench.appendMenu(Menu_Title,commands)
