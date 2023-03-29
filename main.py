import os
import cv2
from PyQt5.QtWidgets import *
from PyQt5 import uic, QtGui
from PyQt5.QtCore import Qt
import shutil


class MyGUI(QMainWindow):

    def __init__(self):
        self.flag = False
        self.scale_w = 340
        self.scale_h = 270
        self.current_file_2 = "default.png"
        super(MyGUI, self).__init__()
        uic.loadUi("imageviewer.ui", self)
        self.show()
        self.root_dir_path = ""
        self.back_data_path = ""
        self.model_name = ""
        pixmap_2 = QtGui.QPixmap(self.current_file_2)
        pixmap_2 = pixmap_2.scaled(self.width(), self.height(), aspectRatioMode=Qt.KeepAspectRatio)
        self.label_8.setPixmap(pixmap_2)
        self.label_8.setMinimumSize(1, 1)

    def resizeEvent(self, event):
        # Root_Dir 경로 선택
        self.pushButton.clicked.connect(self.open_directory)
        # Back_Data 경로 선택
        self.pushButton_2.clicked.connect(self.open_directory2)

        # row, column 입력 기능
        self.pushButton_4.clicked.connect(self.row_col_pressed)
        # cropping시 파일 선택(jpg, png)
        self.pushButton_5.clicked.connect(self.open_image_crop)
        # Cropping 작업 기능
        self.pushButton_6.clicked.connect(self.return_pressed)

        # Generate
        self.pushButton_3.clicked.connect(self.automation)

    def copy_backdata(self, backdata_dir, result_dir, model_name):
        # check file validation
        li1 = os.listdir(os.path.join(backdata_dir, "1CAM"))
        li2 = os.listdir(os.path.join(backdata_dir, "2CAM"))
        li3 = os.listdir(os.path.join(backdata_dir, "3CAM"))

        if len(li1) == len(li2) == len(li3) == 12:
            # model_name_folder create
            model_name_folder_path = os.path.join(result_dir, model_name)
            if os.path.exists(model_name_folder_path):
                shutil.rmtree(model_name_folder_path, ignore_errors=True)
                os.mkdir(model_name_folder_path)
                self.label_3.setText(f"{model_name} 폴더가 생성되었습니다.")
            else:
                os.mkdir(model_name_folder_path)
                self.label_3.setText(f"{model_name} 폴더가 생성되었습니다.")

            # copy backdata
            if os.path.exists(os.path.join(model_name_folder_path, "1CAM")):
                shutil.rmtree(os.path.join(model_name_folder_path, "1CAM"), ignore_errors=True)
            if os.path.exists(os.path.join(model_name_folder_path, "2CAM")):
                shutil.rmtree(os.path.join(model_name_folder_path, "2CAM"), ignore_errors=True)
            if os.path.exists(os.path.join(model_name_folder_path, "3CAM")):
                shutil.rmtree(os.path.join(model_name_folder_path, "3CAM"), ignore_errors=True)

            shutil.copytree(os.path.join(backdata_dir, "1CAM"), os.path.join(model_name_folder_path, "1CAM"))
            shutil.copytree(os.path.join(backdata_dir, "2CAM"), os.path.join(model_name_folder_path, "2CAM"))
            shutil.copytree(os.path.join(backdata_dir, "3CAM"), os.path.join(model_name_folder_path, "3CAM"))
            self.label_4.setText("Backdata 복제가 완료되었습니다.")
            return 0

        else:
            QMessageBox.warning(self, "Error", f"Backdata를 다시 확인해주세요. (각 카메라 폴더당 12개)\n"
                                               f"현재 Backdata 수 -> 1CAM: {len(li1)}, 2CAM: {len(li2)}, 3CAM: {len(li3)}")
            return

    def sum_img(self, root_dir, model_name):
        mode_type = ["Normal", "GlossRatio"]
        subdir = ["1CAM", "2CAM", "3CAM"]

        gloss = list()
        normal = list()
        for i in range(len(subdir)):
            target_dir = os.path.join(root_dir, subdir[i])
            for n in os.listdir(target_dir):
                mode = n.split('.')[0].split('_')[-1]
                if mode == mode_type[0]:
                    normal.append(os.path.join(target_dir, n))
                else:
                    gloss.append(os.path.join(target_dir, n))

        normal.sort()
        gloss.sort()

        # concat normal images
        h_img = list()
        for i in range(3):
            v_img = list()
            for j in range(6):
                idx = i * 6 + j
                v_img.append(cv2.imread(normal[idx]))
            img = cv2.vconcat(v_img)
            h_img.append(img)

        normal_img = cv2.hconcat([h_img[2], h_img[1], h_img[0]])
        # plt.imshow(normal_img)
        cv2.imwrite(os.path.join(root_dir, f"{model_name}_normal.jpg"), normal_img)

        h_img = list()
        for i in range(3):
            v_img = list()
            for j in range(6):
                idx = i * 6 + j
                v_img.append(cv2.imread(gloss[idx]))
            img = cv2.vconcat(v_img)
            h_img.append(img)

        gloss_img = cv2.hconcat([h_img[2], h_img[1], h_img[0]])
        cv2.imwrite(os.path.join(root_dir, f"{model_name}_gloss.jpg"), gloss_img)
        self.label_5.setText("이미지 병합이 완료되었습니다.")

    def default_segmentation(self, model_name_folder_path, img_path, model_name, mode):
        col = 4
        row = 12
        dest_dir = os.path.join(model_name_folder_path, f"{model_name}_{mode}_default_{col * row}cuts")
        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir)

        img = cv2.imread(img_path)
        h, w, _ = img.shape

        s_w = int(w / col)
        s_h = int(h / row)
        for n in range(1, (col * row) + 1):
            x1 = int(((n - 1) % col) * s_w)
            y1 = int(((n - 1) // col) * s_h)
            x2 = x1 + s_w
            y2 = y1 + s_h

            roi = img[y1:y2, x1:x2]
            cv2.imwrite(os.path.join(dest_dir, f"{n}_mode.jpg"), roi)
        self.label_6.setText("이미지 자르기가 완료되었습니다.")

    def erase_backdata(self, backdata_dir):
        shutil.rmtree(os.path.join(backdata_dir, "1CAM"), ignore_errors=True)
        shutil.rmtree(os.path.join(backdata_dir, "2CAM"), ignore_errors=True)
        shutil.rmtree(os.path.join(backdata_dir, "3CAM"), ignore_errors=True)

        os.mkdir(os.path.join(backdata_dir, "1CAM"))
        os.mkdir(os.path.join(backdata_dir, "2CAM"))
        os.mkdir(os.path.join(backdata_dir, "3CAM"))

    def automation(self):
        self.label_3.setText("")
        self.label_4.setText("")
        self.label_5.setText("")
        self.label_6.setText("")

        model_name = self.lineEdit.text()
        if model_name == "모델명 입력" or not model_name:
            QMessageBox.warning(self, "Error", "모델명을 확인해주세요.")
            return
        if self.root_dir_path == "":
            QMessageBox.warning(self, "Error", "결과 이미지 생성 경로를 선택해주세요")
            return
        if self.back_data_path == "":
            QMessageBox.warning(self, "Error", "Backdata를 선택해주세요")
            return


        # copy backdata to result_dir
        copy_check = self.copy_backdata(self.back_data_path, self.root_dir_path, model_name)

        model_name_folder_path = os.path.join(self.root_dir_path, model_name)
        if copy_check == 0:
            self.erase_backdata(self.back_data_path)

            self.sum_img(model_name_folder_path, model_name)

            normal_img = os.path.join(model_name_folder_path, f"{model_name}_normal.jpg")
            gloss_img = os.path.join(model_name_folder_path, f"{model_name}_gloss.jpg")
            self.default_segmentation(model_name_folder_path, normal_img, model_name, "normal")
            self.default_segmentation(model_name_folder_path, gloss_img, model_name, "gloss")

    def open_image_crop(self):
        options = QFileDialog.Options()
        filename, _ = QFileDialog.getOpenFileName(self, "Open File", "", "Image Files (*.png, *.jpg)", options=options)
        if filename == "":
            QMessageBox.warning(self, "Error", "이미지가 선택되지 않았습니다.")
            
        if filename != "":
            self.current_file_2 = filename
            pixmap_2 = QtGui.QPixmap(self.current_file_2)
            pixmap_2 = pixmap_2.scaled(self.scale_w, self.scale_h, aspectRatioMode=Qt.KeepAspectRatio)
            self.label_8.setPixmap(pixmap_2)
        return

    def row_col_pressed(self):
        self.row = self.lineEdit_2.text()
        self.col = self.lineEdit_3.text()
        self.label_7.setText(f"가로: {self.row}, 세로: {self.col}")

        if not self.row.isdigit() or not self.col.isdigit():
            QMessageBox.warning(self, "Error", "가로와 세로는 숫자여야합니다.")
            return
        self.flag = True

    def return_pressed(self):
        if not self.flag:
            QMessageBox.warning(self, "Error", "입력 버튼을 눌러주세요.")
            return

        row = int(self.row)
        col = int(self.col)
        if row == 1 and col == 1:
            QMessageBox.warning(self, "Error", "가로:1, 세로:1은 불가능합니다.")
            return
        img_path = self.current_file_2

        p_path = self.parent_path(self.current_file_2)

        dest_dir = os.path.join(p_path, f"{col}_{row}_{col * row}cuts")
        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir)

        img = cv2.imread(img_path)
        h, w, _ = img.shape

        s_w = int(w / col)
        s_h = int(h / row)
        for n in range(1, (col * row) + 1):
            x1 = int(((n - 1) % col) * s_w)
            y1 = int(((n - 1) // col) * s_h)
            x2 = x1 + s_w
            y2 = y1 + s_h
            roi = img[y1:y2, x1:x2]
            tmp = dest_dir + "/" + f"{n}_cv.jpg"
            cv2.imwrite(tmp, roi)
        self.label_7.setText("파일이 생성되었습니다.")

    def open_directory(self):
        directory = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        if directory == "":
            QMessageBox.warning(self, "Error", "폴더 선택이 되지 않았습니다.")
            return
        self.label.setText(directory)
        self.root_dir_path = directory

    def open_directory2(self):
        directory = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        if directory == "":
            QMessageBox.warning(self, "Error", "폴더 선택이 되지 않았습니다.")
            return
        self.label_2.setText(directory)
        self.back_data_path = directory

    def parent_path(self, f_path):
        if not f_path:
            return
        tmp = list(f_path.split('/'))
        return "/".join(tmp[:len(tmp)-1]) + "/"


def main():
    app = QApplication([])
    window = MyGUI()
    app.exec_()


if __name__ == "__main__":
    main()