# SPDX-License-Identifier: LGPL-2.1-or-later

from ..Panels import createSeries
from FreeCAD import Qt


translate = Qt.translate

Tooltip = translate('Plot_Series','Configure series drawing style and label')
Title = translate('Plot_Series','Configure series')


class Series :

    def GetResources ( self ):
        return {
            'MenuText' : Title ,
            'ToolTip' : Tooltip ,
            'Pixmap' : 'Series'
        }

    def Activated ( self ):
        createSeries()
