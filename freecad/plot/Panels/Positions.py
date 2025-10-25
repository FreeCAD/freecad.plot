# SPDX-License-Identifier: LGPL-2.1-or-later

import os

from FreeCAD.Plot import Plot # type: ignore
from FreeCAD import Gui , Qt

from ..PySide import QtWidgets , QtCore


class TaskForm ( QtWidgets.QWidget ):

    sizeLabel : QtWidgets.QLabel
    posLabel : QtWidgets.QLabel
    items : QtWidgets.QListWidget
    Size : QtWidgets.QDoubleSpinBox
    X : QtWidgets.QDoubleSpinBox
    Y : QtWidgets.QDoubleSpinBox


class TaskPanel :

    form : TaskForm

    names = []
    name = 'plot positions'
    skip = False
    objs = []
    item = 0
    plot = None


    def __init__ ( self ):

        path = os.path.join(
            os.path.dirname(__file__), '..' ,
            'Resources' , 'Interface' , 'Positions.ui'
        )

        self.form = Gui.PySideUic.loadUi(path) # type: ignore


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

    def accept ( self ):
        return True

    def reject ( self ):
        return True

    def open ( self ):
        self.setupUi()


    def setupUi ( self ):

        self.retranslateUi()
        self.updateUI()

        form = self.form

        form.items.currentRowChanged.connect(self.onItem)
        form.Size.valueChanged.connect(self.onData)
        form.X.valueChanged.connect(self.onData)
        form.Y.valueChanged.connect(self.onData)

        Plot.getMdiArea().subWindowActivated.connect(self.onMdiArea)


    def retranslateUi ( self ):

        '''
        Set the user interface locale strings.
        '''

        form = self.form

        form.setWindowTitle(
            Qt.translate(
                'plot_positions',
                'Set positions and sizes'
            )
        )

        form.posLabel.setText(
            Qt.translate(
                'plot_positions',
                'Position'
            )
        )

        form.sizeLabel.setText(
            Qt.translate(
                'plot_positions',
                'Size'
            )
        )

        form.items.setToolTip(
            Qt.translate(
                'plot_positions' ,
                'List of modifiable items'
            )
        )

        form.X.setToolTip(
            Qt.translate(
                'plot_positions',
                'X item position'
            )
        )

        form.Y.setToolTip(
            Qt.translate(
                'plot_positions',
                'Y item position'
            )
        )

        form.Size.setToolTip(
            Qt.translate(
                'plot_positions',
                'Item size'
            )
        )


    def onItem ( self , row ):

        '''
        Executed when selected item is modified.
        '''

        self.item = row
        self.updateUI()


    def onData ( self , value ):

        '''
        Executed when selected item data is modified.
        '''

        plot = Plot.getPlot()

        if not plot:
            self.updateUI()
            return

        if not self.skip:

            self.skip = True

            name = self.names[self.item]
            obj = self.objs[self.item]
            s = self.form.Size.value()
            x = self.form.X.value()
            y = self.form.Y.value()

            # x/y labels only have one position control

            if name.find('x label') >= 0:
                self.form.Y.setValue(x)
            elif name.find('y label') >= 0:
                self.form.X.setValue(y)

            # title and labels only have one size control

            if name.find('title') >= 0 or name.find('label') >= 0:
                obj.set_position((x, y))
                obj.set_size(s)
            else:
                # legend have all controls
                Plot.legend(plot.legend, (x, y), s)

            plot.update()

            self.skip = False

    def onMdiArea ( self , subWin ):

        '''
        Executed when a new window is selected on the mdi area.

        Keyword arguments:
        subWin -- Selected window.
        '''

        plt = Plot.getPlot()

        if plt != subWin:
            self.updateUI()


    def updateUI ( self ):

        '''
        Setup the UI control values if it is possible.
        '''

        plot = Plot.getPlot()

        form = self.form

        enabled = bool(plot)

        form.items.setEnabled(enabled)
        form.Size.setEnabled(enabled)
        form.X.setEnabled(enabled)
        form.Y.setEnabled(enabled)

        if not plot:
            self.plot = plot
            form.items.clear()
            return

        # Refill items list only if Plot instance have been changed

        if self.plot != plot:

            self.plot = plot

            self.plot.update()
            self.setList()

        # Get data for controls

        name = self.names[self.item]
        obj = self.objs[self.item]

        if name.find('title') >= 0 or name.find('label') >= 0:

            p = obj.get_position()

            x = p[0]
            y = p[1]

            s = obj.get_size()

            if name.find('x label') >= 0:
                form.Y.setEnabled(False)
                form.Y.setValue(x)
            elif name.find('y label') >= 0:
                form.X.setEnabled(False)
                form.X.setValue(y)
        else:
            x = plot.legPos[0]
            y = plot.legPos[1]
            s = obj.get_texts()[-1].get_fontsize()

        # Send it to controls

        form.Size.setValue(s)
        form.X.setValue(x)
        form.Y.setValue(y)


    def setList ( self ):

        '''
        Setup UI controls values if possible
        '''

        # Clear lists

        self.names = []
        self.objs = []

        # Fill lists with available objects

        if self.plot:

            # Axes data

            for i in range(0, len(self.plot.axesList)):

                ax = self.plot.axesList[i]

                # Each axes have title, xaxis and yaxis

                self.names.append('title (axes {})'.format(i))
                self.objs.append(ax.title)
                self.names.append('x label (axes {})'.format(i))
                self.objs.append(ax.xaxis.get_label())
                self.names.append('y label (axes {})'.format(i))
                self.objs.append(ax.yaxis.get_label())

            # Legend if exist

            ax = self.plot.axesList[-1]

            if ax.legend_:
                self.names.append('legend')
                self.objs.append(ax.legend_)


        form = self.form

        # Send list to widget

        form.items.clear()

        for name in self.names:
            form.items.addItem(name)

        # Ensure that selected item is correct

        if self.item >= len(self.names):

            self.item = len(self.names) - 1

            index = form.items.indexAt(QtCore.QPoint(0,self.item))

            form.items.setCurrentIndex(index)


def createTask ():

    panel = TaskPanel()

    Gui.Control.showDialog(panel)
