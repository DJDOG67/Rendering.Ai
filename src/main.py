import sys
from pathlib import Path
from PyQt5 import QtWidgets, QtGui, QtCore

from presets import load_presets, save_presets, Preset
from project import Project
from cleanup import cleanup_image


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Rendering.Ai Prototype")
        self.resize(800, 600)

        self.image_label = QtWidgets.QLabel("Load a sketch to begin")
        self.image_label.setAlignment(QtCore.Qt.AlignCenter)
        self.setCentralWidget(self.image_label)

        self._create_menu()
        self.presets = load_presets()
        self.current_project: Project | None = None

    def _create_menu(self):
        menubar = self.menuBar()
        file_menu = menubar.addMenu("File")
        open_action = file_menu.addAction("Open Sketch")
        open_action.triggered.connect(self.open_sketch)
        save_action = file_menu.addAction("Save Project")
        save_action.triggered.connect(self.save_project)
        file_menu.addSeparator()
        exit_action = file_menu.addAction("Exit")
        exit_action.triggered.connect(self.close)

    def open_sketch(self):
        path, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, "Open Sketch", filter="Images (*.png *.jpg *.jpeg)")
        if not path:
            return
        cleaned = cleanup_image(path)
        pix = QtGui.QPixmap(cleaned)
        self.image_label.setPixmap(
            pix.scaled(self.image_label.size(), QtCore.Qt.KeepAspectRatio))
        self.current_project = Project(sketch_path=path)

    def save_project(self):
        if not self.current_project:
            QtWidgets.QMessageBox.information(self, "Info", "No project to save")
            return
        path, _ = QtWidgets.QFileDialog.getSaveFileName(
            self, "Save Project", filter="Sketch Render Project (*.srproj)")
        if not path:
            return
        if not path.endswith('.srproj'):
            path += '.srproj'
        self.current_project.save(Path(path))
        QtWidgets.QMessageBox.information(self, "Saved", f"Project saved to {path}")


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
