# SPDX-License-Identifier: LGPL-2.1-or-later

import os

from FreeCAD.Plot import Plot # type: ignore
from ..PySide import QtWidgets
from FreeCAD import Console , Gui , Qt
from re import search


class TaskForm ( QtWidgets.QWidget ):

    pathButton : QtWidgets.QPushButton
    sizeLabel : QtWidgets.QLabel
    dpiLabel : QtWidgets.QLabel
    sizeX : QtWidgets.QDoubleSpinBox
    sizeY : QtWidgets.QDoubleSpinBox
    path : QtWidgets.QLineEdit
    dpi : QtWidgets.QSpinBox


class TaskPanel:

    form : TaskForm
    name : str = 'plot save'

    def __init__ ( self ):

        path = os.path.join(os.path.dirname(__file__),
                               '../Resources/Interface/',
                               'Save.ui')

        form = Gui.PySideUic.loadUi(path) # type: ignore

        self.form = form


    def accept ( self ):

        plot = Plot.getPlot()

        if plot :

            form = self.form

            size = (
                form.sizeX.value() ,
                form.sizeY.value()
            )

            path = form.path.text()
            dpi = form.dpi.value()

            Plot.save(path,size,dpi)

            return True

        message = Qt.translate(
            'plot_console' ,
            'Plot document must be selected in order to save it'
        )

        Console.PrintError(f'{ message }\n')

        return False


    def isAllowedAlterSelection ( self ):
        return False

    def isAllowedAlterDocument ( self ):
        return False

    def isAllowedAlterView ( self ):
        return True

    def needsFullSpace ( self ):
        return True

    def helpRequested ( self ):
        pass

    def clicked ( self , index ):
        pass

    def reject ( self ):
        return True

    def open ( self ):
        self.setupUi()


    def setupUi ( self ):

        self.retranslateUi()

        home = os.getenv('USERPROFILE') or os.getenv('HOME')

        if not home:
            Console.PrintWarning('No home user / home directory found.')
            return

        form = self.form

        form.path.setText(os.path.join(home,'plot.png'))

        self.updateUI()

        form.pathButton.pressed.connect(self.onPathButton)

        Plot.getMdiArea().subWindowActivated.connect(self.onMdiArea)


    def retranslateUi ( self ):

        '''
        Set the user interface locale strings.
        '''

        form = self.form

        form.setWindowTitle(
            Qt.translate(
                'plot_save',
                'Save figure'
            ))

        form.sizeLabel.setText(
            Qt.translate(
                'plot_save',
                'Inches'
            ))

        form.dpiLabel.setText(
            Qt.translate(
                'plot_save',
                'Dots per Inch'
            ))

        form.path.setToolTip(
            Qt.translate(
                'plot_save',
                'Output image file path'
            ))

        form.pathButton.setToolTip(
            Qt.translate(
                'plot_save',
                'Show a file selection dialog'
            ))

        form.sizeX.setToolTip(
            Qt.translate(
                'plot_save',
                'X image size'
            ))

        form.sizeY.setToolTip(
            Qt.translate(
                'plot_save',
                'Y image size'
            ))

        form.dpi.setToolTip(
            Qt.translate(
                'plot_save',
                'Dots per point,with size will define output image'
                ' resolution'
            ))


    def updateUI ( self ):

        '''
        Setup UI controls values if possible
        '''

        plot = Plot.getPlot()

        enabled = bool(plot)

        form = self.form

        form.pathButton.setEnabled(enabled)
        form.sizeX.setEnabled(enabled)
        form.sizeY.setEnabled(enabled)
        form.path.setEnabled(enabled)
        form.dpi.setEnabled(enabled)

        if not plot:
            return

        figure = plot.fig

        size = figure.get_size_inches()
        dpi = figure.get_dpi()

        form.sizeX.setValue(size[ 0 ])
        form.sizeY.setValue(size[ 1 ])
        form.dpi.setValue(dpi)


    def onPathButton ( self ):

        '''
        Executed when the path selection button is pressed.
        '''

        form = self.form

        path = form.path.text()

        formats = [
            'Portable Network Graphics (*.png)' ,
            'Portable Document Format (*.pdf)' ,
            'Encapsulated PostScript (*.eps)' ,
            'PostScript (*.ps)'
        ]

        filters = str.join(';;',formats)

        [ path , format ] = QtWidgets.QFileDialog.getSaveFileName \
            (None,'Save figure',path,filters)

        print('Save Path',path)

        if path == '' :
            return

        [ root , extension ] = os.path.splitext(path)

        if extension == '' :

            match = search(r'(?<=\*\.)\w+',format)

            if match:

                extension = match.group(0)

                path = f'{ path }{ os.path.extsep }{ extension }'

        print('Path',path,extension)

        form.path.setText(path)


    def onMdiArea ( self , subWin ):

        '''
        Executed when a new window is selected on the mdi area.

        Keyword arguments:
        subWin -- Selected window.
        '''

        plot = Plot.getPlot()

        if plot != subWin :
            self.updateUI()


def createTask():

    panel = TaskPanel()

    Gui.Control.showDialog(panel)
