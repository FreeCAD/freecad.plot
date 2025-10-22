# SPDX-License-Identifier: LGPL-2.1-or-later

import os

from ..PySide import QtWidgets , QtCore
from FreeCAD import Console , Gui , Qt

from FreeCAD.Plot import Plot


class TaskPanel:

    form : QtWidgets.QWidget

    def __init__ ( self ):

        self.name = 'plot save'
        self.ui = os.path.join(os.path.dirname(__file__),
                               '../resources/ui/',
                               'TaskPanel_plotSave.ui')

        form = Gui.PySideUic.loadUi(( self.ui , ))

        if form :
            self.form = form


    def accept ( self ):

        plt = Plot.getPlot()

        if plt :

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
        pass


    def setupUi ( self ):

        form = self.form

        form.pathButton = self.widget(QtWidgets.QPushButton,'pathButton')
        form.sizeX = self.widget(QtWidgets.QDoubleSpinBox,'sizeX')
        form.sizeY = self.widget(QtWidgets.QDoubleSpinBox,'sizeY')
        form.path = self.widget(QtWidgets.QLineEdit,'path')
        form.dpi = self.widget(QtWidgets.QSpinBox,'dpi')

        self.retranslateUi()

        home = os.getenv('USERPROFILE') or os.getenv('HOME')

        form.path.setText(os.path.join(home,'plot.png'))

        self.updateUI()

        QtCore.QObject.connect(
            form.pathButton ,
            QtCore.SIGNAL('pressed()') ,
            self.onPathButton
        )

        QtCore.QObject.connect(
            Plot.getMdiArea() ,
            QtCore.SIGNAL('subWindowActivated(QMdiSubWindow*)') ,
            self.onMdiArea
        )

        return False


    def getMainWindow ( self ):

        widgets = QtWidgets.QApplication.topLevelWidgets()

        for widget in widgets :
            if widget.metaObject().className() == 'Gui::MainWindow' :
                return widget

        raise RuntimeError('No main window found')


    def widget ( self , class_id , name ):

        '''
        Return the selected widget.

        Keyword arguments:
        class_id -- Class identifier
        name -- Name of the widget
        '''

        window = self.getMainWindow()

        form = window.findChild(QtWidgets.QWidget,'TaskPanel_plotSave')

        return form.findChild(class_id,name)


    def retranslateUi ( self ):

        '''Set the user interface locale strings.'''

        self.form.setWindowTitle(
            Qt.translate(
                'plot_save',
                'Save figure'
            ))

        self.widget(QtWidgets.QLabel,'sizeLabel').setText(
            Qt.translate(
                'plot_save',
                'Inches'
            ))

        self.widget(QtWidgets.QLabel,'dpiLabel').setText(
            Qt.translate(
                'plot_save',
                'Dots per Inch'
            ))

        self.widget(QtWidgets.QLineEdit,'path').setToolTip(
            Qt.translate(
                'plot_save',
                'Output image file path'
            ))

        self.widget(QtWidgets.QPushButton,'pathButton').setToolTip(
            Qt.translate(
                'plot_save',
                'Show a file selection dialog'
            ))

        self.widget(QtWidgets.QDoubleSpinBox,'sizeX').setToolTip(
            Qt.translate(
                'plot_save',
                'X image size'
            ))

        self.widget(QtWidgets.QDoubleSpinBox,'sizeY').setToolTip(
            Qt.translate(
                'plot_save',
                'Y image size'
            ))

        self.widget(QtWidgets.QSpinBox,'dpi').setToolTip(
            Qt.translate(
                'plot_save',
                'Dots per point,with size will define output image'
                ' resolution'
            ))

    def updateUI ( self ):

        ''' Setup UI controls values if possible '''

        plot = Plot.getPlot()

        hasPlot = bool(plot)

        form = self.form

        form.pathButton.setEnabled(hasPlot)
        form.sizeX.setEnabled(hasPlot)
        form.sizeY.setEnabled(hasPlot)
        form.path.setEnabled(hasPlot)
        form.dpi.setEnabled(hasPlot)

        if not plot:
            return

        figure = plot.fig

        size = figure.get_size_inches()
        dpi = figure.get_dpi()

        form.sizeX.setValue(size[ 0 ])
        form.sizeY.setValue(size[ 1 ])
        form.dpi.setValue(dpi)


    def onPathButton ( self ):

        '''Executed when the path selection button is pressed.'''

        form = self.form

        path = form.path.text()

        file_choices = (
            'Portable Network Graphics (*.png)|*.png;;'
            'Portable Document Format (*.pdf)|*.pdf;;'
            'PostScript (*.ps)|*.ps;;'
            'Encapsulated PostScript (*.eps)|*.eps'
        )

        path = QtWidgets.QFileDialog.getSaveFileName \
            (None,'Save figure',path,file_choices)

        if path :

            try:
                form.path.setText(path)
            except TypeError:
                form.path.setText(path[ 0 ])


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

    if panel.setupUi():
        Gui.Control.closeDialog()
        return None

    return panel
