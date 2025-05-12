#使用PyQt5和OpenCV实现一个简单的图像处理系统界面
import sys
import cv2
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget, QFileDialog
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt


class ImageProcessingApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("图像处理系统")
        self.setGeometry(100, 100, 800, 600)  # 设置窗口位置和大小

        # 创建中心部件
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # 创建布局
        self.layout = QVBoxLayout(self.central_widget)

        # 创建标签用于显示原始图像
        self.original_label = QLabel("原始图像", self)
        self.original_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.original_label)

        # 创建标签用于显示处理后的图像
        self.processed_label = QLabel("处理后的图像", self)
        self.processed_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.processed_label)

        # 创建按钮用于加载图像
        self.load_button = QPushButton("加载图像", self)
        self.layout.addWidget(self.load_button)
        self.load_button.clicked.connect(self.load_image)

        # 创建按钮用于处理图像
        self.process_button = QPushButton("灰度化处理", self)
        self.layout.addWidget(self.process_button)
        self.process_button.clicked.connect(self.process_image)

        # 创建按钮用于高斯模糊处理
        self.blur_button = QPushButton("高斯模糊", self)
        self.layout.addWidget(self.blur_button)
        self.blur_button.clicked.connect(self.blur_image)

        # 初始化图像变量
        self.original_image = None
        self.processed_image = None

    def load_image(self):
        """加载图像"""
        file_path, _ = QFileDialog.getOpenFileName(self, "选择图像文件", "", "Image Files (*.png *.jpg *.bmp *.gif)")
        if file_path:
            # 使用 OpenCV 加载图像
            self.original_image = cv2.imread(file_path)
            if self.original_image is not None:
                # 将 OpenCV 图像转换为 QPixmap 并显示
                self.display_image(self.original_label, self.original_image)

    def process_image(self):
        """对图像进行灰度化处理"""
        if self.original_image is not None:
            # 使用 OpenCV 进行灰度化处理
            self.processed_image = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2GRAY)
            # 将处理后的图像转换为 QPixmap 并显示
            self.display_image(self.processed_label, self.processed_image)

    def blur_image(self):
        """对图像进行高斯模糊处理"""
        if self.original_image is not None:
            # 使用 OpenCV 进行高斯模糊处理
            self.processed_image = cv2.GaussianBlur(self.original_image, (15, 15), 0)
            # 将处理后的图像转换为 QPixmap 并显示
            self.display_image(self.processed_label, self.processed_image)

    def display_image(self, label, image):
        """将 OpenCV 图像转换为 QPixmap 并显示在 QLabel 中"""
        if len(image.shape) == 3:  # 彩色图像
            height, width, channel = image.shape
            bytesPerLine = 3 * width
            qImg = QImage(image.data, width, height, bytesPerLine, QImage.Format_RGB888).rgbSwapped()
        else:  # 灰度图像
            height, width = image.shape
            bytesPerLine = width
            qImg = QImage(image.data, width, height, bytesPerLine, QImage.Format_Grayscale8)

        pixmap = QPixmap.fromImage(qImg)
        label.setPixmap(pixmap.scaled(400, 400, Qt.KeepAspectRatio))
        label.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)  # 创建应用程序对象
    window = ImageProcessingApp()  # 创建窗口实例
    window.show()  # 显示窗口
    sys.exit(app.exec_())  # 启动应用程序的事件循环