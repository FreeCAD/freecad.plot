# SPDX-License-Identifier: LGPL-2.1-or-later


from FreeCAD.Plot import Plot
from FreeCAD import Console , Qt


QT_TRANSLATE_NOOP = Qt.QT_TRANSLATE_NOOP


class Grid:

    def Activated ( self ):

        plt = Plot.getPlot()

        if plt:

            flag = plt.isGrid()
            Plot.grid(not flag)
            return

        message = Qt.translate(
            'plot_console',
            'The grid must be activated on top of a plot document'
        )

        Console.PrintError(f'{ message }\n')



    def GetResources ( self ):

        tooltip = QT_TRANSLATE_NOOP('Plot_Grid','Show/Hide grid on selected plot')
        text = QT_TRANSLATE_NOOP('Plot_Grid','Show/Hide grid')

        return {
            'MenuText' : text ,
            'ToolTip' : tooltip ,
            'Pixmap' : 'Plot_Grid'
        }

