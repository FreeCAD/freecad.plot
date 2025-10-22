# SPDX-License-Identifier: LGPL-2.1-or-later

import os
import FreeCAD as App
import FreeCADGui as Gui

from PySide import QtGui, QtCore

from FreeCAD.Plot import Plot


class TaskPanel:
    def __init__(self):
        self.name = "plot save"
        self.ui = os.path.join(os.path.dirname(__file__),
                               "../resources/ui/",
                               "TaskPanel_plotSave.ui")
        self.form = Gui.PySideUic.loadUi(self.ui)

    def accept(self):
        plt = Plot.getPlot()
        if not plt:
            msg = App.Qt.translate(
                "plot_console",
                "Plot document must be selected in order to save it",
                None)
            App.Console.PrintError(msg + "\n")
            return False
        path = self.form.path.text()
        size = (self.form.sizeX.value(), self.form.sizeY.value())
        dpi = self.form.dpi.value()
        Plot.save(path, size, dpi)
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
        self.form.path = self.widget(QtGui.QLineEdit, "path")
        self.form.pathButton = self.widget(QtGui.QPushButton, "pathButton")
        self.form.sizeX = self.widget(QtGui.QDoubleSpinBox, "sizeX")
        self.form.sizeY = self.widget(QtGui.QDoubleSpinBox, "sizeY")
        self.form.dpi = self.widget(QtGui.QSpinBox, "dpi")
        self.retranslateUi()
        home = os.getenv('USERPROFILE') or os.getenv('HOME')
        self.form.path.setText(os.path.join(home, "plot.png"))
        self.updateUI()
        QtCore.QObject.connect(
            self.form.pathButton,
            QtCore.SIGNAL("pressed()"),
            self.onPathButton)
        QtCore.QObject.connect(
            Plot.getMdiArea(),
            QtCore.SIGNAL("subWindowActivated(QMdiSubWindow*)"),
            self.onMdiArea)
        return False

    def getMainWindow(self):
        toplevel = QtGui.QApplication.topLevelWidgets()
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
        form = mw.findChild(QtGui.QWidget, "TaskPanel_plotSave")
        return form.findChild(class_id, name)

    def retranslateUi(self):
        """Set the user interface locale strings."""
        self.form.setWindowTitle(App.Qt.translate(
            "plot_save",
            "Save figure",
            None))
        self.widget(QtGui.QLabel, "sizeLabel").setText(
            App.Qt.translate(
                "plot_save",
                "Inches",
                None))
        self.widget(QtGui.QLabel, "dpiLabel").setText(
            App.Qt.translate(
                "plot_save",
                "Dots per Inch",
                None))
        self.widget(QtGui.QLineEdit, "path").setToolTip(
            App.Qt.translate(
                "plot_save",
                "Output image file path",
                None))
        self.widget(QtGui.QPushButton, "pathButton").setToolTip(
            App.Qt.translate(
                "plot_save",
                "Show a file selection dialog",
                None))
        self.widget(QtGui.QDoubleSpinBox, "sizeX").setToolTip(
            App.Qt.translate(
                "plot_save",
                "X image size",
                None))
        self.widget(QtGui.QDoubleSpinBox, "sizeY").setToolTip(
            App.Qt.translate(
                "plot_save",
                "Y image size",
                None))
        self.widget(QtGui.QSpinBox, "dpi").setToolTip(
            App.Qt.translate(
                "plot_save",
                "Dots per point, with size will define output image"
                " resolution",
                None))

    def updateUI(self):
        """ Setup UI controls values if possible """
        plt = Plot.getPlot()
        self.form.path.setEnabled(bool(plt))
        self.form.pathButton.setEnabled(bool(plt))
        self.form.sizeX.setEnabled(bool(plt))
        self.form.sizeY.setEnabled(bool(plt))
        self.form.dpi.setEnabled(bool(plt))
        if not plt:
            return
        fig = plt.fig
        size = fig.get_size_inches()
        dpi = fig.get_dpi()
        self.form.sizeX.setValue(size[0])
        self.form.sizeY.setValue(size[1])
        self.form.dpi.setValue(dpi)

    def onPathButton(self):
        """Executed when the path selection button is pressed."""
        path = self.form.path.text()
        file_choices = ("Portable Network Graphics (*.png)|*.png;;"
                        "Portable Document Format (*.pdf)|*.pdf;;"
                        "PostScript (*.ps)|*.ps;;"
                        "Encapsulated PostScript (*.eps)|*.eps")
        path = QtGui.QFileDialog.getSaveFileName(None,
                                                 'Save figure',
                                                 path,
                                                 file_choices)
        if path:
            try:
                form.path.setText(path)
            except TypeError:
                form.path.setText(path[0])

    def onMdiArea(self, subWin):
        """Executed when a new window is selected on the mdi area.

        Keyword arguments:
        subWin -- Selected window.
        """
        plt = Plot.getPlot()
        if plt != subWin:
            self.updateUI()


def createTask():
    panel = TaskPanel()
    Gui.Control.showDialog(panel)
    if panel.setupUi():
        Gui.Control.closeDialog()
        return None
    return panel
