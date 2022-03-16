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

        # self.equalizer_btn.clicked.connect(self.view_equalized_image)

        self.image_viewer = Viewer()
        self.image_layout.addWidget(self.image_viewer)

        self.equalized_viewer = Viewer()
        self.equalized_layout.addWidget(self.equalized_viewer)


        self.histogram_viewer = Viewer()
        self.histogram_layout.addWidget(self.histogram_viewer)


        self.equalized_histogram = Viewer()
        self.equalized_histogram_layout.addWidget(self.equalized_histogram)



        self.equalized_image_pixmap =  None
        self.original_image_pixmap  =  None
        self.equalized_image_path   = None

        


    def load_original_image(self, image_path):
       
        img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        _, indices, counts = np.unique(img, return_counts=True, return_inverse=True)

        # equalization factor: pixel depth divided by number of pixels of image.
        equalization_factor = 2**8/(img.shape[0]*img.shape[1])
        
        auxillary_var = 0
        commulative_density_function = []   

        # to calculate commulative density function (cdf)
        for i in range(256):
            commulative_density_function.append(counts[i] + auxillary_var)
            auxillary_var = commulative_density_function[i]

        Sx = [i*equalization_factor-1 for i in commulative_density_function]

        # after equalization --> pixels intensity may have float number ---> this reason for calculate ceiling of number
        Sx = [math.ceil(x) for x in Sx]
        image_1D = np.array(Sx)

        # to reverse the origin 1d array after equalization
        image_1D = image_1D[indices]

        # to return to original image
        equalized_image = np.reshape(image_1D, (img.shape[0],img.shape[1]))

        # saving image because we need the path to view it in label
        cv2.imwrite('src/equalizedImage.jpg', equalized_image)
        self.equalized_image_path = 'src/equalizedImage.jpg'

        

        # view equalized image
        # self.original_image_pixmap = QPixmap(image_path)
        # self.image_view.setPixmap(self.original_image_pixmap)
        # self.image_view.setScaledContents(True)


    # def view_equalized_image(self):
    #     # view original image
    #     self.equalized_image_pixmap = QPixmap(self.equalized_image_path)
    #     self.equalization_view.setPixmap(self.equalized_image_pixmap)
    #     self.equalization_view.setScaledContents(True)




    
