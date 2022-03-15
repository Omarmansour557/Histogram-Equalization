from PyQt5 import QtCore as qtc 
from PyQt5 import QtWidgets as qtw 
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QFileDialog, QPushButton
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import pyqtSlot

import cv2
class FilterStudio (qtw.QWidget):
    def __init__(self):
        super().__init__()
        
        uic.loadUi("src/ui/filtering_studio.ui",self)

        self.load_btn.clicked.connect(self.load_original_image)
        self.image_path = None




    # @pyqtSlot()
    # def displayImage(self):
    #     print('PyQt5 button click')
    #     self.image_path,_ = QFileDialog.getOpenFileName(None, 'OpenFile', '', "Image file(*.jpg)")
    #     pixmap = QPixmap(self.image_path)
    #     self.image_viewer.setPixmap(pixmap)
    #     self.label.setScaledContents(True);
    #     read_img = cv2.imread(self.image_path, cv2.IMREAD_COLOR)
    #     print(type(read_img))


    def load_original_image(self, image_path):
        pixmap = QPixmap(image_path)
        self.image_viewer.setPixmap(pixmap)
        self.label.setScaledContents(True);
        # read_img = cv2.imread(self.image_path, cv2.IMREAD_COLOR)
       

    # @pyqtSlot()
    # def filteredImage(self):
    #     read_img = cv2.imread(image[0], cv2.IMREAD_COLOR)


