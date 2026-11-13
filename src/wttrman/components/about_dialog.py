from importlib.metadata import metadata, version
from urllib.request import urlopen

from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (
    QDialog,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
)


class AboutDialog(QDialog):
    def __init__(self, theme_manager, current_theme, parent=None):
        super().__init__(parent)
        self.setWindowTitle("About Wttrman")
        self.setObjectName("MainWindow")
        self.setWindowFlags(Qt.WindowType.Dialog | Qt.WindowType.WindowCloseButtonHint)
        self.setFixedWidth(400)

        # Apply the app's current theme to this dialog
        self.setStyleSheet(theme_manager._render(current_theme))

        # Fetch the accent color for the links
        theme_color = theme_manager.themes[current_theme].get("accent-color", "#58a6ff")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 32, 32, 32)
        layout.setSpacing(16)
        layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        # Logo
        logo_url = (
            "https://raw.githubusercontent.com/melvinquick/wttrman/main/"
            "src/wttrman/resources/images/wttrman-256.png"
        )
        logo_label = QLabel()
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        try:
            data = urlopen(logo_url).read()
            pixmap = QPixmap()
            pixmap.loadFromData(data)
            logo_label.setPixmap(
                pixmap.scaled(
                    128,
                    128,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation,
                )
            )
        except Exception:
            logo_label.setText("🌤")
            logo_label.setObjectName("DialogTitle")
        layout.addWidget(logo_label)

        # App Name
        title = QLabel("Wttrman")
        title.setObjectName("DialogTitle")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        # Version and License
        try:
            app_version = version("wttrman")
            app_license = metadata("wttrman").get("License-Expression", "MIT")
        except Exception:
            app_version = "Unknown"
            app_license = "MIT"

        version_label = QLabel(f"Version {app_version}")
        version_label.setObjectName("MutedLabel")
        version_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(version_label)

        author_label = QLabel("Created by Melvin Quick")
        author_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(author_label)

        license_label = QLabel(f"Licensed under {app_license}")
        license_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(license_label)

        # Links (Qt's HTML parser chokes on multiple inline styles, so we keep it simple)
        links_html = (
            f'<a href="https://github.com/melvinquick/wttrman" style="color: {theme_color};">GitHub Repository</a> | '
            f'<a href="https://github.com/melvinquick/wttrman/blob/main/CHANGELOG" style="color: {theme_color};">Changelog</a>'
        )
        links_label = QLabel(links_html)
        links_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        links_label.setOpenExternalLinks(True)
        links_label.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextBrowserInteraction
        )
        layout.addWidget(links_label)

        layout.addSpacing(16)

        # Close Button
        btn_layout = QHBoxLayout()
        btn_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        close_btn = QPushButton("Close")
        close_btn.setObjectName("PrimaryButton")
        close_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        close_btn.setFixedWidth(100)
        close_btn.clicked.connect(self.accept)
        btn_layout.addWidget(close_btn)

        layout.addLayout(btn_layout)
