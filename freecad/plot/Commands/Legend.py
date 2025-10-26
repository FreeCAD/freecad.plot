# SPDX-License-Identifier: LGPL-2.1-or-later

from FreeCAD.Plot import Plot # type: ignore
from FreeCAD import Console , Qt


translate = Qt.translate

Tooltip = translate('Plot_Legend','Show/Hide legend on selected plot')
Title = translate('Plot_Legend','Show/Hide legend')


class Legend:

    def GetResources ( self ):
        return {
            'MenuText' : Title ,
            'ToolTip' : Tooltip ,
            'Pixmap' : 'Legend'
        }

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