# SPDX-License-Identifier: LGPL-2.1-or-later
# SPDX-FileNotice: Part of the Plot addon.

from .Workbench import PlotWorkbench
from .MatPlot import initMatPlot
from FreeCAD import Gui


initMatPlot()

Gui.addWorkbench(PlotWorkbench())
