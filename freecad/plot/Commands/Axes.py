# SPDX-License-Identifier: LGPL-2.1-or-later

from ..Panels import createAxes
from FreeCAD import Qt


translate = Qt.translate

Tooltip = translate('Plot_Axes','Configure the axes parameters')
Title = translate('Plot_Axes','Configure axes')


class Axes:

    def GetResources ( self ):
        return {
            'MenuText' : Title ,
            'ToolTip' : Tooltip ,
            'Pixmap' : 'Axes'
        }

    def Activated ( self ):
        createAxes()





