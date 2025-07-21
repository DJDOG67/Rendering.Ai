from __future__ import annotations

import sys
from pathlib import Path

from PyQt5 import QtWidgets, QtGui, QtCore

from backend import renderer
from app import project

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Rendering.Ai")
        self.resize(900, 700)

        self.sketch_path: Path | None = None
        self.depth_path: Path | None = None
        self.render_path: Path | None = None

        self.setup_ui()

    def setup_ui(self):
        tabs = QtWidgets.QTabWidget()
        tabs.addTab(self._build_sketch_tab(), "Sketch")
        tabs.addTab(self._build_depth_tab(), "Depth")
        tabs.addTab(self._build_render_tab(), "Render")
        self.setCentralWidget(tabs)

        file_menu = self.menuBar().addMenu("File")
        save_act = file_menu.addAction("Save Project")
        load_act = file_menu.addAction("Load Project")
        save_act.triggered.connect(self.save_project)
        load_act.triggered.connect(self.load_project)

    # --- Tab builders -------------------------------------------------

    def _build_sketch_tab(self) -> QtWidgets.QWidget:
        widget = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(widget)

        self.sketch_view = QtWidgets.QLabel(alignment=QtCore.Qt.AlignCenter)
        self.upload_btn = QtWidgets.QPushButton("Upload Sketch")
        self.clean_btn = QtWidgets.QPushButton("Clean Up")
        layout.addWidget(self.sketch_view, 1)
        layout.addWidget(self.upload_btn)
        layout.addWidget(self.clean_btn)

        self.upload_btn.clicked.connect(self.select_sketch)
        self.clean_btn.clicked.connect(self.clean_sketch)

        return widget

    def _build_depth_tab(self) -> QtWidgets.QWidget:
        widget = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(widget)

        self.depth_view = QtWidgets.QLabel(alignment=QtCore.Qt.AlignCenter)
        self.depth_btn = QtWidgets.QPushButton("Estimate Depth")
        layout.addWidget(self.depth_view, 1)
        layout.addWidget(self.depth_btn)

        self.depth_btn.clicked.connect(self.estimate_depth)
        return widget

    def _build_render_tab(self) -> QtWidgets.QWidget:
        widget = QtWidgets.QWidget()
        form = QtWidgets.QFormLayout(widget)
        self.lighting_edit = QtWidgets.QLineEdit()
        form.addRow("Lighting:", self.lighting_edit)
        self.render_btn = QtWidgets.QPushButton("Render")
        form.addRow(self.render_btn)
        self.render_view = QtWidgets.QLabel(alignment=QtCore.Qt.AlignCenter)
        form.addRow(self.render_view)
        self.render_btn.clicked.connect(self.render_image)
        return widget

    # --- Slots --------------------------------------------------------

    def select_sketch(self) -> None:
        path, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Select sketch")
        if not path:
            return
        self.sketch_path = Path(path)
        pixmap = QtGui.QPixmap(str(self.sketch_path))
        self.sketch_view.setPixmap(pixmap.scaled(400, 400, QtCore.Qt.KeepAspectRatio))

    def clean_sketch(self) -> None:
        if not self.sketch_path:
            return
        self.sketch_path = renderer.clean_up(self.sketch_path)
        pixmap = QtGui.QPixmap(str(self.sketch_path))
        self.sketch_view.setPixmap(pixmap.scaled(400, 400, QtCore.Qt.KeepAspectRatio))

    def estimate_depth(self) -> None:
        if not self.sketch_path:
            return
        self.depth_path = renderer.detect_depth(self.sketch_path)
        pixmap = QtGui.QPixmap(str(self.depth_path))
        self.depth_view.setPixmap(pixmap.scaled(400, 400, QtCore.Qt.KeepAspectRatio))

    def render_image(self) -> None:
        if not self.sketch_path:
            return
        self.render_path = renderer.render_image(self.sketch_path, self.depth_path, {"lighting": self.lighting_edit.text()})
        pixmap = QtGui.QPixmap(str(self.render_path))
        self.render_view.setPixmap(pixmap.scaled(400, 400, QtCore.Qt.KeepAspectRatio))

    def save_project(self) -> None:
        if not self.sketch_path:
            return
        path, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Save project", filter="*.srproj")
        if not path:
            return
        project.save_project(Path(path), self.sketch_path, self.depth_path, {"lighting": self.lighting_edit.text()})

    def load_project(self) -> None:
        path, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Open project", filter="*.srproj")
        if not path:
            return
        data = project.load_project(Path(path))
        self.sketch_path = data.get("sketch")
        self.depth_path = data.get("depth")
        settings = data.get("settings", {})
        self.lighting_edit.setText(settings.get("lighting", ""))
        if self.sketch_path:
            pixmap = QtGui.QPixmap(str(self.sketch_path))
            self.sketch_view.setPixmap(pixmap.scaled(400, 400, QtCore.Qt.KeepAspectRatio))
        if self.depth_path:
            pixmap = QtGui.QPixmap(str(self.depth_path))
            self.depth_view.setPixmap(pixmap.scaled(400, 400, QtCore.Qt.KeepAspectRatio))

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
