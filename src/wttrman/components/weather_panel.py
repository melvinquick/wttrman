from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget, QSizePolicy


class WeatherPanel(QWidget):
    """Displays the weather report or an error message."""

    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.output = QLabel(
            "Press Get Weather to fetch the forecast.",
            objectName="weatherOutput",
            alignment=Qt.AlignmentFlag.AlignCenter,
            wordWrap=True,
        )

        self.output.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )
        self.output.setProperty("kind", "info")

        layout.addWidget(self.output)

    def set_text(self, text):
        self.output.setText(
            f"<div align='center' style='white-space: pre-wrap;'>{text}</div>"
        )
        self._set_kind("info")

    def set_html(self, html):
        self.output.setText(html)
        self._set_kind("info")

    def set_error(self, text):
        self.output.setText(
            f"<div align='center' style='color: #F85149;'>⚠ {text}</div>"
        )
        self._set_kind("danger")

    def _set_kind(self, kind):
        if self.output.property("kind") != kind:
            self.output.setProperty("kind", kind)
            self.output.style().unpolish(self.output)
            self.output.style().polish(self.output)
            self.output.update()
