# SPDX-License-Identifier: LGPL-2.1-or-later


from FreeCAD.Plot import Plot # type: ignore
from ..PySide import QtWidgets
from os.path import splitext , dirname , extsep , join
from FreeCAD import Console , Gui , Qt
from os import getenv
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

        path = join(
            dirname(__file__) , '..' ,
            'Resources' , 'Interface' , 'Save.ui'
        )

        self.form = Gui.PySideUic.loadUi(path) # type: ignore


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

    def getStandardButtons ( self ):
        return QtWidgets.QDialogButtonBox.StandardButton.Save | QtWidgets.QDialogButtonBox.StandardButton.Cancel

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

        home = getenv('USERPROFILE') or getenv('HOME')

        if not home:
            Console.PrintWarning('No home user / home directory found.')
            return

        path = join(home,'Plot.png')

        form = self.form

        form.path.setText(path)

        self.updateUI()

        form.pathButton.pressed.connect(self.onPathButton)

        Plot.getMdiArea().subWindowActivated.connect(self.onMdiArea)


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

        [ root , extension ] = splitext(path)

        if extension == '' :

            match = search(r'(?<=\*\.)\w+',format)

            if match:

                extension = match.group(0)

                path = f'{ path }{ extsep }{ extension }'

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


def createTask ():

    panel = TaskPanel()

    Gui.Control.showDialog(panel)
