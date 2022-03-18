from PyQt5 import QtCore as qtc 
from PyQt5 import QtWidgets as qtw 
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QFileDialog, QPushButton
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import pyqtSlot
import cv2
import numpy as np
import math
from viewer import Viewer


class Equalizer(qtw.QWidget):
    
    def __init__(self):
        super().__init__()
        
        uic.loadUi("src/ui/equalization.ui", self)

        self.img = [[]]
        self.equalized_image = [[]]

        self.image_viewer = Viewer()
        
        self.image_layout.addWidget(self.image_viewer)

        self.equalized_viewer = Viewer()
        self.equalized_layout.addWidget(self.equalized_viewer)


        self.histogram_viewer = Viewer()
        self.histogram_layout.addWidget(self.histogram_viewer)


        self.equalized_histogram = Viewer()
        self.equalized_histogram_layout.addWidget(self.equalized_histogram)

        # self.equalizer_btn.clicked.connect(self.equalization)
        # self.pushButton.clicked.connect(self.view_equalized_histogram)

    def load_original_image(self, image_path):
       
        self.img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        
        self.view_original_image()
        # self.equalization()
        
        
     
    # def view_equalized_histogram(self):
    #     self.view_equalized_image()

    #     self.view_histogram(self.img)

        
        

       
        
    def equalization(self):
        _, indices, counts = np.unique(self.img, return_counts=True, return_inverse=True)
        
        # equalization factor: pixel depth divided by number of pixels of image.
        equalization_factor = 2**8/(self.img.shape[0]*self.img.shape[1])
        
       
        commulative_density_function = []   

        # to calculate commulative density function (cdf)
        commulative_density_function = np.cumsum(counts)

        Sx = commulative_density_function*equalization_factor-1

        

        # after equalization --> pixels intensity may have float number ---> this reason for calculate ceiling of number
        Sx = np.ceil(Sx)
      
        image_1D = Sx

        # to reverse the origin 1d array after equalization
        image_1D = image_1D[indices]

        # to return to original image
        self.equalized_image = np.reshape(image_1D, (self.img.shape[0],self.img.shape[1]))

        
        # self.view_equalized_histogram(self.equalized_image)
        
      
        

    def view_original_image(self):
        self.image_viewer.draw_image(self.img)

    def view_equalized_image(self):
        self.equalized_viewer.draw_image(self.equalized_image)

    def view_histogram(self, img):
        print("-----------")
        self.histogram_viewer.clear_canvans()
        self.histogram_viewer.draw_histogram(img)

    # def view_equalized_histogram(self, img):
        
    #     self.equalized_histogram.draw_histogram(img)
        

        





    
