import matplotlib as matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as navigation_toolbar
from matplotlib.figure import Figure
plt.style.use('dark_background')
matplotlib.use('Qt5Agg')



class Viewer(FigureCanvas):

    def __init__(self, parent=None, width=0.1, height=0.01, dpi=100):
        self.fig = Figure()
        super().__init__(self.fig) 
        self.axes = self.fig.add_subplot(111)
        for spine in ['right', 'top', 'left', 'bottom']:
            self.axes.spines[spine].set_color('gray')
        # self.axes.tick_params(left=False, bottom=False, labelleft=False, labelbottom=False)
        # self.fig.tight_layout()
        self.axes.axis('off')
        # self.cmap = plt.get_cmap('inferno')

    def draw_image(self,img):
        self.axes.imshow(img)
        self.draw()

    def update_image(self, img):
        self.axes.imshow(img)
        self.draw()


    def clear_canvans(self):
        self.axes.clear()
        self.draw()

    def draw_histogram(self, img):
        pass 