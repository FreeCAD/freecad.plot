# SPDX-License-Identifier: LGPL-2.1-or-later


from ..Panels import createAxes
from FreeCAD import Qt


QT_TRANSLATE_NOOP = Qt.QT_TRANSLATE_NOOP


class Axes:

    def Activated ( self ):
        createAxes()

    def GetResources ( self ):

        tooltip = QT_TRANSLATE_NOOP('Plot_Axes','Configure the axes parameters')
        text = QT_TRANSLATE_NOOP('Plot_Axes','Configure axes')

        return {
            'MenuText' : text ,
            'ToolTip' : tooltip ,
            'Pixmap' : 'Plot_Axes'
        }


