# SPDX-License-Identifier: LGPL-2.1-or-later

from ..Panels import createSave
from FreeCAD import Qt


translate = Qt.translate

Tooltip = translate('Plot_SaveFig','Save the plot as an image file')
Title = translate('Plot_SaveFig','Save plot')


class Save :

    def GetResources ( self ):
        return {
            'MenuText' : Title ,
            'ToolTip' : Tooltip ,
            'Pixmap' : 'Save'
        }

    def Activated ( self ):
        createSave()