# SPDX-License-Identifier: LGPL-2.1-or-later
# SPDX-FileNotice: Part of the Plot addon.


from matplotlib.colors import colorConverter
from matplotlib.lines import Line2D
from FreeCAD.Plot import Plot # type: ignore
from ..PySide import QtWidgets , QtCore
from os.path import dirname , join
from FreeCAD import Gui



class TaskForm ( QtWidgets.QWidget ):

    markerLabel : QtWidgets.QLabel
    markerSize : QtWidgets.QSpinBox
    styleLabel : QtWidgets.QLabel
    lineWidth : QtWidgets.QDoubleSpinBox
    lineStyle : QtWidgets.QComboBox
    markers : QtWidgets.QComboBox
    isLabel : QtWidgets.QCheckBox
    remove : QtWidgets.QPushButton
    items : QtWidgets.QListWidget
    color : QtWidgets.QPushButton
    label : QtWidgets.QLineEdit


class TaskPanel :

    form : TaskForm

    plot : object = None
    skip : bool = False
    name : str = 'plot series editor'
    item : int = 0


    def __init__ ( self ):

        path = join(
            dirname(__file__) , '..' ,
            'Resources' , 'Interface' , 'Series.ui'
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

        self.fillStyles()
        self.updateUI()

        form = self.form

        form.markerSize.valueChanged.connect(self.onData)
        form.lineStyle.currentIndexChanged.connect(self.onData)
        form.lineWidth.valueChanged.connect(self.onData)
        form.markers.currentIndexChanged.connect(self.onData)
        form.isLabel.stateChanged.connect(self.onData)
        form.label.editingFinished.connect(self.onData)

        form.remove.pressed.connect(self.onRemove)
        form.items.currentRowChanged.connect(self.onItem)
        form.color.pressed.connect(self.onColor)

        Plot.getMdiArea().subWindowActivated.connect(self.onMdiArea)


    def fillStyles ( self ):

        '''
        Fill the style combo boxes with the available ones.
        '''

        form = self.form

        # Line styles

        for style in Line2D.lineStyles.keys():

            string = '\'' + str(style) + '\''
            string += ' (' + Line2D.lineStyles[style] + ')'

            form.lineStyle.addItem(string)

        # Markers

        for marker in Line2D.markers.keys():

            string = '\'' + str(marker) + '\''
            string += ' (' + Line2D.markers[marker] + ')'

            form.markers.addItem(string)


    def onItem ( self , row ):

        '''
        Executed when the selected item is modified.
        '''

        if self.skip:
            return

        self.skip = True

        self.item = row

        self.updateUI()

        self.skip = False


    def onData ( self ):

        '''
        Executed when the selected item data is modified.
        '''

        if self.skip:
            return

        self.skip = True

        plot = Plot.getPlot()

        if not plot:
            self.updateUI()
            return

        # Ensure that selected series exist

        if self.item >= len(Plot.series()):
            self.updateUI()
            return

        # Set label

        serie = Plot.series()[ self.item ]

        if(self.form.isLabel.isChecked()):
            serie.name = None
            self.form.label.setEnabled(False)
        else:
            serie.name = self.form.label.text()
            self.form.label.setEnabled(True)

        # Set line style and marker

        style = self.form.lineStyle.currentIndex()
        linestyles = list(Line2D.lineStyles.keys())
        serie.line.set_linestyle(linestyles[style])
        marker = self.form.markers.currentIndex()
        markers = list(Line2D.markers.keys())
        serie.line.set_marker(markers[marker])

        # Set line width and marker size

        serie.line.set_linewidth(self.form.lineWidth.value())
        serie.line.set_markersize(self.form.markerSize.value())

        plot.update()

        # Regenerate series labels

        self.setList()
        self.skip = False


    def onColor ( self ):

        '''
        Executed when color palette is requested.
        '''

        plot = Plot.getPlot()

        if not plot:
            self.updateUI()
            return

        # Ensure that selected serie exist

        if self.item >= len(Plot.series()):
            self.updateUI()
            return

        # Show widget to select color

        col = QtWidgets.QColorDialog.getColor()

        # Send color to widget and serie

        if col.isValid():

            serie = plot.series[self.item]

            self.form.color.setStyleSheet(
                f'background-color: rgb({ col.red() }, { col.green() }, { col.blue() });'
            )

            serie.line.set_color((
                col.redF() ,
                col.greenF() ,
                col.blueF()
            ))

            plot.update()


    def onRemove ( self ):

        '''
        Executed when the data serie must be removed.
        '''

        plt = Plot.getPlot()

        if not plt:
            self.updateUI()
            return

        # Ensure that selected serie exist

        if self.item >= len(Plot.series()):
            self.updateUI()
            return

        # Remove serie

        removeSeries(self.item)

        self.setList()
        self.updateUI()

        plt.update()


    def onMdiArea(self, subWin):

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
        Setup UI controls values if possible
        '''

        form = self.form
        plot = Plot.getPlot()

        enabled = bool(plot)

        form.markerSize.setEnabled(enabled)
        form.lineStyle.setEnabled(enabled)
        form.lineWidth.setEnabled(enabled)
        form.markers.setEnabled(enabled)
        form.isLabel.setEnabled(enabled)
        form.remove.setEnabled(enabled)
        form.items.setEnabled(enabled)
        form.label.setEnabled(enabled)
        form.color.setEnabled(enabled)

        if not plot:
            self.plot = None
            form.items.clear()
            return

        self.skip = True

        # Refill list

        series = Plot.series()

        if self.plot != plot or len(series) != form.items.count():
            self.plot = plot
            self.setList()

        # Ensure that have series

        if not len(series):
            form.markerSize.setEnabled(False)
            form.lineStyle.setEnabled(False)
            form.lineWidth.setEnabled(False)
            form.isLabel.setEnabled(False)
            form.markers.setEnabled(False)
            form.remove.setEnabled(False)
            form.label.setEnabled(False)
            form.color.setEnabled(False)
            return

        # Set label

        serie = series[ self.item ]

        if serie.name is None:
            form.isLabel.setChecked(True)
            form.label.setEnabled(False)
            form.label.setText('')
        else:
            form.isLabel.setChecked(False)
            form.label.setText(serie.name)

        # Set line style and marker

        form.lineStyle.setCurrentIndex(0)

        for i, style in enumerate(Line2D.lineStyles.keys()):
            if style == serie.line.get_linestyle():
                form.lineStyle.setCurrentIndex(i)

        form.markers.setCurrentIndex(0)

        for i, marker in enumerate(Line2D.markers.keys()):
            if marker == serie.line.get_marker():
                form.markers.setCurrentIndex(i)

        # Set line width and marker size

        form.markerSize.setValue(serie.line.get_markersize())
        form.lineWidth.setValue(serie.line.get_linewidth())

        # Set color

        color = colorConverter.to_rgb(serie.line.get_color())

        green = int(color[1] * 255)
        blue = int(color[2] * 255)
        red = int(color[0] * 255)

        form.color.setStyleSheet(
            f'background-color: rgb({ red },{ green },{ blue });'
        )

        self.skip = False


    def setList(self):

        '''
        Setup the UI control values if it is possible.
        '''

        form = self.form

        form.items.clear()

        series = Plot.series()

        for i in range(0, len(series)):

            serie = series[i]
            string = 'serie ' + str(i) + ': '

            if serie.name is None:
                string = string + '\'No label\''
            else:
                string = string + serie.name

            form.items.addItem(string)

        # Ensure that selected item is correct

        if len(series) and self.item >= len(series):

            self.item = len(series) - 1

            index = form.items.indexAt(QtCore.QPoint(0,self.item))

            form.items.setCurrentIndex(index)


def createTask ():

    panel = TaskPanel()

    Gui.Control.showDialog(panel)


def removeSeries ( index : int ):

    plot = Plot.getPlot()

    if not plot :
        return

    series = plot.series

    if not series :
        return

    serie = series[ index ]

    if not serie :
        return

    axes = serie.axes

    axes.lines[ serie.lid ].remove()

    del plot.series[ index ]

    plot.update()