# SPDX-License-Identifier: LGPL-2.1-or-later


from FreeCAD.Plot import Plot # type: ignore
from FreeCAD import Console , Qt


QT_TRANSLATE_NOOP = Qt.QT_TRANSLATE_NOOP


class Legend:

    def Activated ( self ):

        plot = Plot.getPlot()

        if plot :
            isLegend = plot.isLegend()
            Plot.legend(not isLegend)
            return

        message = Qt.translate(
            'plot_console' ,
            'The legend must be activated on top of a plot document'
        )

        Console.PrintError(f'{ message }\n')


    def GetResources ( self ):

        tooltip = QT_TRANSLATE_NOOP('Plot_Legend','Show/Hide legend on selected plot')
        text = QT_TRANSLATE_NOOP('Plot_Legend','Show/Hide legend')

        return {
            'MenuText' : text ,
            'ToolTip' : tooltip ,
            'Pixmap' : 'Legend'
        }
