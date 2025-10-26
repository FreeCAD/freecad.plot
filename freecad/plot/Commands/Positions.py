# SPDX-License-Identifier: LGPL-2.1-or-later

from FreeCAD.Plot import Plot # type: ignore
from ..Panels import createPositions
from FreeCAD import Qt


translate = Qt.translate

Tooltip = translate('Plot_Positions','Set labels and legend positions and sizes')
Title = translate('Plot_Positions','Set positions and sizes')


class Positions :

    def GetResources ( self ):
        return {
            'MenuText' : Title ,
            'ToolTip' : Tooltip ,
            'Pixmap' : 'Positions'
        }

    def IsActive ( self ):
        return bool( Plot.getPlot() )

    def Activated ( self ):
        createPositions()