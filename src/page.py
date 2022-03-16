from calendar import c
from PyQt5 import QtCore as qtc
from PyQt5 import QtWidgets as qtw
from PyQt5 import uic

from filtering_studio import FilterStudio
from equalization import Equalizer

class Page (qtw.QTabWidget):
    def __init__ (self):
        super().__init__()

        uic.loadUi("src/ui/page.ui", self)

        
        self.filter_studio = FilterStudio()
        self.equalizer = Equalizer()


        self.filter_layout.addWidget(self.filter_studio)
        self.equalizer_layout.addWidget(self.equalizer)

    def load_image(self, image_path):
        self.filter_studio.load_original_image(image_path)
        self.equalizer.load_original_image(image_path)
        

        