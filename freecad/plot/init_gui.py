# SPDX-License-Identifier: LGPL-2.1-or-later

import FreeCAD
import FreeCADGui as Gui
import os

import matplotlib

import matplotlib.pyplot as plt
from matplotlib import style
from .Commands import Positions , Legend , Labels , Series , Axes , Grid  , Save

matplotlib.use('module://freecad.plot.freecad_backend')

style_list = [ 'default' , 'classic' ] + sorted(
    style for style in plt.style.available
    if style != 'classic' and not style.startswith('_') and 'colorblind' in style
)

sorted_style_list = sorted(style_list,reverse = True)

if len(sorted_style_list) > 1:
    style.use(sorted_style_list[ 1 ])
elif len(sorted_style_list) == 1:
    style.use(sorted_style_list[ 0 ])
else:
    FreeCAD.Console.PrintWarning(
        FreeCAD.Qt.translate('plot_console', 'matplotlib style sheets not found') + '\n'
    )

matplotlib.rcParams[ 'figure.facecolor' ] = 'efefef'
matplotlib.rcParams[ 'axes.facecolor' ] = 'efefef'

plt.ion()

__dir__ = os.path.dirname(__file__)


QT_TRANSLATE_NOOP = FreeCAD.Qt.QT_TRANSLATE_NOOP


Workbench_Tooltip = QT_TRANSLATE_NOOP('Workbench','The Plot module is used to edit/save output plots performed by other tools')
Workbench_Title = QT_TRANSLATE_NOOP('Workbench','Plot')
Toolbar_Title = QT_TRANSLATE_NOOP('Plot','Plot edition tools')
Menu_Title = QT_TRANSLATE_NOOP('Plot','Plot')


class PlotWorkbench ( Gui.Workbench ):

    MenuText = Workbench_Title
    ToolTip = Workbench_Tooltip
    Icon = os.path.join(__dir__, 'resources', 'icons', 'Plot_Workbench.svg')

    def __init__ ( self ):

        Gui.addLanguagePath(os.path.join(__dir__, 'Resources', 'Locales'))
        Gui.updateLocale()

        Gui.addIconPath(os.path.join(__dir__, 'resources', 'icons'))

        Gui.addCommand('Plot_SaveFig',Save())
        Gui.addCommand('Plot_Axes',Axes())
        Gui.addCommand('Plot_Series',Series())
        Gui.addCommand('Plot_Grid',Grid())
        Gui.addCommand('Plot_Legend',Legend())
        Gui.addCommand('Plot_Labels',Labels())
        Gui.addCommand('Plot_Positions',Positions())


    def Initialize ( self ):

        commands = [
            'Plot_SaveFig' ,
            'Plot_Axes' ,
            'Plot_Series' ,
            'Plot_Grid' ,
            'Plot_Legend' ,
            'Plot_Labels' ,
            'Plot_Positions'
        ]

        self.appendToolbar(Toolbar_Title,commands)
        self.appendMenu(Menu_Title,commands)

        try:
            import matplotlib
        except ImportError:
            FreeCAD.Console.PrintMessage(
                FreeCAD.Qt.translate(
                    'plot_console', 'matplotlib not found, Plot module will be disabled'
                )
                + '\n'
            )


Gui.addWorkbench(PlotWorkbench())
