from PyQt5 import QtCore as qtc 
from PyQt5 import QtWidgets as qtw 
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QFileDialog, QPushButton
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import pyqtSlot
from viewer import Viewer
import cv2
import numpy as np
class FilterStudio (qtw.QWidget):
    def __init__(self):
        super().__init__()
        
        uic.loadUi("src/ui/filtering_studio.ui",self)

        
        self.original_image = Viewer()
        self.image_layout.addWidget(self.original_image)
        


        self.filtered_image = Viewer()
        self.filtered_layout.addWidget(self.filtered_image)


        self.dft_image = Viewer()
        self.dft_layout.addWidget(self.dft_image)


        self.filtered_dft = Viewer()
        self.filtered_dft_layout.addWidget(self.filtered_dft)

        self.filters_list.currentIndexChanged.connect(self.selectionChange)


        self.image_path = None

    def selectionChange(self, filter_index):
        if(filter_index == 0):
            self.apply_low_pass_filter()

        elif filter_index == 1:
            self.apply_high_pass_filter() 

        elif filter_index == 2:
            self.apply_median_pass_filter()     
        else:
            self.apply_laplacian_filter()   



    def load_original_image(self, image_path):
        self.image_path = image_path
        self.img = cv2.imread(self.image_path, cv2.IMREAD_GRAYSCALE)
        self.original_image.draw_image(self.img)
       
        
    def apply_low_pass_filter(self):
        ## apply low pass filter --> gamel's mission
        pass  
       

    def apply_high_pass_filter(self):
         ## apply high pass filter --> saied's mission
        pass

    def apply_median_pass_filter(self) :
        
         ## apply median  filter --> omar's mission
        self.img = cv2.imread(self.image_path, cv2.IMREAD_GRAYSCALE)
        medianfilter_image = cv2.medianBlur(self.img, 3)
        self.filtered_image.draw_image(medianfilter_image)
        
        ## draw fft of image 
        f = np.fft.fft2(self.img)
        fshift = np.fft.fftshift(f)
        magnitude_spectrum = 20*np.log(np.abs(fshift))
        self.dft_image.draw_image(magnitude_spectrum)



        # draw filtered fft
        f = np.fft.fft2(medianfilter_image)
        f_filter_shift = np.fft.fftshift(f)
        magnitude_spectrum_filter = 20*np.log(np.abs(f_filter_shift))
        self.filtered_dft.draw_image( magnitude_spectrum_filter)

       

    def apply_laplacian_filter(self):
        ## apply laplacian filter --> Anas's mission
        pass