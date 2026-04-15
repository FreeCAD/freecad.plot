# SPDX-License-Identifier: LGPL-2.1-or-later
# SPDX-FileNotice: Part of the Plot addon.


from FreeCAD.Plot import Plot # type: ignore
from PySide6 import QtWidgets , QtCore
from os.path import dirname , join
from FreeCAD import Gui


class TaskForm ( QtWidgets.QWidget ):

    sizeLabel : QtWidgets.QLabel
    posLabel : QtWidgets.QLabel
    items : QtWidgets.QListWidget
    Size : QtWidgets.QDoubleSpinBox
    X : QtWidgets.QDoubleSpinBox
    Y : QtWidgets.QDoubleSpinBox


class TaskPanel :

    form : TaskForm

    objects = []
    names = []
    name = 'plot positions'
    skip = False
    item = 0
    plot = None


    def __init__ ( self ):

        path = join(
            dirname(__file__), '..' ,
            'Resources' , 'Interface' , 'Positions.ui'
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

    def clicked ( self , index ):
        pass

    def accept ( self ):
        return True

    def reject ( self ):
        return True

    def open ( self ):
        self.setupUi()


    def setupUi ( self ):

        self.updateUI()

        form = self.form

        form.items.currentRowChanged.connect(self.onItem)
        form.Size.valueChanged.connect(self.onData)
        form.X.valueChanged.connect(self.onData)
        form.Y.valueChanged.connect(self.onData)

        Plot.getMdiArea().subWindowActivated.connect(self.onMdiArea)


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

        if not plot :
            self.updateUI()
            return

        if self.skip :
            return

        self.skip = True

        object = self.objects[ self.item ]
        name = self.names[ self.item ]

        form = self.form

        size = form.Size.value()
        x = form.X.value()
        y = form.Y.value()

        # x/y labels only have one position control

        if name.find('x label') >= 0 :
            form.Y.setValue(x)
        elif name.find('y label') >= 0 :
            form.X.setValue(y)

        # title and labels only have one size control

        if name.find('title') >= 0 or name.find('label') >= 0:
            object.set_position((x,y))
            object.set_size(size)
        else:
            # legend have all controls
            Plot.legend(plot.legend, (x, y), size)

        plot.update()

        self.skip = False


    def onMdiArea ( self , window : Plot ):

        plot = Plot.getPlot()

        if plot != window :
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

        if not plot :
            self.plot = plot
            form.items.clear()
            return

        # Refill items list only if Plot instance have been changed

        if self.plot != plot :

            self.plot = plot

            self.plot.update()
            self.setList()

        anyItems = len( self.objects ) > 0

        form.Size.setEnabled(anyItems)
        form.Y.setEnabled(anyItems)
        form.X.setEnabled(anyItems)

        if not anyItems :
            return

        # Get data for controls

        object = self.objects[ self.item ]
        name = self.names[ self.item ]


        if name.find('title') >= 0 or name.find('label') >= 0 :

            position = object.get_position()

            x = position[ 0 ]
            y = position[ 1 ]

            size = object.get_size()

            if name.find('x label') >= 0 :
                form.Y.setEnabled(False)
                form.Y.setValue(x)
            elif name.find('y label') >= 0 :
                form.X.setEnabled(False)
                form.X.setValue(y)

        else :

            x = plot.legPos[ 0 ]
            y = plot.legPos[ 1 ]

            texts = object.get_texts()

            if len( texts ) > 0 :
                size = texts[ -1 ].get_fontsize()
            else :
                size = 10

        # Send it to controls

        form.Size.setValue(size)
        form.X.setValue(x)
        form.Y.setValue(y)


    def setList ( self ):

        '''
        Setup UI controls values if possible
        '''

        # Clear lists

        self.objects = []
        self.names = []

        # Fill lists with available objects

        if self.plot:

            # Axes data

            for i in range(0, len(self.plot.axesList)):

                axes = self.plot.axesList[i]

                # Each axes have title, xaxis and yaxis

                title = axes.title
                text = title.get_text()

                if len( text ) > 0 :
                    self.names.append(f'title (axes { i })')
                    self.objects.append(title)


                label = axes.xaxis.label
                text = label.get_text()

                if len( text ) > 0 :
                    self.objects.append(label)
                    self.names.append(f'x label (axes { i })')


                label = axes.yaxis.label
                text = label.get_text()

                if len( text ) > 0 :
                    self.objects.append(label)
                    self.names.append(f'y label (axes { i })')

            # Legend if exist

            axes = self.plot.axesList[ -1 ]

            legend = axes.legend_

            if legend :

                if len( legend.get_texts() ) > 0 :
                    self.objects.append(axes.legend_)
                    self.names.append('legend')


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
