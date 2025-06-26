from PyQt5 import QtWidgets
import sys

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Rendering.Ai")
        self.resize(800, 600)
        self.setup_ui()

    def setup_ui(self):
        central = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout()

        self.upload_btn = QtWidgets.QPushButton("Upload Sketch")
        self.clean_btn = QtWidgets.QPushButton("Clean Up")
        self.render_btn = QtWidgets.QPushButton("Render")
        layout.addWidget(self.upload_btn)
        layout.addWidget(self.clean_btn)
        layout.addWidget(self.render_btn)

        central.setLayout(layout)
        self.setCentralWidget(central)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
