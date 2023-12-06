#***************************************************************************
#*                                                                         *
#*   Copyright (c) 2011, 2012                                              *
#*   Jose Luis Cercos Pita <jlcercos@gmail.com>                            *
#*                                                                         *
#*   This program is free software; you can redistribute it and/or modify  *
#*   it under the terms of the GNU Lesser General Public License (LGPL)    *
#*   as published by the Free Software Foundation; either version 2 of     *
#*   the License, or (at your option) any later version.                   *
#*   for detail see the LICENCE text file.                                 *
#*                                                                         *
#*   This program is distributed in the hope that it will be useful,       *
#*   but WITHOUT ANY WARRANTY; without even the implied warranty of        *
#*   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         *
#*   GNU Library General Public License for more details.                  *
#*                                                                         *
#*   You should have received a copy of the GNU Library General Public     *
#*   License along with this program; if not, write to the Free Software   *
#*   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  *
#*   USA                                                                   *
#*                                                                         *
#***************************************************************************

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
    from PySide import QtCore, QtGui
    msg = QtGui.QApplication.translate(
        "plot_console",
        "matplotlib style sheets not found",
        None)
    FreeCAD.Console.PrintWarning(msg + '\n')
matplotlib.rcParams["figure.facecolor"] = "efefef"
matplotlib.rcParams["axes.facecolor"] = "efefef"

plt.ion()

__dir__ = os.path.dirname(__file__)

class PlotWorkbench(Gui.Workbench):
    """Workbench of Plot module."""
    def __init__(self):
        self.__class__.Icon = os.path.join(__dir__, "resources", "icons", "Plot_Workbench.svg")
        self.__class__.MenuText = "Plot"
        self.__class__.ToolTip = "The Plot module is used to edit/save output plots performed by other tools"

    import freecad.plot.PlotGui

    def Initialize(self):
        from PySide import QtCore, QtGui
        cmdlst = ["Plot_SaveFig",
                  "Plot_Axes",
                  "Plot_Series",
                  "Plot_Grid",
                  "Plot_Legend",
                  "Plot_Labels",
                  "Plot_Positions"]
        self.appendToolbar(str(QtCore.QT_TRANSLATE_NOOP(
            "Plot",
            "Plot edition tools")), cmdlst)
        self.appendMenu(str(QtCore.QT_TRANSLATE_NOOP(
            "Plot",
            "Plot")), cmdlst)
        try:
            import matplotlib
        except ImportError:
            from PySide import QtCore, QtGui
            msg = QtGui.QApplication.translate(
                "plot_console",
                "matplotlib not found, Plot module will be disabled",
                None)
            FreeCAD.Console.PrintMessage(msg + '\n')


Gui.addWorkbench(PlotWorkbench())
