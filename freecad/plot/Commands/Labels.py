# SPDX-License-Identifier: LGPL-2.1-or-later


from ..Panels import createLabels
from FreeCAD import Qt


QT_TRANSLATE_NOOP = Qt.QT_TRANSLATE_NOOP


class Labels:

    def Activated ( self ):
        createLabels()

    def GetResources ( self ):

        tooltip = QT_TRANSLATE_NOOP('Plot_Labels','Set title and axes labels')
        text = QT_TRANSLATE_NOOP('Plot_Labels','Set labels')

        return {
            'MenuText' : text ,
            'ToolTip' : tooltip ,
            'Pixmap' : 'Plot_Labels'
        }

