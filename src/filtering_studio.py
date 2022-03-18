from PyQt5 import QtCore as qtc 
from PyQt5 import QtWidgets as qtw 
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QFileDialog, QPushButton
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import pyqtSlot
from viewer import Viewer
import cv2
import numpy as np
from skimage.color import rgb2gray
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

        self.filters_list.activated.connect(lambda:self.selectionChange(self.filters_list.currentIndex()))
        self.modes_list.activated.connect(lambda:self.flag_change(self.modes_list.currentIndex()))
        self.flag = 0
        self.image_path = None


    def flag_change(self,mode_index ):
        self.flag = mode_index
        print(self.flag)
        self.selectionChange(self.filters_list.currentIndex())
        print(self.filters_list.currentIndex())






    def selectionChange(self, filter_index):
        if(filter_index == 0):
            self.apply_low_pass_filter()

        elif filter_index == 1:
            self.apply_high_pass_filter() 

        elif filter_index == 2:
            self.apply_median_pass_filter()     
        else:
            self.apply_laplacian_filter()   



    # def load_original_image(self, image_path):
    #     self.image_path = image_path
    #     self.img = cv2.imread(self.image_path, cv2.IMREAD_GRAYSCALE)
    #     self.original_image.draw_image(self.img)
       
        
    def load_original_image(self, image_path):
        self.image_path = image_path
        self.img = cv2.imread(self.image_path, cv2.IMREAD_GRAYSCALE)
        self.original_image.draw_image(self.img)
        image=cv2.imread(image_path)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  

        if(len(image.shape)==2):
                image =rgb2gray(image)*255

        # image = cv2.resize(image, (100, 540))                # Resize image

        self.original_image.draw_image(image)
        self.to_dft()
        self.selectionChange(self.filters_list.currentIndex())

    
    def apply_low_pass_filter(self):
        img = cv2.imread(self.image_path)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        if(self.flag == 0):
            img =rgb2gray(img)*255
        else:
            img = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
            tem=img
            img=img[:,:,2]


        dft = np.fft.fft2(img, axes=(0,1))
        dft_shift = np.fft.fftshift(dft)
        radius = 32
        mask = np.zeros_like(img)
        cy = mask.shape[0] // 2
        cx = mask.shape[1] // 2
        cv2.circle(mask, (cx,cy), radius, (255,255,255), -1)[0]
        dft_shift_masked = np.multiply(dft_shift,mask) / 255
        dft_shift_masked_scaled=20*np.log(np.abs(dft_shift_masked)+1)
        back_ishift_masked = np.fft.ifftshift(dft_shift_masked)
        img_filtered = np.fft.ifft2(back_ishift_masked, axes=(0,1))
        img_filtered = np.abs(img_filtered).clip(0,255).astype(np.uint8)

        if(self.flag == 1):
            img_filtered=np.transpose([tem[:,:,0].T, tem[:,:,1].T, img_filtered.T])
            img_filtered=cv2.cvtColor(img_filtered,cv2.COLOR_HSV2RGB)

        


        self.filtered_image.draw_image(img_filtered) 
        self.filtered_dft.draw_image(dft_shift_masked_scaled)


    def to_dft(self):  
        img = cv2.imread(self.image_path,0)
        # img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        # img = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
        dft = np.fft.fft2(img)
        dft_shift = np.fft.fftshift(dft)
        dft_shifted_scaled = 20*np.log(np.abs(dft_shift)+1) 
        self.dft_image.draw_image(dft_shifted_scaled)   

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
        img = cv2.imread(self.image_path,0)
        laplacian_filter =  cv2.Laplacian(img,cv2.CV_64F ,ksize =5)
        self.filtered_image.draw_image(laplacian_filter)
        #dft of image 
        frequency = np.fft.fft2(self.img)
        fshift = np.fft.fftshift(frequency)
        laplacian_spectrum = np.log(np.abs(fshift)+1)
        self.dft_image.draw_image(laplacian_spectrum)
        #filtered dft
        frequencyf = np.fft.fft2(laplacian_filter)
        f_filter_shift = np.fft.fftshift(frequencyf)
        laplacian_spectrum_filtered = 20*np.log(np.abs(f_filter_shift)+1)
        self.filtered_dft.draw_image( laplacian_spectrum_filtered)