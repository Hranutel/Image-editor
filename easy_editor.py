from PyQt5.QtWidgets import QApplication,QWidget,QLabel,QHBoxLayout,QVBoxLayout,QListWidget,QFileDialog,QPushButton
import os
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from PIL import Image,ImageFilter,ImageEnhance

last_image = None
image_edited = None
original = None

app = QApplication([])
win = QWidget()
win.resize(1150, 700)
win.move(125,0)
win.setWindowTitle("Easy Editor")

label_image = QLabel("Картинка")
button_folder = QPushButton("Папка")
files = QListWidget()

button_left = QPushButton("Вліво")
button_right = QPushButton("Вправо")
button_flip = QPushButton("Дзеркально")
button_sharp = QPushButton("Різкість")
button_BW = QPushButton("Ч/Б")
button_save = QPushButton("Зберегти")
button_cancel = QPushButton("Відміна")

main_layout = QHBoxLayout()
colum1 = QVBoxLayout()
colum2 = QVBoxLayout()
colum1.addWidget(button_folder)
colum1.addWidget(files)
colum1.addWidget(button_save)
colum1.addWidget(button_cancel)
colum2.addStretch(1)
colum2.addWidget(label_image,95,alignment=Qt.AlignHCenter)
colum2.addStretch(1)

row_tools = QHBoxLayout()
row_tools.addWidget(button_left)
row_tools.addWidget(button_right)
row_tools.addWidget(button_flip)
row_tools.addWidget(button_sharp)
row_tools.addWidget(button_BW)
colum2.addLayout(row_tools)
colum2.addStretch(1)

main_layout.addLayout(colum1,20)
main_layout.addLayout(colum2,80)
win.setLayout(main_layout)

workdir = ""
def filter(files,extensions):
    result = []
    for file in files:
        for extension in extensions:
            if file.endswith(extension):
                result.append(file)
    return result
def choseWorkdir():
    global workdir
    try:
        workdir = QFileDialog.getExistingDirectory()
    except:
        pass
def showFilenamesList():
    extensions = [".jpg",".jpeg",".png",".bmp",".gif",".ico"]
    choseWorkdir()
    if workdir != "":
        file = filter(os.listdir(workdir), extensions)
        files.clear()
        for filenames in file:
            files.addItem(filenames)

def show_image():
    global last_image,original,rotate_degrees,image_edited
    label_image.hide()
    key = files.selectedItems()[0].text()
    if image_edited == None:
        image = QPixmap(f"{workdir}/{key}")
        image_edited = None
        last_image = f"{workdir}/{key}"
    else:
        button_folder.hide()
        files.hide()
        button_cancel.show()
        button_save.show()
        image = QPixmap(image_edited)

    if image.width() < 900 and image.height() < 900 and  image.width() > 100 and image.height() >100 : 
        label_image.resize(image.width(),image.height())
    elif image.width() < 100 and image.height() < 100:
        label_image.resize(350,350)
    elif image.width() >= 900 or image.width() <= 900 and image.height() >= 900:
        label_image.resize(900,625)
    image=image.scaled(label_image.width(),label_image.height(),1)
    label_image.setPixmap(image)
    image.scaled(label_image.width(),label_image.height(),1)
    label_image.show()

def rotate_left_or_right():
    if last_image != None:
        original = Image.open(last_image)
        if button_left.sender() == button_left :
            rotated =  original.rotate(90,expand=True)
        elif button_right.sender() == button_right:
            rotated = original.rotate(-90,expand=True)
        save_image(rotated)
        show_image()

def save_image(method):
    global image_edited,last_image
    # print(last_image.find("(1)"))
    if last_image.find("(1)") == -1:
        image = last_image.split("/")
        image=image[len(image)-1].split(".")
        image[0] = image[0] + "(1)."
        image = image[0]+image[1]
        image_edited =  f"{workdir}/{image}"
        method.save(image_edited)
        last_image = image_edited
        print(image_edited)
    else:
        image_edited = last_image
        method.save(last_image)

def add_image_to_files():
    global last_image,image_edited
    extensions = [".jpg",".jpeg",".png",".bmp",".gif",".ico"]
    file = filter(os.listdir(workdir), extensions)
    files.clear()
    for filenames in file:
        files.addItem(filenames)
    last_image = None
    image_edited = None
    button_cancel.hide()
    button_save.hide()
    files.show()
    label_image.setText("Картинка")

def remove_image():
    global last_image,image_edited
    os.remove(last_image)
    extensions = [".jpg",".jpeg",".png",".bmp",".gif",".ico"]
    file = filter(os.listdir(workdir), extensions)
    files.clear()
    for filenames in file:
        files.addItem(filenames)
    last_image = None
    image_edited = None
    button_cancel.hide()
    button_save.hide()
    files.show()
    label_image.setText("Картинка")
    
def convert_to_BW():
    if last_image != None:
        print(image_edited)
        original = Image.open(last_image)
        converted = original.convert("L")
        save_image(converted)
        show_image()

def flip_image():
    if last_image != None:
        original = Image.open(last_image)
        fliped = original.transpose(Image.FLIP_LEFT_RIGHT)
        save_image(fliped)
        show_image()

def contrast_image():
    if last_image!= None:
        original = Image.open(last_image)
        contrasted = ImageEnhance.Contrast(original)
        contrasted = contrasted.enhance(1.5)
        save_image(contrasted)
        show_image()


def main():
    button_cancel.hide()
    button_save.hide()
    button_sharp.clicked.connect(contrast_image)
    button_flip.clicked.connect(flip_image)
    button_BW.clicked.connect(convert_to_BW)
    button_right.clicked.connect(rotate_left_or_right)
    button_cancel.clicked.connect(remove_image)
    button_save.clicked.connect(add_image_to_files)
    button_left.clicked.connect(rotate_left_or_right)
    files.itemClicked.connect(show_image)
    button_folder.clicked.connect(showFilenamesList)
    win.show()
    app.exec()

if __name__ == "__main__":
    main()