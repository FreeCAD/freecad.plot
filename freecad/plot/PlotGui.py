# SPDX-License-Identifier: LGPL-2.1-or-later

import os
import FreeCAD
import FreeCADGui

from FreeCAD import Qt

QT_TRANSLATE_NOOP = FreeCAD.Qt.QT_TRANSLATE_NOOP

FreeCADGui.addLanguagePath(
    os.path.join(os.path.dirname(__file__), 'resources', 'translations')
)
FreeCADGui.addIconPath(os.path.join(os.path.dirname(__file__), 'resources', 'icons'))


from FreeCAD.Plot import Plot
from .Panels import createPositions , createLabels , createSeries , createSave , createAxes


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

        FreeCAD.Console.PrintError(f'{ message }\n')



    def GetResources ( self ):

        tooltip = QT_TRANSLATE_NOOP('Plot_Grid','Show/Hide grid on selected plot')
        text = QT_TRANSLATE_NOOP('Plot_Grid','Show/Hide grid')

        return {
            'MenuText' : text ,
            'ToolTip' : tooltip ,
            'Pixmap' : 'Plot_Grid'
        }


class Legend:

    def Activated ( self ):

        plt = Plot.getPlot()

        if plt :

            flag = plt.isLegend()
            Plot.legend(not flag)

            return

        message = Qt.translate(
            'plot_console' ,
            'The legend must be activated on top of a plot document'
        )

        FreeCAD.Console.PrintError(f'{ message }\n')


    def GetResources ( self ):

        tooltip = QT_TRANSLATE_NOOP('Plot_Legend','Show/Hide legend on selected plot')
        text = QT_TRANSLATE_NOOP('Plot_Legend','Show/Hide legend')

        return {
            'MenuText' : text ,
            'ToolTip' : tooltip ,
            'Pixmap' : 'Plot_Legend'
        }



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


FreeCADGui.addCommand('Plot_SaveFig',Save())
FreeCADGui.addCommand('Plot_Axes',Axes())
FreeCADGui.addCommand('Plot_Series',Series())
FreeCADGui.addCommand('Plot_Grid',Grid())
FreeCADGui.addCommand('Plot_Legend',Legend())
FreeCADGui.addCommand('Plot_Labels',Labels())
FreeCADGui.addCommand('Plot_Positions',Positions())
