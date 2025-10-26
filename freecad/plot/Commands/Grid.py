# SPDX-License-Identifier: LGPL-2.1-or-later

from FreeCAD.Plot import Plot # type: ignore
from FreeCAD import Console , Qt


translate = Qt.translate

Tooltip = translate('Plot_Grid','Show/Hide grid on selected plot')
Title = translate('Plot_Grid','Show/Hide grid')



class Grid:

    def GetResources ( self ):
        return {
            'MenuText' : Title ,
            'ToolTip' : Tooltip ,
            'Pixmap' : 'Grid'
        }

    def Activated ( self ):

        plot = Plot.getPlot()

        if plot :

            isGrid = plot.isGrid()
            Plot.grid(not isGrid)
            return

        message = Qt.translate(
            'plot_console',
            'The grid must be activated on top of a plot document'
        )

        Console.PrintError(f'{ message }\n')
