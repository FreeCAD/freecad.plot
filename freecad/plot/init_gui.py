# SPDX-License-Identifier: LGPL-2.1-or-later

import FreeCAD
import FreeCADGui as Gui
import os, sys

import matplotlib

# Force matplotlib to use PySide backend by temporarily unloading PyQt
PyQt5WasLoaded = False
if 'PyQt5.QtCore' in sys.modules:
    del sys.modules['PyQt5.QtCore']
    PyQt5WasLoaded = True

import matplotlib.pyplot as plt

if PyQt5WasLoaded:
    import PyQt5.QtCore

matplotlib.use("module://freecad.plot.freecad_backend")
style_list = ['default', 'classic'] + sorted(
    style for style in plt.style.available
    if style != 'classic' and not style.startswith('_') and 'colorblind' in style)
sorted_style_list = sorted(style_list, reverse = True)
if len(sorted_style_list) > 1:
    matplotlib.style.use(sorted_style_list[1])
elif len(sorted_style_list) == 1:
    matplotlib.style.use(sorted_style_list[0])
else:
    FreeCAD.Console.PrintWarning(
        FreeCAD.Qt.translate("plot_console", "matplotlib style sheets not found") + "\n"
    )
matplotlib.rcParams["figure.facecolor"] = "efefef"
matplotlib.rcParams["axes.facecolor"] = "efefef"

plt.ion()

__dir__ = os.path.dirname(__file__)


class PlotWorkbench(Gui.Workbench):
    """Workbench of Plot module."""

    def __init__(self):
        Gui.addLanguagePath(os.path.join(__dir__, "resources", "translations"))
        Gui.updateLocale()
        self.__class__.Icon = os.path.join(
            __dir__, "resources", "icons", "Plot_Workbench.svg"
        )
        self.__class__.MenuText = FreeCAD.Qt.translate("Workbench", "Plot")
        self.__class__.ToolTip = FreeCAD.Qt.translate(
            "Workbench",
            "The Plot module is used to edit/save output plots performed by other tools",
        )

    import freecad.plot.PlotGui

    def Initialize(self):
        cmdlst = ["Plot_SaveFig",
                  "Plot_Axes",
                  "Plot_Series",
                  "Plot_Grid",
                  "Plot_Legend",
                  "Plot_Labels",
                  "Plot_Positions"]
        QT_TRANSLATE_NOOP = FreeCAD.Qt.QT_TRANSLATE_NOOP

        self.appendToolbar(QT_TRANSLATE_NOOP("Plot", "Plot edition tools"), cmdlst)
        self.appendMenu(QT_TRANSLATE_NOOP("Plot", "Plot"), cmdlst)
        try:
            import matplotlib
        except ImportError:
            FreeCAD.Console.PrintMessage(
                FreeCAD.Qt.translate(
                    "plot_console", "matplotlib not found, Plot module will be disabled"
                )
                + "\n"
            )


Gui.addWorkbench(PlotWorkbench())
