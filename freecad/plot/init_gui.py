# SPDX-License-Identifier: LGPL-2.1-or-later


from matplotlib.pyplot import style , ion
from matplotlib import rcParams , use
from .Commands import Positions , Legend , Labels , Series , Axes , Grid  , Save
from FreeCAD import Console , Gui , Qt
from os.path import dirname , join


use('module://freecad.plot.freecad_backend')


style_list = [ 'default' , 'classic' ] + sorted(
    style for style in style.available
    if style != 'classic' and not style.startswith('_') and 'colorblind' in style
)

sorted_style_list = sorted(style_list,reverse = True)

if len(sorted_style_list) > 1:
    style.use(sorted_style_list[ 1 ])
elif len(sorted_style_list) == 1:
    style.use(sorted_style_list[ 0 ])
else:
    Console.PrintWarning(
        Qt.translate('plot_console', 'matplotlib style sheets not found') + '\n'
    )

rcParams[ 'figure.facecolor' ] = 'efefef'
rcParams[ 'axes.facecolor' ] = 'efefef'

ion()

__dir__ = dirname(__file__)


translate = Qt.translate

Workbench_Tooltip = translate('Workbench','The Plot module is used to edit/save output plots performed by other tools')
Workbench_Title = translate('Workbench','Plot')
Toolbar_Title = translate('Plot','Plot edition tools')
Menu_Title = translate('Plot','Plot')


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
            Console.PrintMessage(
                Qt.translate(
                    'plot_console', 'matplotlib not found, Plot module will be disabled'
                )
                + '\n'
            )


Gui.addWorkbench(PlotWorkbench())
