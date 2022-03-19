from PyQt5 import QtCore as qtc
from PyQt5 import QtWidgets as qtw
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QFileDialog, QPushButton
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import pyqtSlot
from viewer import Viewer
import cv2
from numpy.fft import fft2, ifft2, fftshift, ifftshift
import numpy as np


class FilterStudio(qtw.QWidget):
    def __init__(self):
        super().__init__()

        uic.loadUi("ui/filtering_studio.ui", self)

        self.original_image = Viewer()
        self.image_layout.addWidget(self.original_image)
        self.filtered_image = Viewer()
        self.filtered_layout.addWidget(self.filtered_image)
        self.dft_image = Viewer()
        self.dft_layout.addWidget(self.dft_image)
        self.filtered_dft = Viewer()
        self.filtered_dft_layout.addWidget(self.filtered_dft)

        self.MODES = ['gray', 'RGB']
        self.FILTERS = ['Low_Pass', 'High_Pass', 'Median', 'Laplacian']
        self.Image_mode = "gray"
        self.filters_list.activated.connect(self.image_transformation)
        self.modes_list.activated.connect(self.image_transformation)

        self.original_img = None
        self.HSV_img = None
        self.dft_gray = None
        self.dft_RGB = None

    def load_original_image(self, image_path):

        BGR_img = cv2.imread(image_path)
        self.original_img = cv2.cvtColor(BGR_img, cv2.COLOR_BGR2RGB)
        self.HSV_img = cv2.cvtColor(BGR_img, cv2.COLOR_BGR2HSV)

        self.init_dft_gray(self.original_img)
        self.init_dft_RGB(self.original_img)
        self.image_transformation()

    def init_dft_gray(self, rgb_img):
        gray_img = cv2.cvtColor(rgb_img, cv2.COLOR_BGR2GRAY)
        dft_img = fft2(gray_img)
        self.dft_gray = fftshift(dft_img)

    def init_dft_RGB(self, rgb_img):
        HSV_img = cv2.cvtColor(rgb_img, cv2.COLOR_RGB2HSV)
        intensity = HSV_img[:, :, 2]
        dft_img = fft2(intensity)
        self.dft_RGB = fftshift(dft_img)

    def image_transformation(self):
        MODE = str(self.modes_list.currentText())
        FILTER = str(self.filters_list.currentText())
        print((MODE))
        print(FILTER)

        if FILTER == "Low_Pass":
            self.apply_low_pass_filter(MODE)
        elif FILTER == "High_Pass":
            self.apply_high_pass_filter(MODE)
        elif FILTER == "Median":
            self.apply_median_pass_filter(MODE)
        else:
            self.apply_laplacian_filter(MODE)

    def apply_low_pass_filter(self, MODE):

        if MODE == 'gray':

            radius = 30  # --------ratio from image
            mask = np.zeros(self.dft_gray.shape)


            cy = mask.shape[0] // 2
            cx = mask.shape[1] // 2

            cv2.circle(mask, (cx, cy), radius, (255, 255, 255), -1)[0]  # remove [0]

            filterd_dft = np.multiply(self.dft_gray, mask) / 255
            inv_shifit_dft = np.fft.ifftshift(filterd_dft)
            filterd_dft = 20 * np.log(np.abs(filterd_dft) + 1)
            dft_spectrum=20 * np.log(np.abs(self.dft_gray))

            img_filtered = np.fft.ifft2(inv_shifit_dft, axes=(0, 1))
            img_filtered = np.abs(img_filtered)
            print('applay lowpass:')

            self.draw(dft_spectrum, filterd_dft, self.original_img, img_filtered)


        else:
            radius = 30  # --------ratio from image
            mask = np.zeros(self.dft_RGB.shape)

            cy = mask.shape[0] // 2
            cx = mask.shape[1] // 2

            cv2.circle(mask, (cx, cy), radius, (255, 255, 255), -1)[0]  # remove [0]

            filterd_dft = np.multiply(self.dft_RGB, mask) / 255
            inv_shifit_dft = np.fft.ifftshift(filterd_dft)
            filterd_dft = 20 * np.log(np.abs(filterd_dft) + 1)
            dft_spectrum=20 * np.log(np.abs(self.dft_RGB))

            img_filtered = np.abs(np.fft.ifft2(inv_shifit_dft, axes=(0, 1))).clip(0, 255).astype(np.uint8)
            img_filtered = np.dstack((self.HSV_img[:, :, 0], self.HSV_img[:, :, 1], img_filtered))
            img_filtered = cv2.cvtColor(img_filtered, cv2.COLOR_HSV2RGB)

            self.draw(dft_spectrum, filterd_dft, self.original_img, img_filtered)


    def apply_high_pass_filter(self, MODE):
        if MODE == 'gray':

            radius = 30  # --------ratio from image
            mask = np.ones(self.dft_gray.shape)
            print('applay lowpass:', mask)

            cy = mask.shape[0] // 2
            cx = mask.shape[1] // 2

            cv2.circle(mask, (cx, cy), radius, (0, 0, 0), -1)[0]  # remove [0]

            filterd_dft = np.multiply(self.dft_gray, mask)
            inv_shifit_dft = np.fft.ifftshift(filterd_dft)

            filterd_dft = 20 * np.log(np.abs(filterd_dft) + 1)
            dft_spectrum=20 * np.log(np.abs(self.dft_gray))


            img_filtered = np.fft.ifft2(inv_shifit_dft, axes=(0, 1))
            img_filtered = np.abs(img_filtered)
            print('applay lowpass:')

            self.draw(dft_spectrum, filterd_dft, self.original_img, img_filtered)


        else:
            radius = 30  # --------ratio from image
            mask = np.ones(self.dft_RGB.shape)

            cy = mask.shape[0] // 2
            cx = mask.shape[1] // 2

            cv2.circle(mask, (cx, cy), radius, (0, 0, 0), -1)[0]  # remove [0]

            filterd_dft = np.multiply(self.dft_RGB, mask)
            inv_shifit_dft = np.fft.ifftshift(filterd_dft)
            filterd_dft = 20 * np.log(np.abs(filterd_dft) + 1)
            dft_spectrum=20 * np.log(np.abs(self.dft_RGB))

            img_filtered = np.abs(np.fft.ifft2(inv_shifit_dft, axes=(0, 1))).clip(0, 255).astype(np.uint8)
            img_filtered = np.dstack((self.HSV_img[:, :, 0], self.HSV_img[:, :, 1], img_filtered))

            img_filtered = cv2.cvtColor(img_filtered, cv2.COLOR_HSV2RGB)
            print('applay highpass RGB:')

            self.draw(dft_spectrum, filterd_dft, self.original_img, img_filtered)

    def apply_median_pass_filter(self, MODE):

        if MODE == 'gray':

            gray_img= cv2.cvtColor(self.original_img, cv2.COLOR_BGR2GRAY)
            medianfilter_image = cv2.medianBlur(gray_img, 3)

            ## draw fft of image
            dft_img= np.fft.fft2(gray_img)
            dft_img = np.fft.fftshift(dft_img)
            magnitude_spectrum = 20 * np.log(np.abs(dft_img))


            # draw filtered fft
            filterd_dft = np.fft.fft2(medianfilter_image)
            filterd_dft = np.fft.fftshift(filterd_dft)
            magnitude_spectrum_filter = 20 * np.log(np.abs(filterd_dft))

            self.dft_image.draw_image(magnitude_spectrum)
            self.filtered_image.draw_image(medianfilter_image)
            self.filtered_dft.draw_image(magnitude_spectrum_filter)
        else:
            HSV_img = cv2.cvtColor(self.original_img, cv2.COLOR_RGB2HSV)
            dft_img = np.fft.fft2(HSV_img[:,:,-1])
            dft_img = np.fft.fftshift(dft_img)
            magnitude_spectrum = 20 * np.log(np.abs(dft_img))

            medianfilter_image = cv2.medianBlur(HSV_img, 3)
            filterd_dft = np.fft.fft2(medianfilter_image[:,:,-1])
            filterd_dft = np.fft.fftshift(filterd_dft)
            magnitude_spectrum_filter = 20 * np.log(np.abs(filterd_dft))

            medianfilter_image = cv2.cvtColor(medianfilter_image, cv2.COLOR_HSV2RGB)
            self.draw(magnitude_spectrum, magnitude_spectrum_filter, self.original_img, medianfilter_image)



    def apply_laplacian_filter(self, MODE):



        gray_img= cv2.cvtColor(self.original_img, cv2.COLOR_BGR2GRAY)
        filtered_img =  cv2.Laplacian(gray_img,cv2.CV_64F ,ksize =5)

        laplacian_spectrum = np.log(np.abs(self.dft_gray) + 1)
         # filtered dft
        filterd_dft = np.fft.fft2(filtered_img)
        filterd_dft = np.fft.fftshift(filterd_dft)
        laplacian_spectrum_filtered = 20 * np.log(np.abs(filterd_dft) + 1)



        self.draw(laplacian_spectrum,laplacian_spectrum_filtered,self.original_img,filtered_img)




    def draw(self,spectrum,filtered_spectrum,original_image,filtered_image):


        self.dft_image.draw_image(spectrum)
        self.filtered_dft.draw_image(filtered_spectrum)

        self.original_image.draw_image(original_image)


        self.filtered_image.draw_image(filtered_image)