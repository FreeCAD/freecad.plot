# SPDX-License-Identifier: LGPL-2.1-or-later
# SPDX-FileNotice: Part of the Plot addon.

from .Commands import Positions , Legend , Labels , Series , Axes , Grid  , Save
from .Toolbar import createToolbar
from FreeCAD import Console , Gui , Qt
from os.path import dirname , join


__dir__ = dirname(__file__)


translate = Qt.translate

Workbench_Tooltip = translate('Workbench','The Plot module is used to edit/save output plots performed by other tools')
Workbench_Title = translate('Workbench','Plot')


class PlotWorkbench ( Gui.Workbench ):

    MenuText = Workbench_Title
    ToolTip = Workbench_Tooltip

    Icon = join(__dir__, 'Resources', 'Icons', 'Addon.svg')


    def __init__ ( self ):

        Gui.addLanguagePath(join(__dir__, 'Resources', 'Locales'))
        Gui.updateLocale()

        Gui.addIconPath(join(__dir__, 'Resources', 'Icons'))

        Gui.addCommand('Plot_SaveFig',Save())
        Gui.addCommand('Plot_Axes',Axes())
        Gui.addCommand('Plot_Series',Series())
        Gui.addCommand('Plot_Grid',Grid())
        Gui.addCommand('Plot_Legend',Legend())
        Gui.addCommand('Plot_Labels',Labels())
        Gui.addCommand('Plot_Positions',Positions())


    def Initialize ( self ):

        try:
            import matplotlib
        except ImportError:
            Console.PrintMessage(
                Qt.translate(
                    'plot_console', 'matplotlib not found, Plot module will be disabled'
                )
                + '\n'
            )

        createToolbar(self)

