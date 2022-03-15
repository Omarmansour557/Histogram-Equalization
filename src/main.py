from PyQt5 import QtCore as qtc 
from PyQt5 import QtWidgets as qtw 
from PyQt5 import uic
import sys
import qdarkstyle
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QFileDialog, QPushButton
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import pyqtSlot

from page import Page


class MainWindow(qtw.QMainWindow):
    def __init__(self):
        super().__init__()

        uic.loadUi("src/ui/mainWindow.ui", self)
        self.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyqt5'))
        self.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
        self.page = Page()
        self.centralWidget().layout().addWidget(self.page)
        self.browse_action.triggered.connect(self.Load_image_file)
        print("test")


    @pyqtSlot()
    def Load_image_file(self):
        image_path,_ = QFileDialog.getOpenFileName(None, 'OpenFile', '', "Image file(*.jpg)")
        self.page.load_image(image_path)


if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())