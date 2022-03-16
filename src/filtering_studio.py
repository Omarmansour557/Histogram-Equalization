from PyQt5 import QtCore as qtc 
from PyQt5 import QtWidgets as qtw 
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QFileDialog, QPushButton
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import pyqtSlot
from viewer import Viewer
import cv2
class FilterStudio (qtw.QWidget):
    def __init__(self):
        super().__init__()
        
        uic.loadUi("src/ui/filtering_studio.ui",self)

        self.load_btn.clicked.connect(self.load_original_image)
        self.original_image = Viewer()
        self.image_layout.addWidget(self.original_image)


        self.filtered_image = Viewer()
        self.filtered_layout.addWidget(self.filtered_image)


        self.dft_image = Viewer()
        self.dft_layout.addWidget(self.dft_image)


        self.filtered_dft = Viewer()
        self.filtered_dft_layout.addWidget(self.filtered_dft)


        self.image_path = None




    def load_original_image(self, image_path):
        pixmap = QPixmap(image_path)
        self.image_viewer.setPixmap(pixmap)
        self.label.setScaledContents(True);
       
       

   

