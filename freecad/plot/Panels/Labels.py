# SPDX-License-Identifier: LGPL-2.1-or-later

import os
import FreeCAD as App
import FreeCADGui as Gui

from ..PySide import QtWidgets , QtCore

from FreeCAD.Plot import Plot

try:
    unicode        # Python 2
except NameError:
    unicode = str  # Python 3


class TaskPanel:
    def __init__(self):
        self.name = "plot labels"
        self.ui = os.path.join(os.path.dirname(__file__),
                               "../resources/ui/",
                               "Labels.ui")
        self.form = Gui.PySideUic.loadUi(self.ui)
        self.skip = False

    def accept(self):
        return True

    def reject(self):
        return True

    def clicked(self, index):
        pass

    def open(self):
        pass

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

    def setupUi(self):
        self.form.axId = self.widget(QtWidgets.QSpinBox, "axesIndex")
        self.form.title = self.widget(QtWidgets.QLineEdit, "title")
        self.form.titleSize = self.widget(QtWidgets.QSpinBox, "titleSize")
        self.form.xLabel = self.widget(QtWidgets.QLineEdit, "titleX")
        self.form.xSize = self.widget(QtWidgets.QSpinBox, "xSize")
        self.form.yLabel = self.widget(QtWidgets.QLineEdit, "titleY")
        self.form.ySize = self.widget(QtWidgets.QSpinBox, "ySize")
        self.retranslateUi()
        # Look for active axes if can
        axId = 0
        plt = Plot.getPlot()
        if plt:
            while plt.axes != plt.axesList[axId]:
                axId = axId + 1
            self.form.axId.setValue(axId)
        self.updateUI()
        QtCore.QObject.connect(self.form.axId,
                               QtCore.SIGNAL('valueChanged(int)'),
                               self.onAxesId)
        QtCore.QObject.connect(self.form.title,
                               QtCore.SIGNAL("editingFinished()"),
                               self.onLabels)
        QtCore.QObject.connect(self.form.xLabel,
                               QtCore.SIGNAL("editingFinished()"),
                               self.onLabels)
        QtCore.QObject.connect(self.form.yLabel,
                               QtCore.SIGNAL("editingFinished()"),
                               self.onLabels)
        QtCore.QObject.connect(self.form.titleSize,
                               QtCore.SIGNAL("valueChanged(int)"),
                               self.onFontSizes)
        QtCore.QObject.connect(self.form.xSize,
                               QtCore.SIGNAL("valueChanged(int)"),
                               self.onFontSizes)
        QtCore.QObject.connect(self.form.ySize,
                               QtCore.SIGNAL("valueChanged(int)"),
                               self.onFontSizes)
        QtCore.QObject.connect(
            Plot.getMdiArea(),
            QtCore.SIGNAL("subWindowActivated(QMdiSubWindow*)"),
            self.onMdiArea)
        return False

    def getMainWindow(self):
        toplevel = QtWidgets.QApplication.topLevelWidgets()
        for i in toplevel:
            if i.metaObject().className() == "Gui::MainWindow":
                return i
        raise RuntimeError("No main window found")

    def widget(self, class_id, name):
        """Return the selected widget.

        Keyword arguments:
        class_id -- Class identifier
        name -- Name of the widget
        """
        mw = self.getMainWindow()
        form = mw.findChild(QtWidgets.QWidget, "Plot-Task-Labels")
        return form.findChild(class_id, name)

    def retranslateUi(self):
        """ Set the user interface locale strings.
        """
        self.form.setWindowTitle(App.Qt.translate(
            "plot_labels",
            "Set labels",
            None))
        self.widget(QtWidgets.QLabel, "axesLabel").setText(
            App.Qt.translate("plot_labels",
                                         "Active axes",
                                         None))
        self.widget(QtWidgets.QLabel, "titleLabel").setText(
            App.Qt.translate("plot_labels",
                                         "Title",
                                         None))
        self.widget(QtWidgets.QLabel, "xLabel").setText(
            App.Qt.translate("plot_labels",
                                         "X label",
                                         None))
        self.widget(QtWidgets.QLabel, "yLabel").setText(
            App.Qt.translate("plot_labels",
                                         "Y label",
                                         None))
        self.widget(QtWidgets.QSpinBox, "axesIndex").setToolTip(App.Qt.translate(
            "plot_labels",
            "Index of the active axes",
            None))
        self.widget(QtWidgets.QLineEdit, "title").setToolTip(
            App.Qt.translate(
                "plot_labels",
                "Title (associated to active axes)",
                None))
        self.widget(QtWidgets.QSpinBox, "titleSize").setToolTip(
            App.Qt.translate(
                "plot_labels",
                "Title font size",
                None))
        self.widget(QtWidgets.QLineEdit, "titleX").setToolTip(
            App.Qt.translate(
                "plot_labels",
                "X axis title",
                None))
        self.widget(QtWidgets.QSpinBox, "xSize").setToolTip(
            App.Qt.translate(
                "plot_labels",
                "X axis title font size",
                None))
        self.widget(QtWidgets.QLineEdit, "titleY").setToolTip(
            App.Qt.translate(
                "plot_labels",
                "Y axis title",
                None))
        self.widget(QtWidgets.QSpinBox, "ySize").setToolTip(
            App.Qt.translate(
                "plot_labels",
                "Y axis title font size",
                None))

    def onAxesId(self, value):
        """ Executed when axes index is modified. """
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
        """ Executed when labels have been modified. """
        plt = Plot.getPlot()
        if not plt:
            self.updateUI()
            return

        Plot.title(unicode(self.form.title.text()))
        Plot.xlabel(unicode(self.form.xLabel.text()))
        Plot.ylabel(unicode(self.form.yLabel.text()))
        plt.update()

    def onFontSizes(self, value):
        """ Executed when font sizes have been modified. """
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
        """ Executed when window is selected on mdi area.

        Keyword arguments:
        subWin -- Selected window.
        """
        plt = Plot.getPlot()
        if plt != subWin:
            self.updateUI()

    def updateUI(self):
        """ Setup UI controls values if possible """

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


def createTask():
    panel = TaskPanel()
    Gui.Control.showDialog(panel)
    if panel.setupUi():
        Gui.Control.closeDialog()
        return None
    return panel
