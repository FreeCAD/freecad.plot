# SPDX-License-Identifier: LGPL-2.1-or-later


from ..Panels import createPositions
from FreeCAD import Qt

QT_TRANSLATE_NOOP = Qt.QT_TRANSLATE_NOOP


class Positions :

    def Activated ( self ):
        createPositions()

    def GetResources ( self ):

        tooltip = QT_TRANSLATE_NOOP('Plot_Positions','Set labels and legend positions and sizes')
        text = QT_TRANSLATE_NOOP('Plot_Positions','Set positions and sizes')

        return {
            'MenuText' : text ,
            'ToolTip' : tooltip ,
            'Pixmap' : 'Plot_Positions'
        }

