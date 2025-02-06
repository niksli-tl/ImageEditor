from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QTextEdit, QLineEdit, \
    QListWidget, QMessageBox, QFileDialog
import os
from PIL import Image , ImageEnhance , ImageFilter

workdir = ''
class ImageProcessor:
    def __init__(self):
        self.image = None
        self.filename = None
        self.pixmap = None
        self.path = None

    def load_image(self, filename):
        self.path = os.path.join(workdir, filename)
        self.pixmap = QPixmap(self.path)
        self.image = Image.open(self.path)
        w, h = picture.width(), picture.height()
        self.pixmap = self.pixmap.scaled(w, h, Qt.AspectRatioMode.KeepAspectRatio)

    def reload_file(self):
        self.path = os.path.join(workdir, 'temp.png')
        self.image.save(self.path)
        self.pixmap = QPixmap(self.path)
        w, h = picture.width(), picture.height()
        self.pixmap = self.pixmap.scaled(w, h, Qt.AspectRatioMode.KeepAspectRatio)
        os.remove(self.path)

    def show_image(self):
        picture.hide()
        picture.setPixmap(self.pixmap)
        picture.show()

    def wb_image(self):
        self.image = self.image.convert('L')
        self.reload_file()
        self.show_image()

    def do_left(self):
        self.image = self.image.transpose(Image.ROTATE_90)
        self.reload_file()
        self.show_image()

    def do_right(self):
        self.image = self.image.transpose(Image.ROTATE_270)
        self.reload_file()
        self.show_image()

    def do_mirrow(self):
        self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
        self.reload_file()
        self.show_image()

    def do_sharpness(self):
        self.image = ImageEnhance.Sharpness(self.image)
        self.image = self.image.enhance(5)
        self.reload_file()
        self.show_image()

    def do_blured(self):
        self.image = self.image.filter(ImageFilter.BLUR)
        self.reload_file()
        self.show_image()

    def do_contrast(self):
        self.image = ImageEnhance.Contrast(self.image)
        self.image = self.image.enhance(1.5)
        self.reload_file()
        self.show_image()

    def do_emboss(self):
        self.image = self.image.filter(ImageFilter.EMBOSS)
        self.reload_file()
        self.show_image()

    def do_smooth(self):
        self.image = self.image.filter(ImageFilter.SMOOTH)
        self.reload_file()
        self.show_image()

    def box_blur(self):
        self.image = self.image.filter(ImageFilter.BoxBlur(radius=5))
        self.reload_file()
        self.show_image()

    def do_contour(self):
        self.image = self.image.filter(ImageFilter.CONTOUR)
        self.reload_file()
        self.show_image()

    def save(self,path):
        self.image.save(path)



workimage = ImageProcessor()
app = QApplication([])
main_win = QWidget()
main_win.setWindowTitle('SmartNotes')
main_win.setFixedSize(800, 600)

layout_main = QHBoxLayout()
layout_v1 = QVBoxLayout()
layout_v2 = QVBoxLayout()
layout_h_sup1 = QHBoxLayout()
layout_h_sup2 = QHBoxLayout()
folder_button = QPushButton('FOLDER')
picture = QLabel('PICTURE')
list_item = QListWidget()
left_button = QPushButton('LEFT')
right_button = QPushButton('RIGHT')
mirror_button = QPushButton('MIRROR')
sharp_button = QPushButton('SHARPNESS')
bw_button = QPushButton('B/W')
blur_button = QPushButton('BLUR')
contrast_button = QPushButton('CONTRAST')
emboss_button = QPushButton('EMBOSS')
edges_button = QPushButton('SMOOTH')
box_blur_button = QPushButton('BOX_BLUR')
contour_button = QPushButton('CONTOUR')
save_button = QPushButton('SAVE PICTURE')
save_button.setStyleSheet("background-color : green; color : white ; font : bold")

layout_v1.addWidget(folder_button)
layout_v1.addWidget(list_item)
layout_h_sup1.addWidget(left_button)
layout_h_sup1.addWidget(right_button)
layout_h_sup1.addWidget(mirror_button)
layout_h_sup1.addWidget(sharp_button)
layout_h_sup1.addWidget(bw_button)
layout_h_sup1.addWidget(blur_button)
layout_h_sup2.addWidget(contrast_button)
layout_h_sup2.addWidget(emboss_button)
layout_h_sup2.addWidget(edges_button)
layout_h_sup2.addWidget(box_blur_button)
layout_h_sup2.addWidget(contour_button)
layout_h_sup2.addWidget(save_button)
layout_v2.addWidget(picture)
layout_v2.addLayout(layout_h_sup1)
layout_v2.addLayout(layout_h_sup2)

layout_main.addLayout(layout_v1)
layout_main.addLayout(layout_v2)
main_win.setLayout(layout_main)

def choose_workdir():
    global workdir
    workdir = QFileDialog.getExistingDirectory()

def filter(files, extensions):
    result = []
    for filename in files:
        for extension in extensions:
            if filename.endswith(extension):
                result.append(filename)
    return result

def show_filenames_list():
    choose_workdir()
    files = os.listdir(workdir)
    extensions = ['.png','.jpeg','.jpg','.bmp']
    result = filter(files,extensions)
    list_item.clear()
    list_item.addItems(result)

def show_selected_image():
    if len(list_item.selectedItems()) == 0:
        msg = QMessageBox()
        msg.setWindowTitle('Ошибка')
        msg.setText('Выделите нужный файл')
        msg.exec()
        return
    filename = list_item.selectedItems()[0].text()
    workimage.load_image(filename)
    workimage.show_image()

def save_file():
    file, _ = QFileDialog.getSaveFileName()
    workimage.save(file)

contour_button.clicked.connect(workimage.do_contour)
box_blur_button.clicked.connect(workimage.box_blur)
edges_button.clicked.connect(workimage.do_smooth)
save_button.clicked.connect(save_file)
emboss_button.clicked.connect(workimage.do_emboss)
contrast_button.clicked.connect(workimage.do_contrast)
blur_button.clicked.connect(workimage.do_blured)
left_button.clicked.connect(workimage.do_left)
right_button.clicked.connect(workimage.do_right)
mirror_button.clicked.connect(workimage.do_mirrow)
sharp_button.clicked.connect(workimage.do_sharpness)
bw_button.clicked.connect(workimage.wb_image)
list_item.itemClicked.connect(show_selected_image)
folder_button.clicked.connect(show_filenames_list)
main_win.show()
app.exec()