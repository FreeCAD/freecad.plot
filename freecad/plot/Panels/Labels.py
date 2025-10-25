# SPDX-License-Identifier: LGPL-2.1-or-later

import os

from FreeCAD import Gui , Qt
from FreeCAD.Plot import Plot # type: ignore
from ..PySide import QtWidgets , QtCore


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

        path = os.path.join(
            os.path.dirname(__file__) , '..' ,
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

        self.retranslateUi()

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


    def retranslateUi ( self ):

        '''
        Set the user interface locale strings.
        '''

        form = self.form

        form.setWindowTitle(Qt.translate(
            'plot_labels',
            'Set labels',
            None))
        self.widget(QtWidgets.QLabel, 'axesLabel').setText(
            Qt.translate('plot_labels',
                                         'Active axes',
                                         None))
        self.widget(QtWidgets.QLabel, 'titleLabel').setText(
            Qt.translate('plot_labels',
                                         'Title',
                                         None))
        self.widget(QtWidgets.QLabel, 'xLabel').setText(
            Qt.translate('plot_labels',
                                         'X label'))
        self.widget(QtWidgets.QLabel, 'yLabel').setText(
            Qt.translate('plot_labels',
                                         'Y label'))
        self.widget(QtWidgets.QSpinBox, 'axesIndex').setToolTip(Qt.translate(
            'plot_labels',
            'Index of the active axes'))
        self.widget(QtWidgets.QLineEdit, 'title').setToolTip(
            Qt.translate(
                'plot_labels',
                'Title (associated to active axes)'))
        self.widget(QtWidgets.QSpinBox, 'titleSize').setToolTip(
            Qt.translate(
                'plot_labels',
                'Title font size'))
        self.widget(QtWidgets.QLineEdit, 'titleX').setToolTip(
            Qt.translate(
                'plot_labels',
                'X axis title'))
        self.widget(QtWidgets.QSpinBox, 'xSize').setToolTip(
            Qt.translate(
                'plot_labels',
                'X axis title font size'))
        self.widget(QtWidgets.QLineEdit, 'titleY').setToolTip(
            Qt.translate(
                'plot_labels',
                'Y axis title'))
        self.widget(QtWidgets.QSpinBox, 'ySize').setToolTip(
            Qt.translate(
                'plot_labels',
                'Y axis title font size'))

    def onAxesId(self, value):
        ''' Executed when axes index is modified. '''
        if not self.skip:
            self.skip = True
            # No active plot case
            plt = Plot.getPlot()
            if not plt:
                self.updateUI()
                self.skip = False
                return

            self.form.axId.setMaximum(len(plt.axesList))
            if self.form.axId.value() >= len(plt.axesList):
                self.form.axId.setValue(len(plt.axesList) - 1)
            # Send new control to Plot instance
            plt.setActiveAxes(self.form.axId.value())
            self.updateUI()
            self.skip = False

    def onLabels(self):
        ''' Executed when labels have been modified. '''
        plt = Plot.getPlot()
        if not plt:
            self.updateUI()
            return

        Plot.title(str(self.form.title.text()))
        Plot.xlabel(str(self.form.xLabel.text()))
        Plot.ylabel(str(self.form.yLabel.text()))
        plt.update()

    def onFontSizes(self, value):
        ''' Executed when font sizes have been modified. '''
        # Get apply environment
        plt = Plot.getPlot()
        if not plt:
            self.updateUI()
            return

        ax = plt.axes
        ax.title.set_fontsize(self.form.titleSize.value())
        ax.xaxis.label.set_fontsize(self.form.xSize.value())
        ax.yaxis.label.set_fontsize(self.form.ySize.value())
        plt.update()

    def onMdiArea(self, subWin):
        ''' Executed when window is selected on mdi area.

        Keyword arguments:
        subWin -- Selected window.
        '''
        plt = Plot.getPlot()
        if plt != subWin:
            self.updateUI()

    def updateUI(self):
        ''' Setup UI controls values if possible '''

        plt = Plot.getPlot()
        self.form.axId.setEnabled(bool(plt))
        self.form.title.setEnabled(bool(plt))
        self.form.titleSize.setEnabled(bool(plt))
        self.form.xLabel.setEnabled(bool(plt))
        self.form.xSize.setEnabled(bool(plt))
        self.form.yLabel.setEnabled(bool(plt))
        self.form.ySize.setEnabled(bool(plt))
        if not plt:
            return
        # Ensure that active axes is correct
        index = min(self.form.axId.value(), len(plt.axesList) - 1)
        self.form.axId.setValue(index)
        # Store data before starting changing it.

        ax = plt.axes
        t = ax.get_title()
        x = ax.get_xlabel()
        y = ax.get_ylabel()
        tt = ax.title.get_fontsize()
        xx = ax.xaxis.label.get_fontsize()
        yy = ax.yaxis.label.get_fontsize()
        # Set labels
        self.form.title.setText(t)
        self.form.xLabel.setText(x)
        self.form.yLabel.setText(y)
        # Set font sizes
        self.form.titleSize.setValue(tt)
        self.form.xSize.setValue(xx)
        self.form.ySize.setValue(yy)


def createTask ():

    panel = TaskPanel()

    Gui.Control.showDialog(panel)
