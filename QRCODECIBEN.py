import sys
import qrcode
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel, QFileDialog, QMessageBox, QMainWindow, QAction
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt
from PIL import Image

class QRCodeGenerator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QR Code Generator")
        self.setGeometry(100, 100, 400, 300)  # Increased height to accommodate larger image

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        layout = QVBoxLayout()

        # Add stretchable space at the top
        layout.addStretch(1)

        self.program_image_label = QLabel(self)
        program_image = QPixmap("D:\Development\PYTHON\lunbi.png")
        self.program_image_label.setPixmap(program_image.scaledToWidth(100))  # Resize image to 200 pixels wide
        self.program_image_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.program_image_label)

        # Adjust the layout to add some spacing
        layout.addSpacing(20)  # Adjust the spacing as needed

        self.link_input = QLineEdit(self)
        self.link_input.setPlaceholderText("Enter the link")
        layout.addWidget(self.link_input)

        self.logo_button = QPushButton("Select Logo", self)
        self.logo_button.clicked.connect(self.load_logo)
        layout.addWidget(self.logo_button)

        self.generate_button = QPushButton("Generate QR Code", self)
        self.generate_button.clicked.connect(self.generate_qr_code)
        layout.addWidget(self.generate_button)

        self.qr_image_label = QLabel(self)
        layout.addWidget(self.qr_image_label)

        self.save_button = QPushButton("Save QR Code", self)
        self.save_button.clicked.connect(self.save_qr_code)
        layout.addWidget(self.save_button)

        # Add stretchable space at the bottom
        layout.addStretch(1)

        # Copyright notice
        copyright_label = QLabel("© 2024 Ibnulsahgianto. All rights reserved.", self)
        layout.addWidget(copyright_label)

        self.central_widget.setLayout(layout)

        self.logo_path = None

        self.create_menu()

    def create_menu(self):
        menubar = self.menuBar()

        # File menu
        file_menu = menubar.addMenu('File')

        save_action = QAction('Save QR Code', self)
        save_action.triggered.connect(self.save_qr_code)
        file_menu.addAction(save_action)

        exit_action = QAction('Exit', self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # Help menu
        help_menu = menubar.addMenu('Help')

        about_action = QAction('About', self)
        about_action.triggered.connect(self.show_about_dialog)
        help_menu.addAction(about_action)

    def load_logo(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.ExistingFile)
        file_dialog.setNameFilter("Images (*.png *.jpg *.jpeg *.gif)")
        if file_dialog.exec_():
            file_paths = file_dialog.selectedFiles()
            if file_paths:
                self.logo_path = file_paths[0]

    def generate_qr_code(self):
        link = self.link_input.text()

        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=1,
        )
        qr.add_data(link)
        qr.make(fit=True)
        qr_image = qr.make_image(fill_color="black", back_color="white")

        if self.logo_path:
            logo = Image.open(self.logo_path)

            # Calculate the size for the logo
            logo_size = min(qr_image.size[0], qr_image.size[1]) // 6
            logo = logo.resize((logo_size, logo_size), Image.LANCZOS)  # Use LANCZOS for higher quality

            # Create a new image with RGBA mode to support transparency
            result_image = Image.new("RGBA", qr_image.size, (255, 255, 255, 0))

            # Calculate the position to paste the logo in the center
            x = (qr_image.size[0] - logo.size[0]) // 2
            y = (qr_image.size[1] - logo.size[1]) // 2

            # Paste the logo onto the result image with transparency
            result_image.paste(logo, (x, y), logo)

            # Composite the result image onto the QR code image
            qr_image = Image.alpha_composite(qr_image.convert("RGBA"), result_image)

        qr_image.save("qrcode.png")

        pixmap = QPixmap("qrcode.png")
        self.qr_image_label.setPixmap(pixmap.scaledToWidth(600))
        self.qr_image_label.setAlignment(Qt.AlignCenter)

    def save_qr_code(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Save QR Code", "", "PNG (*.png)")
        if file_path:
            pixmap = self.qr_image_label.pixmap()
            pixmap.save(file_path, "PNG")

    def show_about_dialog(self):
        QMessageBox.about(self, "About", "QR Code Generator v1.0\n\nCreated by Ibnulsahgianto\n contact me on insta: @sahgianto or more aboout me on https://sahgianto.com ")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QRCodeGenerator()
    window.show()
    sys.exit(app.exec_())
