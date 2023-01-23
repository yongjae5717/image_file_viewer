import os

import cv2
from PyQt5.QtWidgets import *
from PyQt5 import uic, QtGui


class MyGUI(QMainWindow):

    def __init__(self):
        super(MyGUI, self).__init__()
        uic.loadUi("imageviewer.ui", self)
        self.show()
        self.current_file = "default.png"
        self.current_file_2 = "default.png"
        pixmap = QtGui.QPixmap(self.current_file)
        pixmap_2 = QtGui.QPixmap(self.current_file_2)
        # pixmap = pixmap.scaled(self.width(), self.height())
        self.label.setPixmap(pixmap)
        self.label.setMinimumSize(1, 1)
        self.label_3.setPixmap(pixmap_2)
        self.label_3.setMinimumSize(1, 1)

    def resizeEvent(self, event):
        try:
            pixmap = QtGui.QPixmap(self.current_file)
        except:
            pixmap = QtGui.QPixmap("default.png")
        pixmap = pixmap.scaled(self.width(), self.height())
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
        # widget list에서 더블클릭시 파일 보여주기 기능
        self.listWidget.itemDoubleClicked.connect(self.click_image)
        self.pushButton_5.clicked.connect(self.open_image_crop)
        self.pushButton_4.clicked.connect(self.row_col_pressed)
        self.pushButton_6.clicked.connect(self.return_pressed)

    def click_image(self):
        filename = str(self.file_list[self.listWidget.currentRow()])
        if filename != "":
            self.current_file = filename
            pixmap = QtGui.QPixmap(self.current_file)
            # pixmap = pixmap.scaled(self.width(), self.height())
            self.label.setPixmap(pixmap)
            self.label_2.setText(self.current_file)

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


    def open_image_crop(self):
        self.listWidget.clear()
        self.file_list = list()
        options = QFileDialog.Options()
        filename, _ = QFileDialog.getOpenFileName(self, "Open File", "", "Image Files (*.png, *.jpg)", options=options)
        # print(filename)
        if filename != "":
            self.current_file2 = filename
            pixmap_2 = QtGui.QPixmap(self.current_file2)
            # pixmap = pixmap.scaled(self.width(), self.height())
            self.label_3.setPixmap(pixmap_2)

    def open_directory(self):
        directory = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        self.file_list = [directory + "/" + str(f) + "_cv.jpg" for f in range(1, len(os.listdir(directory)) + 1)]
        self.file_counter = 0
        self.current_file = self.file_list[self.file_counter]
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

    def row_col_pressed(self):
        self.row = self.lineEdit.text()
        self.col = self.lineEdit_2.text()
        self.label_4.setText(f"Row: {self.row}, Col: {self.col}")

    def return_pressed(self):
        row = int(self.row)
        col = int(self.col)
        img_path = self.current_file2
        print(row, col, img_path)

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


def main():
    app = QApplication([])
    window = MyGUI()
    app.exec_()


if __name__ == "__main__":
    main()