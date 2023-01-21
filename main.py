import os
from PyQt5.QtWidgets import *
from PyQt5 import uic, QtGui
import cv2


class MyGUI(QMainWindow):

    def __init__(self):
        super(MyGUI, self).__init__()
        uic.loadUi("imageviewer.ui", self)
        self.show()
        self.current_file = "default.png"
        pixmap = QtGui.QPixmap(self.current_file)
        # pixmap = pixmap.scaled(self.width(), self.height())
        self.label.setPixmap(pixmap)
        self.label.setMinimumSize(1, 1)

    def resizeEvent(self, event):
        try:
            pixmap = QtGui.QPixmap(self.current_file)
        except:
            pixmap = QtGui.QPixmap("default.png")
        # pixmap = pixmap.scaled(self.width(), self.height())
        self.label.setPixmap(pixmap)
        self.label.resize(self.width(), self.height())
        self.file_list = None
        self.file_counter = None
        # 개별 이미지 조회
        self.actionOpen_Image.triggered.connect(self.open_image)
        # 폴더별 이미지 조회
        self.actionOpen_Directory.triggered.connect(self.open_directory)
        # "<" 버튼
        self.pushButton_2.clicked.connect(self.previous_image)
        # ">" 버튼
        self.pushButton.clicked.connect(self.next_image)
        # "View File List" 버튼
        self.pushButton_3.clicked.connect(self.show_list)

    def open_image(self):
        self.listWidget.clear()
        self.file_list = list()
        options = QFileDialog.Options()
        filename, _ = QFileDialog.getOpenFileName(self, "Open File", "", "Image Files (*.png, *.jpg)", options=options)
        if filename != "":
            self.current_file = filename
            pixmap = QtGui.QPixmap(self.current_file)
            # pixmap = pixmap.scaled(self.width(), self.height())
            self.label.setPixmap(pixmap)

    def open_directory(self):
        directory = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        self.file_list = [directory + "/" + str(f) + "_cv.jpg" for f in range(1, len(os.listdir(directory)) + 1)]
        self.file_counter = 0
        self.current_file = self.file_list[self.file_counter]
        pixmap = QtGui.QPixmap(self.current_file)
        # pixmap = pixmap.scaled(self.width(), self.height())
        self.label.setPixmap(pixmap)

    def crop(self):
        options = QFileDialog.Options()
        filename, _ = QFileDialog.getOpenFileName(self, "Open File", "", "Image Files (*.png, *.jpg)", options=options)
        if filename != "":
            self.current_file = filename
            pixmap = QtGui.QPixmap(self.current_file)
            # pixmap = pixmap.scaled(self.width(), self.height())
            self.label.setPixmap(pixmap)

    def next_image(self):
        if self.file_counter is not None and self.file_list:
            self.file_counter += 1
            self.file_counter %= len(self.file_list)
            self.current_file = self.file_list[self.file_counter]
            pixmap = QtGui.QPixmap(self.current_file)
            # pixmap = pixmap.scaled(self.width(), self.height())
            self.label.setPixmap(pixmap)
            self.label_2.setText(self.current_file)

    def previous_image(self):
        if self.file_counter is not None and self.file_list:
            self.file_counter -= 1
            self.file_counter %= len(self.file_list)
            self.current_file = self.file_list[self.file_counter]
            pixmap = QtGui.QPixmap(self.current_file)
            # pixmap = pixmap.scaled(self.width(), self.height())
            self.label.setPixmap(pixmap)
            self.label_2.setText(self.current_file)

    def show_list(self):
        self.listWidget.clear()
        self.count = 0
        if self.file_list is not None:
            for item in self.file_list:
                self.listWidget.insertItem(self.count, item)
                self.count += 1
        self.label_2.setText(self.current_file)


def main():
    app = QApplication([])
    window = MyGUI()
    app.exec_()


def cropping_img(img_path, col, row):
    dest_dir = os.path.join('./', f"{col}_{row}_{col * row}cuts")
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    img = cv2.imread(img_path)
    h, w, _ = img.shape

    s_w = int(w / col)
    s_h = int(h / row)
    print(f"crop image size = {s_w}x{s_h}")

    for n in range(1, (col * row) + 1):
        x1 = int(((n - 1) % col) * s_w)
        y1 = int(((n - 1) // col) * s_h)
        x2 = x1 + s_w
        y2 = y1 + s_h
        print(f"{n} roi : ({x1}, {y1}), ({x2}, {y2})")

        roi = img[y1:y2, x1:x2]
        cv2.imwrite(os.path.join(dest_dir, f"{n}_cv.jpg"), roi)


if __name__ == "__main__":
    main()