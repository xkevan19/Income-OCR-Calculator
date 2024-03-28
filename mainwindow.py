from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QPushButton, QLabel, QFileDialog, QWidget, QApplication
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap, QPainter, QColor, QIcon, QFont
import cv2
import easyocr
import os


class ImageProcessor:
    def __init__(self):
        self.reader = easyocr.Reader(['en'], gpu=False)

    def process_image(self, image_path):
        if not os.path.isfile(image_path):
            print("Error: The selected file does not exist.")
            return None

        try:
            img = cv2.imread(image_path)

            if img is None:
                raise Exception("Failed to load image.")
        except Exception as e:
            print("Error:", e)
            return None

        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        text_ = self.reader.readtext(img_rgb)

        total_salary = None

        for bbox, text, score in text_:
            if text == 'Total Salary':
                total_salary = text_[text_.index((bbox, text, score)) + 1][1]
                break

        return total_salary

    def process_images_and_calculate_income(self, image_paths):
        total_incomes = []

        for image_path in image_paths:
            total_salary = self.process_image(image_path)
            if total_salary is not None:
                total_incomes.append(float(total_salary.replace(',', '')))

        total_income = sum(total_incomes)
        return total_income


class ColoredButton(QPushButton):
    def __init__(self, text):
        super().__init__(text)
        self.setMouseTracking(True)  # Enable mouse tracking for hover effect
        self.setCursor(Qt.PointingHandCursor)  # Set cursor to pointing hand

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Determine the background color based on hover state
        if self.underMouse():
            color = QColor("#00cc00")  # Hover color
        else:
            color = QColor("#00ff00")  # Default color

        painter.setBrush(color)
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(self.rect(), 20, 20)

        # Draw the text
        painter.setPen(Qt.black)
        painter.drawText(self.rect(), Qt.AlignCenter, self.text())

    def enterEvent(self, event):
        self.update()

    def leaveEvent(self, event):
        self.update()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Income Calculator")
        self.setWindowIcon(QIcon("C:/Users/kevan/PycharmProjects/ocr-with-ui/app-icon.png"))
        self.setStyleSheet("background-color: black;")
        self.setFixedSize(599, 400)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        main_layout = QVBoxLayout(self.central_widget)
        main_layout.setAlignment(Qt.AlignCenter)

        label_layout = QVBoxLayout()
        label_layout.setAlignment(Qt.AlignCenter)
        label_layout.setSpacing(30)

        self.label = QLabel("Total Income: $0.00")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("font-size: 18px; color: #00ff00; padding: 10px; border: 2px solid #00ff00; border-radius: 10px;")
        self.label.setFont(QFont("Helvetica", 12))
        label_layout.addWidget(self.label)

        main_layout.addLayout(label_layout)
        main_layout.addSpacing(20)  # Add spacing between the label and the button

        self.select_button = ColoredButton("Select Images")
        self.select_button.setStyleSheet("color: black; padding: 10px 20px; border-radius: 5px;")
        self.select_button.setFont(QFont("Helvetica", 10))
        self.select_button.setFixedWidth(200)
        self.select_button.setFixedHeight(40)
        self.select_button.clicked.connect(self.select_images)
        main_layout.addWidget(self.select_button)

        self.image_processor = ImageProcessor()

        # Set background image
        self.set_background_image("C:/Users/kevan/PycharmProjects/ocr-with-ui/bg.jpg")

    def set_background_image(self, image_path):
        pixmap = QPixmap(image_path)
        self.central_widget.setStyleSheet(f"background-image: url({image_path}); background-position: center; background-repeat: no-repeat; background-color: black;")
        self.central_widget.setMinimumSize(pixmap.width(), pixmap.height())

    def select_images(self):
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.ExistingFiles)
        file_dialog.setNameFilter("Image files (*.png *.jpg *.jpeg)")

        if file_dialog.exec():
            image_paths = file_dialog.selectedFiles()
            total_income = self.image_processor.process_images_and_calculate_income(image_paths)
            self.label.setText(f"Total Income: ${total_income:.2f}")


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
