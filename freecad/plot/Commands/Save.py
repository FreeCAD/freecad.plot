# SPDX-License-Identifier: LGPL-2.1-or-later


from ..Panels import createSave
from FreeCAD import Qt


QT_TRANSLATE_NOOP = Qt.QT_TRANSLATE_NOOP


class Save :

    def Activated ( self ):
        createSave()

    def GetResources ( self ):

        tooltip = QT_TRANSLATE_NOOP('Plot_SaveFig','Save the plot as an image file')
        text = QT_TRANSLATE_NOOP('Plot_SaveFig','Save plot')

        return {
            'MenuText' : text ,
            'ToolTip' : tooltip ,
            'Pixmap' : 'Plot_Save'
        }
