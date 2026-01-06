# SPDX-License-Identifier: LGPL-2.1-or-later
# SPDX-FileNotice: Part of the Plot addon.

from FreeCAD.Plot import Plot # type: ignore
from ..Panels import createLabels
from FreeCAD import Qt


translate = Qt.translate

Tooltip = translate('Plot_Labels','Set title and axes labels')
Title = translate('Plot_Labels','Set labels')


class Labels :

    def GetResources ( self ):
        return {
            'MenuText' : Title ,
            'ToolTip' : Tooltip ,
            'Pixmap' : 'Labels'
        }

    def Activated ( self ):
        createLabels()



