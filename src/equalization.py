from PyQt5 import QtCore as qtc 
from PyQt5 import QtWidgets as qtw 
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QFileDialog, QPushButton
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import pyqtSlot
import cv2

class Equalizer(qtw.QWidget):
    def __init__(self):
        super().__init__()
        
        uic.loadUi("src/ui/equalization.ui", self)


    def load_original_image(self, image_path):

        pixmap = QPixmap(image_path)
        print(type(pixmap))

        self.image_view.setPixmap(pixmap)
        # self.label.setScaledContents(True);

    
