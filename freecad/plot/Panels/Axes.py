# SPDX-License-Identifier: LGPL-2.1-or-later


from matplotlib.spines import Spines
from FreeCAD.Plot import Plot # type: ignore
from ..PySide import QtWidgets
from os.path import dirname , join
from FreeCAD import Console , Gui , Qt


class TaskForm ( QtWidgets.QWidget ):

    newAxesButton : QtWidgets.QPushButton
    delAxesButton : QtWidgets.QPushButton
    axesIndex : QtWidgets.QSpinBox
    allAxes : QtWidgets.QCheckBox
    xOffset : QtWidgets.QSpinBox
    yOffset : QtWidgets.QSpinBox
    posXMin : QtWidgets.QSlider
    posXMax : QtWidgets.QSlider
    posYMin : QtWidgets.QSlider
    posYMax : QtWidgets.QSlider
    xAlign : QtWidgets.QComboBox
    yAlign : QtWidgets.QComboBox
    xAuto : QtWidgets.QCheckBox
    yAuto : QtWidgets.QCheckBox
    xMin : QtWidgets.QLineEdit
    yMin : QtWidgets.QLineEdit
    xMax : QtWidgets.QLineEdit
    yMax : QtWidgets.QLineEdit


class TaskPanel:

    form : TaskForm

    name = 'plot axes'
    skip = False


    def __init__ ( self ):

        path = join(
            dirname(__file__),'..' ,
            'Resources' , 'Interface' , 'Axes.ui'
        )

        self.form = Gui.PySideUic.loadUi(path) # type: ignore


    def isAllowedAlterSelection ( self ):
        return False

    def isAllowedAlterDocument ( self ):
        return False

    def isAllowedAlterView ( self ):
        return True

    def getStandardButtons ( self ):
        return QtWidgets.QDialogButtonBox.StandardButton.Close

    def needsFullSpace ( self ):
        return True

    def helpRequested ( self ):
        pass

    def accept ( self ):
        return True

    def reject ( self ):
        return True

    def clicked ( self , index ):
        pass

    def open ( self ):
        self.setupUi()


    def setupUi ( self ):

        # Look for active axes if can

        axId = 0

        form = self.form

        plot = Plot.getPlot()

        if plot:

            while plot.axes != plot.axesList[axId]:
                axId = axId + 1

            form.axesIndex.setValue(axId)

        self.updateUI()

        form.axesIndex.valueChanged.connect(self.onAxesId)

        form.delAxesButton.pressed.connect(self.onRemove)
        form.newAxesButton.pressed.connect(self.onNew)

        form.posXMin.valueChanged.connect(self.onDims)
        form.posXMax.valueChanged.connect(self.onDims)
        form.posYMin.valueChanged.connect(self.onDims)
        form.posYMax.valueChanged.connect(self.onDims)

        form.xAlign.currentIndexChanged.connect(self.onAlign)
        form.yAlign.currentIndexChanged.connect(self.onAlign)

        form.xOffset.valueChanged.connect(self.onOffset)
        form.yOffset.valueChanged.connect(self.onOffset)

        form.xAuto.stateChanged.connect(self.onScales)
        form.yAuto.stateChanged.connect(self.onScales)
        form.xMin.editingFinished.connect(self.onScales)
        form.xMax.editingFinished.connect(self.onScales)
        form.yMin.editingFinished.connect(self.onScales)
        form.yMax.editingFinished.connect(self.onScales)

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

        form = self.form

        form.axesIndex.setMaximum(len(plot.axesList))

        if form.axesIndex.value() >= len(plot.axesList):
            form.axesIndex.setValue(len(plot.axesList) - 1)

        # Send new control to Plot instance

        plot.setActiveAxes(form.axesIndex.value())

        self.updateUI()

        self.skip = False


    def onNew ( self ):

        '''
        Executed when new axes must be created.
        '''

        # Ensure that we can work

        plot = Plot.getPlot()

        if not plot:
            self.updateUI()
            return

        Plot.addNewAxes()

        form = self.form

        form.axesIndex.setValue(len(plot.axesList) - 1)

        plot.update()


    def onRemove ( self ):

        '''
        Executed when axes must be deleted.
        '''

        # Ensure that we can work

        plot = Plot.getPlot()

        if not plot:
            self.updateUI()
            return

        form = self.form

        # Don't remove first axes

        if not form.axesIndex.value():

            message = Qt.translate(
                'plot_console',
                'Axes 0 can not be deleted'
            )

            Console.PrintError(f'{ message }\n')

            return

        # Remove axes

        ax = plot.axes
        ax.set_axis_off()

        plot.axesList.pop(form.axesIndex.value())

        # Ensure that active axes is correct

        index = min(form.axesIndex.value(), len(plot.axesList) - 1)

        form.axesIndex.setValue(index)

        plot.update()


    def onDims ( self , value ):

        '''
        Executed when axes dims have been modified.
        '''

        # Ensure that we can work

        plot = Plot.getPlot()

        if not plot:
            self.updateUI()
            return

        axesList = [plot.axes]

        if self.form.allAxes.isChecked():
            axesList = plot.axesList

        # Set new dimensions

        xmin = self.form.posXMin.value() / 100.0
        xmax = self.form.posXMax.value() / 100.0

        ymin = self.form.posYMin.value() / 100.0
        ymax = self.form.posYMax.value() / 100.0

        for axes in axesList:
            axes.set_position([xmin, ymin, xmax - xmin, ymax - ymin])

        plot.update()


    def onAlign ( self , value ):

        '''
        Executed when axes align have been modified.
        '''

        # Ensure that we can work

        plot = Plot.getPlot()

        if not plot:
            self.updateUI()
            return

        axesList = [plot.axes]

        if self.form.allAxes.isChecked():
            axesList = plot.axesList

        # Set new alignment

        for axes in axesList:

            if self.form.xAlign.currentIndex() == 0:
                axes.xaxis.tick_bottom()
                axes.spines['bottom'].set_color((0.0, 0.0, 0.0))
                axes.spines['top'].set_color('none')
                axes.xaxis.set_ticks_position('bottom')
                axes.xaxis.set_label_position('bottom')
            else:
                axes.xaxis.tick_top()
                axes.spines['top'].set_color((0.0, 0.0, 0.0))
                axes.spines['bottom'].set_color('none')
                axes.xaxis.set_ticks_position('top')
                axes.xaxis.set_label_position('top')

            if self.form.yAlign.currentIndex() == 0:
                axes.yaxis.tick_left()
                axes.spines['left'].set_color((0.0, 0.0, 0.0))
                axes.spines['right'].set_color('none')
                axes.yaxis.set_ticks_position('left')
                axes.yaxis.set_label_position('left')
            else:
                axes.yaxis.tick_right()
                axes.spines['right'].set_color((0.0, 0.0, 0.0))
                axes.spines['left'].set_color('none')
                axes.yaxis.set_ticks_position('right')
                axes.yaxis.set_label_position('right')

        plot.update()


    def onOffset ( self , value ):

        '''
        Executed when axes offsets have been modified.
        '''

        # Ensure that we can work

        plot = Plot.getPlot()

        if not plot:
            self.updateUI()
            return

        form = self.form

        axesList = [ plot.axes ]

        if form.allAxes.isChecked():
            axesList = plot.axesList

        # Set new offset

        for axes in axesList:

            # For some reason, modify spines offset erase axes labels, so we
            # need store it in order to regenerate later

            x = axes.get_xlabel()
            y = axes.get_ylabel()

            spines : Spines = axes.spines

            for loc , spine in spines.items() :

                if loc in [ 'bottom', 'top' ]:
                    spine.set_position(('outward',form.xOffset.value()))

                if loc in [ 'left' , 'right' ]:
                    spine.set_position(('outward',form.yOffset.value()))

            # Now we can restore axes labels

            Plot.xlabel(str(x))
            Plot.ylabel(str(y))

        plot.update()


    def onScales ( self ):

        '''
        Executed when axes scales have been modified.
        '''

        # Ensure that we can work

        plot = Plot.getPlot()

        if not plot:
            self.updateUI()
            return

        axesList = [plot.axes]

        if self.form.allAxes.isChecked():
            axesList = plot.axesList

        if self.skip :
            return

        self.skip = True

        # X axis

        if self.form.xAuto.isChecked():

            for ax in axesList:
                ax.set_autoscalex_on(True)

            self.form.xMin.setEnabled(False)
            self.form.xMax.setEnabled(False)

            lim = plot.axes.get_xlim()

            self.form.xMin.setText(str(lim[0]))
            self.form.xMax.setText(str(lim[1]))

        else:

            self.form.xMin.setEnabled(True)
            self.form.xMax.setEnabled(True)

            try:
                xMin = float(self.form.xMin.text())
            except:
                xMin = plot.axes.get_xlim()[0]
                self.form.xMin.setText(str(xMin))

            try:
                xMax = float(self.form.xMax.text())
            except:
                xMax = plot.axes.get_xlim()[1]
                self.form.xMax.setText(str(xMax))

            for ax in axesList:
                ax.set_xlim((xMin, xMax))

        # Y axis

        if self.form.yAuto.isChecked():

            for ax in axesList:
                ax.set_autoscaley_on(True)

            self.form.yMin.setEnabled(False)
            self.form.yMax.setEnabled(False)

            lim = plot.axes.get_ylim()

            self.form.yMin.setText(str(lim[0]))
            self.form.yMax.setText(str(lim[1]))

        else:

            self.form.yMin.setEnabled(True)
            self.form.yMax.setEnabled(True)

            try:
                yMin = float(self.form.yMin.text())
            except:
                yMin = plot.axes.get_ylim()[0]
                self.form.yMin.setText(str(yMin))

            try:
                yMax = float(self.form.yMax.text())
            except:
                yMax = plot.axes.get_ylim()[1]
                self.form.yMax.setText(str(yMax))

            for ax in axesList:
                ax.set_ylim((yMin, yMax))

        plot.update()

        self.skip = False


    def onMdiArea ( self , subWin ):

        '''
        Executed when window is selected on mdi area.

        Keyword arguments:
        subWin -- Selected window.
        '''

        plot = Plot.getPlot()

        if plot != subWin:
            self.updateUI()


    def updateUI ( self ):

        '''
        Setup UI controls values if possible
        '''

        plot = Plot.getPlot()

        form = self.form

        form.newAxesButton.setEnabled(bool(plot))
        form.delAxesButton.setEnabled(bool(plot))
        form.axesIndex.setEnabled(bool(plot))
        form.allAxes.setEnabled(bool(plot))
        form.posXMin.setEnabled(bool(plot))
        form.posXMax.setEnabled(bool(plot))
        form.posYMin.setEnabled(bool(plot))
        form.posYMax.setEnabled(bool(plot))
        form.xAlign.setEnabled(bool(plot))
        form.yAlign.setEnabled(bool(plot))
        form.xOffset.setEnabled(bool(plot))
        form.yOffset.setEnabled(bool(plot))
        form.xAuto.setEnabled(bool(plot))
        form.yAuto.setEnabled(bool(plot))
        form.xMin.setEnabled(bool(plot))
        form.xMax.setEnabled(bool(plot))
        form.yMin.setEnabled(bool(plot))
        form.yMax.setEnabled(bool(plot))

        if not plot:
            form.axesIndex.setValue(0)
            return

        # Ensure that active axes is correct

        index = min(form.axesIndex.value(), len(plot.axesList) - 1)
        form.axesIndex.setValue(index)

        # Set dimensions

        ax = plot.axes
        bb = ax.get_position()

        form.posXMin.setValue(int(100 * bb.min[0]))
        form.posXMax.setValue(int(100 * bb.max[0]))
        form.posYMin.setValue(int(100 * bb.min[1]))
        form.posYMax.setValue(int(100 * bb.max[1]))

        # Set alignment and offset

        xPos = ax.xaxis.get_ticks_position()
        yPos = ax.yaxis.get_ticks_position()

        xOffset = ax.spines['bottom'].get_position()[1]
        yOffset = ax.spines['left'].get_position()[1]

        if xPos == 'bottom' or xPos == 'default':
            form.xAlign.setCurrentIndex(0)
        else:
            form.xAlign.setCurrentIndex(1)

        form.xOffset.setValue(xOffset)

        if yPos == 'left' or yPos == 'default':
            form.yAlign.setCurrentIndex(0)
        else:
            form.yAlign.setCurrentIndex(1)

        form.yOffset.setValue(yOffset)

        # Set scales

        if ax.get_autoscalex_on():
            form.xAuto.setChecked(True)
            form.xMin.setEnabled(False)
            form.xMax.setEnabled(False)
        else:
            form.xAuto.setChecked(False)
            form.xMin.setEnabled(True)
            form.xMax.setEnabled(True)

        lim = ax.get_xlim()

        form.xMin.setText(str(lim[0]))
        form.xMax.setText(str(lim[1]))

        if ax.get_autoscaley_on():
            form.yAuto.setChecked(True)
            form.yMin.setEnabled(False)
            form.yMax.setEnabled(False)
        else:
            form.yAuto.setChecked(False)
            form.yMin.setEnabled(True)
            form.yMax.setEnabled(True)

        lim = ax.get_ylim()

        form.yMin.setText(str(lim[0]))
        form.yMax.setText(str(lim[1]))


def createTask ():

    panel = TaskPanel()

    Gui.Control.showDialog(panel)
