#!/usr/bin/env python3


#Running command in terminal: python3 CVHW2.py

from PIL import Image
import numpy as np
from math import pi, exp
import sys
import matplotlib.pyplot as plt
from PIL import Image
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QHBoxLayout, QWidget, QPushButton, QAction, QGroupBox, QLabel, QVBoxLayout, QFileDialog
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QImage
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.image as mpimg


image = np.zeros((1,1))

class main_window(QMainWindow):
    
    def __init__(self):
        super().__init__()
        self.open_window()

    def open_window(self):
     
        layout = QHBoxLayout(self)
        self.setLayout(layout)
        
        menubar = self.menuBar()

        file_menu = menubar.addMenu('File') 

        open_input = QAction('Open', self)  
        file_menu.addAction(open_input)

        self.input_label = QLabel(self)
        open_input.triggered.connect(self.open_input_image) #open_input_image function will be called when Open Input is clicked.
        
        save = QAction('Save', self)
        file_menu.addAction(save)
        save.triggered.connect(self.save_image)  

        exit_program = QAction('Exit', self)
        file_menu.addAction(exit_program)
        exit_program.triggered.connect(self.exit_prog) #Exit element has connected with exit_prog function, thus this function will be called when Exit is clicked.

        filters_menu = menubar.addMenu('Filters')
        average = filters_menu.addMenu('Average Filters')
        a = []   
        gaussian = filters_menu.addMenu('Gaussian Filters') 
        g = []
        median = filters_menu.addMenu('Median Filters')
        m = []

        x = 0
        i = 3
        while (i<16):
            a.append(QAction(str(i) + ' x ' + str(i), self))
            average.addAction(a[x])
            g.append(QAction(str(i) + ' x ' + str(i), self))
            gaussian.addAction(g[x])
            m.append(QAction(str(i) + ' x ' + str(i), self))
            median.addAction(m[x])
            i = i + 2
            x = x + 1
		
        a[0].triggered.connect(lambda: self.average_filtering(3))
        a[1].triggered.connect(lambda: self.average_filtering(5))
        a[2].triggered.connect(lambda: self.average_filtering(7))
        a[3].triggered.connect(lambda: self.average_filtering(9))
        a[4].triggered.connect(lambda: self.average_filtering(11))
        a[5].triggered.connect(lambda: self.average_filtering(13))
        a[6].triggered.connect(lambda: self.average_filtering(15))

        g[0].triggered.connect(lambda: self.gaussian_filtering(3))
        g[1].triggered.connect(lambda: self.gaussian_filtering(5))
        g[2].triggered.connect(lambda: self.gaussian_filtering(7))
        g[3].triggered.connect(lambda: self.gaussian_filtering(9))
        g[4].triggered.connect(lambda: self.gaussian_filtering(11))
        g[5].triggered.connect(lambda: self.gaussian_filtering(13))
        g[6].triggered.connect(lambda: self.gaussian_filtering(15))

        m[0].triggered.connect(lambda: self.median_filtering(3))
        m[1].triggered.connect(lambda: self.median_filtering(5))
        m[2].triggered.connect(lambda: self.median_filtering(7))
        m[3].triggered.connect(lambda: self.median_filtering(9))
        m[4].triggered.connect(lambda: self.median_filtering(11))
        m[5].triggered.connect(lambda: self.median_filtering(13))
        m[6].triggered.connect(lambda: self.median_filtering(15))

        geometric_menu = menubar.addMenu('Geometric Transformations')

        rotate = geometric_menu.addMenu('Rotate') #Rotate submenu 
        rotate_10l = QAction('Rotate 10 degree left', self)
        rotate_10r = QAction('Rotate 10 degree right', self)
        rotate.addAction(rotate_10l)
        rotate.addAction(rotate_10r)
        rotate_10l.triggered.connect(lambda: self.rotation(np.pi/18)) #10 degrees left rotation
        rotate_10r.triggered.connect(lambda: self.rotation(-np.pi/18)) #10 degrees right rotation 

        scale = geometric_menu.addMenu('Scale') #Scale submenu 
        scale_2x = QAction('2x', self)
        scale_half = QAction('1/2 x', self)
        scale.addAction(scale_2x)
        scale.addAction(scale_half)
        scale_2x.triggered.connect(lambda: self.scale(2)) #2x scale
        scale_half.triggered.connect(lambda: self.scale(0.5)) #1/2x scale
        
        translate = geometric_menu.addMenu('Translate') #Translate submenu
        translate_left = QAction('Left', self)
        translate_right = QAction('Rİght', self)
        translate.addAction(translate_left)
        translate.addAction(translate_right)
        translate_left.triggered.connect(lambda: self.translation(-1)) #Left translate
        translate_right.triggered.connect(lambda: self.translation(1)) #Right translate


        self.setGeometry(10, 10, 500, 750) #Size of initial window is determined.
        self.setWindowTitle('Filtering & Geometric Transformations')  
        self.show() 

    def exit_prog(self):
        sys.exit() #When exit is clicked, program is closed

    def open_input_image(self, k):

        global image

        path,_ = QFileDialog.getOpenFileName() #Browse the files in order to select input image and take its path.
        
        img = Image.open(path)
        img = np.array(img)

        image = img[:,:,0:3]

        self.input_preview = QPixmap(path)
        self.input_label.move((500 - image.shape[1])//2,(750 - image.shape[0])//2)
        self.input_label.resize(self.input_preview.width(), self.input_preview.height())
        self.input_label.setPixmap(self.input_preview) #Place of the image is prepared.

    def average_filtering(self, size):

        global image
        
        [height, width, channel] = image.shape
        image_filter = np.zeros((size, size, channel))
        image_filter = image_filter + 1/size**2

        img = np.zeros((height + (size - 1) , width + (size - 1), channel))
        padding = int((size-1)/2)
        img[padding:padding+height, padding:padding+ width, :] = image #Padding
        output = np.zeros((height, width, channel))
         
        for i in range(0, height):
            for j in range (0, width):
                  output[i][j] = np.sum(np.sum(img[i:(i+size), j:(j+size)]*image_filter, 0),0)
        
        image = output
        self.show_image()

    def gaussian_filtering(self, size):

        global image
        [height, width, channel] = image.shape
        sigma = 5
        image_filter = np.zeros((size, size, channel))

        img = np.zeros((height + (size - 1) , width + (size - 1), channel))
        padding = int((size-1)/2)
        img[padding:padding+height, padding:padding+ width, :] = image #Padding
        output = np.zeros((height, width, channel))

        for i in range (-1*(size//2), size//2 + 1): #Gaussian filter is calculated according to formula
            for j in range (-1*(size//2), size//2 + 1):
                image_filter[i+size//2][j+size//2] = exp(-1*(i**2 + j**2)/(2*sigma**2))/(2*pi*sigma**2)
        
        #Filter is divided by the sum of the elements in the filter in order to avoid overgrowth of the pixel values
        image_filter = image_filter/np.sum(image_filter[:,:,0])
      
        for i in range(0, output.shape[0]):
            for j in range (0, output.shape[1]):
                output[i][j] = np.sum(np.sum(img[i:(i+size), j:(j+size)]*image_filter, 0),0)
        
        image = output
        self.show_image()

    def median_filtering(self, size):

        global image
        
        [height, width, channel] = image.shape
        img = np.zeros((height + (size - 1) , width + (size - 1), channel))
        padding = int((size-1)/2)
        img[padding:padding+height, padding:padding+ width, :] = image #Padding
        output = np.zeros((height, width, channel))

        for i in range(0, output.shape[0]):
            for j in range (0, output.shape[1]):
                for k in range (0, output.shape[2]):
                       temp = img[i:(i+size), j:(j+size), k].reshape(1, size**2)
                       temp = np.squeeze(temp)
                       temp = np.sort(temp) #Sorting pixel values
                       output[i][j][k] = temp[size**2//2+1] #Get the middle value
        
        image = output
        self.show_image()

    def rotation(self, degree):                                        
        
        global image
        img = image

        [height, width, dim] = img.shape
        
        x = width//2
        y = height//2
        center = np.array([[x],[y]])

        new_width = int(width * np.cos(abs(degree)) + height * np.sin(abs(degree))) #New image size 
        new_height = int(height * np.cos(abs(degree)) + width * np.sin(abs(degree)))
        output_center = np.array([[new_width//2],[new_height//2]]) #Center of the outpu image 

        output = np.zeros((new_height, new_width, dim))
        output = output + 240
        
        for i in range (0, new_height): #backward mapping
            for j in range (0, new_width):
                rotation = np.array([[np.cos(degree), np.sin(degree)],[-1*np.sin(degree), np.cos(degree)]])
                inverse_rotation = np.linalg.inv(rotation)
                new_coord = np.matmul(inverse_rotation, np.array([[j - output_center[0][0]],[i-output_center[1][0]]]))
                new_coord = new_coord + center
                if int(new_coord[0][0]) > 0 and int(new_coord[0][0]) < img.shape[1] and int(new_coord[1][0]) > 0 and int(new_coord[1][0]) < img.shape[0]:
                       output[i][j] = img[int(new_coord[1][0])][int(new_coord[0][0])] #Get the nearest value. Cannot implement bicubic interpolation

        image = output
        self.show_image()

    def scale(self, rate):
        
        global image

        img = image
  
        [height, width, dim] = img.shape
        
        x = width//2
        y = height//2
        center = np.array([y, x])

        new_height = int(height * rate)
        new_width = int(width * rate)

        output = np.zeros((new_height, new_width, img.shape[2]))
        output_center = np.array([new_height//2, new_width//2])
        
        
        for i in range (0, new_height): #backward mapping
            for j in range (0, new_width):
                coord = np.array([i,j])-output_center
                coord = coord/rate
                coord = coord + center
                if int(coord[0]) < img.shape[0] and int(coord[1]) < img.shape[1]:
                   output[i][j] = img[int(coord[0])][int(coord[1])] #Get the nearest value. Cannot implement bicubic interpolation

        image = output
        self.show_image()

    def translation(self, left_right):
        global image
        translation_amount = 20 * left_right
        img = image
        [height, width, channel] = img.shape
        output = np.zeros((height, width, channel))
        output = output + 240
        for i in range (0, height):
            for j in range (0, width):
                if j-translation_amount > 0 and j-translation_amount < width:
                     output[i][j] = img[i][j-translation_amount]

        image = output
        self.show_image()
  
    def show_image(self):
        global image

        image = np.int8(image)

        height, width, ch = image.shape #Displaying matrix image.
        BPL = ch * width
        qtimg = QImage(image.data, width, height, BPL, QImage.Format_RGB888)
        input_img = QPixmap.fromImage(qtimg)
        self.input_label.move((500 - image.shape[1])//2,(750 - image.shape[0])//2)
        
        self.input_label.setAlignment(Qt.AlignCenter)
        self.input_preview = QPixmap(input_img)
        self.input_label.resize(self.input_preview.width(), self.input_preview.height())
        self.input_label.setPixmap(self.input_preview)
        self.input_label.show()

    def save_image(self):
        global image
        image = np.int8(image)

        height, width, ch = image.shape
        BPL = ch * width
        qtimg = QImage(image.data, width, height, BPL, QImage.Format_RGB888)
        path,_ = QFileDialog.getSaveFileName()
        print(path)
        qtimg.save(path, "PNG") #Save as png
if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    window = main_window()
    sys.exit(app.exec_())


