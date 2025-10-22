# SPDX-License-Identifier: LGPL-2.1-or-later

import os
import FreeCAD
import FreeCADGui

QT_TRANSLATE_NOOP = FreeCAD.Qt.QT_TRANSLATE_NOOP

FreeCADGui.addLanguagePath(
    os.path.join(os.path.dirname(__file__), "resources", "translations")
)
FreeCADGui.addIconPath(os.path.join(os.path.dirname(__file__), "resources", "icons"))


class Save:
    def Activated(self):
        from freecad.plot import plotSave

        plotSave.load()

    def GetResources(self):
        MenuText = QT_TRANSLATE_NOOP("Plot_SaveFig", "Save plot")
        ToolTip = QT_TRANSLATE_NOOP("Plot_SaveFig", "Save the plot as an image file")
        return {"Pixmap": "Plot_Save", "MenuText": MenuText, "ToolTip": ToolTip}


class Axes:
    def Activated(self):
        from freecad.plot import plotAxes

        plotAxes.load()

    def GetResources(self):
        MenuText = QT_TRANSLATE_NOOP("Plot_Axes", "Configure axes")
        ToolTip = QT_TRANSLATE_NOOP("Plot_Axes", "Configure the axes parameters")
        return {"Pixmap": "Plot_Axes", "MenuText": MenuText, "ToolTip": ToolTip}


class Series:
    def Activated(self):
        from freecad.plot import plotSeries

        plotSeries.load()

    def GetResources(self):
        MenuText = QT_TRANSLATE_NOOP("Plot_Series", "Configure series")
        ToolTip = QT_TRANSLATE_NOOP(
            "Plot_Series", "Configure series drawing style and label"
        )
        return {"Pixmap": "Plot_Series", "MenuText": MenuText, "ToolTip": ToolTip}


class Grid:
    def Activated(self):
        from FreeCAD.Plot import Plot

        plt = Plot.getPlot()
        if not plt:
            msg = App.Qt.translate(
                "plot_console",
                "The grid must be activated on top of a plot document",
                None,
            )
            FreeCAD.Console.PrintError(msg + "\n")
            return
        flag = plt.isGrid()
        Plot.grid(not flag)

    def GetResources(self):
        MenuText = QT_TRANSLATE_NOOP("Plot_Grid", "Show/Hide grid")
        ToolTip = QT_TRANSLATE_NOOP("Plot_Grid", "Show/Hide grid on selected plot")
        return {"Pixmap": "Plot_Grid", "MenuText": MenuText, "ToolTip": ToolTip}


class Legend:
    def Activated(self):
        from FreeCAD.Plot import Plot

        plt = Plot.getPlot()
        if not plt:
            msg = App.Qt.translate(
                "plot_console",
                "The legend must be activated on top of a plot document",
                None,
            )
            FreeCAD.Console.PrintError(msg + "\n")
            return
        flag = plt.isLegend()
        Plot.legend(not flag)

    def GetResources(self):
        MenuText = QT_TRANSLATE_NOOP("Plot_Legend", "Show/Hide legend")
        ToolTip = QT_TRANSLATE_NOOP("Plot_Legend", "Show/Hide legend on selected plot")
        return {"Pixmap": "Plot_Legend", "MenuText": MenuText, "ToolTip": ToolTip}


class Labels:
    def Activated(self):
        from freecad.plot import plotLabels

        plotLabels.load()

    def GetResources(self):
        MenuText = QT_TRANSLATE_NOOP("Plot_Labels", "Set labels")
        ToolTip = QT_TRANSLATE_NOOP("Plot_Labels", "Set title and axes labels")
        return {"Pixmap": "Plot_Labels", "MenuText": MenuText, "ToolTip": ToolTip}


class Positions:
    def Activated(self):
        from freecad.plot import plotPositions

        plotPositions.load()

    def GetResources(self):
        MenuText = QT_TRANSLATE_NOOP("Plot_Positions", "Set positions and sizes")
        ToolTip = QT_TRANSLATE_NOOP(
            "Plot_Positions", "Set labels and legend positions and sizes"
        )
        return {"Pixmap": "Plot_Positions", "MenuText": MenuText, "ToolTip": ToolTip}


FreeCADGui.addCommand("Plot_SaveFig", Save())
FreeCADGui.addCommand("Plot_Axes", Axes())
FreeCADGui.addCommand("Plot_Series", Series())
FreeCADGui.addCommand("Plot_Grid", Grid())
FreeCADGui.addCommand("Plot_Legend", Legend())
FreeCADGui.addCommand("Plot_Labels", Labels())
FreeCADGui.addCommand("Plot_Positions", Positions())
