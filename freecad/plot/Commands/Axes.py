# SPDX-License-Identifier: LGPL-2.1-or-later

from FreeCAD.Plot import Plot # type: ignore
from ..Panels import createAxes
from FreeCAD import Qt


translate = Qt.translate

Tooltip = translate('Plot_Axes','Configure the axes parameters')
Title = translate('Plot_Axes','Configure axes')


class Axes :

    def GetResources ( self ):
        return {
            'MenuText' : Title ,
            'ToolTip' : Tooltip ,
            'Pixmap' : 'Axes'
        }

    def IsActive ( self ):
        return bool( Plot.getPlot() )

    def Activated ( self ):
        createAxes()





