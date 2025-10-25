# SPDX-License-Identifier: LGPL-2.1-or-later


from FreeCAD.Plot import Plot # type: ignore
from ..PySide import QtWidgets
from os.path import dirname , join
from FreeCAD import Gui


class TaskForm ( QtWidgets.QWidget ):

    titleSize : QtWidgets.QSpinBox
    titleX : QtWidgets.QLineEdit
    titleY : QtWidgets.QLineEdit
    title : QtWidgets.QLineEdit

    xSize : QtWidgets.QSpinBox
    ySize : QtWidgets.QSpinBox

    axId : QtWidgets.QSpinBox



class TaskPanel:

    form : TaskForm

    name = 'plot labels'
    skip = False

    def __init__ ( self ):

        path = join(
            dirname(__file__) , '..' ,
            'Resources' , 'Interface' , 'Labels.ui'
        )

        self.form = Gui.PySideUic.loadUi(path) # type: ignore


    def needsFullSpace(self):
        return True

    def isAllowedAlterSelection(self):
        return False

    def isAllowedAlterView(self):
        return True

    def isAllowedAlterDocument(self):
        return False

    def helpRequested(self):
        pass

    def clicked ( self , index ):
        pass

    def accept ( self ):
        return True

    def reject ( self ):
        return True

    def open ( self ):
        self.setupUi()


    def setupUi(self):

        # Look for active axes if can

        axId = 0

        form = self.form

        plot = Plot.getPlot()

        if plot:

            while plot.axes != plot.axesList[axId]:
                axId = axId + 1

            form.axId.setValue(axId)

        self.updateUI()

        form.titleSize.valueChanged.connect(self.onFontSizes)
        form.titleX.editingFinished.connect(self.onLabels)
        form.titleY.editingFinished.connect(self.onLabels)
        form.title.editingFinished.connect(self.onLabels)

        form.xSize.valueChanged.connect(self.onFontSizes)
        form.ySize.valueChanged.connect(self.onFontSizes)

        form.axId.valueChanged.connect(self.onAxesId)

        Plot.getMdiArea().subWindowActivated.connect(self.onMdiArea)


    def onAxesId ( self , value ):

        '''
        Executed when axes index is modified.
        '''

        if self.skip :
            return

        self.skip = True

        # No active plot case

        plot = Plot.getPlot()

        if not plot:
            self.updateUI()
            self.skip = False
            return

        self.form.axId.setMaximum(len(plot.axesList))

        if self.form.axId.value() >= len(plot.axesList):
            self.form.axId.setValue(len(plot.axesList) - 1)

        # Send new control to Plot instance

        plot.setActiveAxes(self.form.axId.value())

        self.updateUI()

        self.skip = False


    def onLabels ( self ):

        '''
        Executed when labels have been modified.
        '''

        plot = Plot.getPlot()

        if not plot:
            self.updateUI()
            return

        Plot.title(str(self.form.title.text()))

        Plot.xlabel(str(self.form.titleX.text()))
        Plot.ylabel(str(self.form.titleY.text()))

        plot.update()


    def onFontSizes ( self , value ):

        '''
        Executed when font sizes have been modified.
        '''

        # Get apply environment

        plot = Plot.getPlot()

        if not plot:
            self.updateUI()
            return

        axes = plot.axes

        axes.title.set_fontsize(self.form.titleSize.value())

        axes.xaxis.label.set_fontsize(self.form.xSize.value())
        axes.yaxis.label.set_fontsize(self.form.ySize.value())

        plot.update()


    def onMdiArea ( self , subWin ):

        '''
        Executed when window is selected on mdi area.

        Keyword arguments:
        subWin -- Selected window.
        '''

        plt = Plot.getPlot()

        if plt != subWin:
            self.updateUI()


    def updateUI ( self ):

        '''
        Setup UI controls values if possible
        '''

        plot = Plot.getPlot()

        self.form.axId.setEnabled(bool(plot))
        self.form.title.setEnabled(bool(plot))
        self.form.titleSize.setEnabled(bool(plot))
        self.form.titleX.setEnabled(bool(plot))
        self.form.xSize.setEnabled(bool(plot))
        self.form.titleY.setEnabled(bool(plot))
        self.form.ySize.setEnabled(bool(plot))

        if not plot:
            return

        # Ensure that active axes is correct

        index = min(self.form.axId.value(), len(plot.axesList) - 1)

        self.form.axId.setValue(index)

        # Store data before starting changing it.

        ax = plot.axes

        t = ax.get_title()
        x = ax.get_xlabel()
        y = ax.get_ylabel()

        tt = ax.title.get_fontsize()
        xx = ax.xaxis.label.get_fontsize()
        yy = ax.yaxis.label.get_fontsize()

        # Set labels

        self.form.title.setText(t)
        self.form.titleX.setText(x)
        self.form.titleY.setText(y)

        # Set font sizes

        self.form.titleSize.setValue(tt)
        self.form.xSize.setValue(xx)
        self.form.ySize.setValue(yy)


def createTask ():

    panel = TaskPanel()

    Gui.Control.showDialog(panel)
