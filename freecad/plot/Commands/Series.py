# SPDX-License-Identifier: LGPL-2.1-or-later


from ..Panels import createSeries
from FreeCAD import Qt


QT_TRANSLATE_NOOP = Qt.QT_TRANSLATE_NOOP


class Series:

    def Activated ( self ):
        createSeries()

    def GetResources ( self ):

        tooltip = QT_TRANSLATE_NOOP('Plot_Series','Configure series drawing style and label')
        text = QT_TRANSLATE_NOOP('Plot_Series','Configure series')

        return {
            'MenuText' : text ,
            'ToolTip' : tooltip ,
            'Pixmap' : 'Plot_Series'
        }