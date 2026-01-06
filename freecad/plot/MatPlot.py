# SPDX-License-Identifier: LGPL-2.1-or-later
# SPDX-FileNotice: Part of the Plot addon.

from matplotlib.pyplot import style , ion
from matplotlib import rcParams , use
from FreeCAD import Console , Qt


def initMatPlot ():

    use('module://freecad.plot.Backend')


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
