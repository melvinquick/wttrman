import os
import sys

import requests
from PySide6.QtCore import QSettings, Qt, QTimer
from PySide6.QtGui import QAction
from PySide6.QtWidgets import (
    QApplication,
    QFrame,
    QHBoxLayout,
    QMainWindow,
    QMenuBar,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from .components.about_dialog import AboutDialog
from .components.location_panel import LocationPanel
from .components.location_repository import LocationRepository
from .components.preferences_dialog import PreferencesDialog
from .components.qss_file_handler import QssFileHandler
from .components.theme_manager import ThemeManager
from .components.weather_panel import WeatherPanel
from .components.weather_service import WeatherService
from .components.yaml_file_handler import YamlFileHandler


class Wttrman(QMainWindow):
    def __init__(self):
        super().__init__()
        self.service = WeatherService()
        self.repo = LocationRepository()

        self.themes = YamlFileHandler(
            "../resources/styles/themes.yaml"
        ).load_yaml_file()
        qss = QssFileHandler("../resources/styles/styles.qss").load_qss_file()
        self.theme_manager = ThemeManager(self.themes, qss)

        config_dir = os.path.expanduser("~/.config/wttrman")
        os.makedirs(config_dir, exist_ok=True)
        settings_path = os.path.join(config_dir, "settings.conf")
        self.settings = QSettings(settings_path, QSettings.Format.IniFormat)

        self.theme_name = self.settings.value("theme", ThemeManager.DEFAULT_THEME)

        self._status_timer = QTimer(self)
        self._status_timer.setSingleShot(True)
        self._status_timer.timeout.connect(self.clear_status)

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Wttrman")
        self.setObjectName("MainWindow")

        # --- CUSTOM MENU BAR ---
        top_bar_container = QWidget()
        top_bar_container.setObjectName("TopBarContainer")
        top_bar_layout = QHBoxLayout(top_bar_container)
        top_bar_layout.setContentsMargins(12, 4, 12, 4)
        top_bar_layout.setSpacing(8)

        self.menu_bar = QMenuBar()
        self.menu_bar.setObjectName("MenuBar")
        self.menu_bar.setSizePolicy(
            QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Preferred
        )

        file_menu = self.menu_bar.addMenu("File")
        file_menu.addAction("Exit", self.close)

        edit_menu = self.menu_bar.addMenu("Edit")
        edit_menu.addAction("Copy Weather", self.copy_weather)

        help_menu = self.menu_bar.addMenu("Help")
        help_menu.addAction("About", self.open_about)

        prefs_action = QAction("Preferences", self)
        prefs_action.triggered.connect(self.open_preferences)
        self.menu_bar.addAction(prefs_action)

        top_bar_layout.addWidget(self.menu_bar)
        top_bar_layout.addStretch()

        # --- MAIN LAYOUT ---
        central = QWidget()
        central.setObjectName("CentralWidget")
        self.setCentralWidget(central)

        root_layout = QVBoxLayout(central)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)
        root_layout.addWidget(top_bar_container)

        content_widget = QWidget()
        content_widget.setObjectName("CentralWidget")
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(24, 24, 24, 24)
        content_layout.setSpacing(16)

        body = QHBoxLayout()
        body.setSpacing(16)

        left_card = QFrame()
        left_card.setObjectName("Card")
        left_layout = QVBoxLayout(left_card)
        left_layout.setContentsMargins(24, 24, 24, 24)
        left_layout.setSpacing(12)

        self.location_panel = LocationPanel(self.repo)
        left_layout.addWidget(self.location_panel)
        left_layout.addStretch()

        right_card = QFrame()
        right_card.setObjectName("Card")
        right_layout = QVBoxLayout(right_card)
        right_layout.setContentsMargins(24, 24, 24, 24)

        self.weather_panel = WeatherPanel()
        right_layout.addWidget(self.weather_panel)

        body.addWidget(left_card, 1)
        body.addWidget(right_card, 2)
        content_layout.addLayout(body, 1)

        controls_layout = QVBoxLayout()
        controls_layout.setSpacing(8)

        self.get_weather = QPushButton("Get Weather")
        self.get_weather.setObjectName("PrimaryButton")
        self.get_weather.setCursor(Qt.CursorShape.PointingHandCursor)
        self.get_weather.setMinimumHeight(46)

        self.status_label = QPushButton("")
        self.status_label.setObjectName("StatusLabel")
        self.status_label.setEnabled(False)
        self.status_label.setFlat(True)

        controls_layout.addWidget(self.get_weather)
        controls_layout.addWidget(self.status_label)
        content_layout.addLayout(controls_layout)

        root_layout.addWidget(content_widget)

        # --- SIGNALS ---
        self.get_weather.clicked.connect(self.fetch_weather)
        self.location_panel.selection_changed.connect(self._on_location_changed)

        self.apply_theme(self.theme_name)

        self.setMinimumWidth(720)
        self.setMinimumHeight(460)
        self.resize(800, 500)

        # Load startup location
        self._load_startup_location()

    def _get_weather_emoji(self, condition_code):
        code = str(condition_code)
        if code in ["113"]:
            return "☀️"
        elif code in ["116"]:
            return "⛅"
        elif code in ["119", "122"]:
            return "☁️"
        elif code in ["143", "248", "260"]:
            return "🌫️"
        elif code in [
            "176",
            "263",
            "266",
            "293",
            "296",
            "299",
            "302",
            "305",
            "308",
            "353",
            "356",
            "359",
        ]:
            return "🌧️"
        elif code in [
            "179",
            "182",
            "185",
            "227",
            "230",
            "281",
            "284",
            "311",
            "314",
            "317",
            "320",
            "323",
            "326",
            "329",
            "332",
            "335",
            "338",
            "350",
            "362",
            "365",
            "368",
            "371",
            "374",
            "377",
        ]:
            return "❄️"
        elif code in ["200", "386", "389", "392", "395"]:
            return "⛈️"
        return "🌡️"

    def _load_startup_location(self):
        d_country = self.settings.value("defaults/country", "")
        if d_country:
            d_region = self.settings.value("defaults/region", "")
            d_city = self.settings.value("defaults/city", "")
            self.location_panel.set_location(d_country, d_region, d_city)
            return

        l_country = self.settings.value("location/country", "")
        l_region = self.settings.value("location/region", "")
        l_city = self.settings.value("location/city", "")

        if l_country:
            self.location_panel.set_location(l_country, l_region, l_city)
        else:
            self.location_panel.set_location()

    def closeEvent(self, event):
        country, region, city = self.location_panel.selection()
        if country:
            self.settings.setValue("location/country", country)
            self.settings.setValue("location/region", region)
            self.settings.setValue("location/city", city)
        super().closeEvent(event)

    # --- ACTIONS ---
    def open_preferences(self):
        dialog = PreferencesDialog(self.settings, self.theme_manager, self.repo, self)
        dialog.theme_changed.connect(self.apply_theme)
        dialog.exec()

    def open_about(self):
        dialog = AboutDialog(self.theme_manager, self.theme_name, self)
        dialog.exec()

    def apply_theme(self, theme_name):
        self.theme_name = self.theme_manager.resolve(theme_name)
        self.settings.setValue("theme", self.theme_name)
        qss = self.theme_manager.render(self.theme_name)
        QApplication.instance().setStyleSheet(qss)

    def _on_location_changed(self, *_):
        self.weather_panel.set_text("Press Get Weather to fetch the forecast.")
        self.clear_status()

    def fetch_weather(self):
        country, region, city = self.location_panel.selection()
        if not city:
            self.set_status("Select a country, region, and city.", "warning")
            return

        self.get_weather.setEnabled(False)
        self.weather_panel.set_text("Fetching…")
        QApplication.processEvents()

        units = self.settings.value("weather/units", "m")
        use_icons = bool(self.settings.value("weather/icons", ""))

        url = f"https://wttr.in/{city},{region},{country}?format=j1&{units}"

        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            data = response.json()

            current = data["current_condition"][0]
            code = current["weatherCode"]
            condition_text = current["weatherDesc"][0]["value"]

            span_start = "<span style='font-size: 16pt;'>"
            span_end = "</span>"
            nbsp = "&nbsp;"

            emoji = (
                f"{span_start}{self._get_weather_emoji(code)}{span_end}"
                if use_icons
                else ""
            )

            html = "<div align='center'>"

            # Header
            if self.settings.value("weather/cb_condition", True, type=bool):
                html += f"<div style='margin-bottom: 8px;'>{emoji}{nbsp}{condition_text}</div>"
                html += "<div style='color: #8B949E; margin-bottom: 16px;'>─────────────────────────</div>"

            # Collect stats into a list of (icon, text) tuples
            stats = []

            if self.settings.value("weather/cb_temp", True, type=bool):
                if units == "m":
                    temp_text = f"{current['temp_C']}°C"
                    feels_text = f"({current['FeelsLikeC']}°C)"
                else:
                    temp_text = f"{current['temp_F']}°F"
                    feels_text = f"({current['FeelsLikeF']}°F)"

                if self.settings.value("weather/cb_feels_like", False, type=bool):
                    temp_text += f" {feels_text}"
                stats.append(("🌡️", temp_text))

            if self.settings.value("weather/cb_wind", True, type=bool):
                speed = (
                    current["windspeedKmph"]
                    if units == "m"
                    else current["windspeedMiles"]
                )
                unit = "km/h" if units == "m" else "mph"
                # Use &nbsp; inside the text string to prevent Qt from breaking "km/h" into "km/" and "h"
                stats.append(
                    ("💨", f"{current['winddir16Point']}{nbsp}{speed}{nbsp}{unit}")
                )

            if self.settings.value("weather/cb_humidity", False, type=bool):
                stats.append(("💧", f"{current['humidity']}%"))

            if self.settings.value("weather/cb_precip", True, type=bool):
                precip = (
                    current["precipMM"] if units == "m" else current["precipInches"]
                )
                unit = "mm" if units == "m" else "in"
                stats.append(("🌧️", f"{precip}{nbsp}{unit}"))

            if self.settings.value("weather/cb_pressure", False, type=bool):
                stats.append(("🧭", f"{current['pressure']}{nbsp}hPa"))

            if self.settings.value("weather/cb_uv", False, type=bool):
                stats.append(("🕶️", f"UV:{nbsp}{current['uvIndex']}"))

            # Build the 3-column HTML table (Left Item | Spacer | Right Item)
            if stats:
                html += "<table align='center' width='100%' cellspacing='0' cellpadding='4' style='margin-top: 10px;'>"
                for i in range(0, len(stats), 2):
                    html += "<tr>"

                    # Left Item
                    icon, text = stats[i]
                    html += (
                        "<td align='right' width='45%'>"
                        f"{span_start}{icon}{span_end}{nbsp}{text}"
                        "</td>"
                    )

                    # Middle Spacer
                    html += "<td width='10%'></td>"

                    # Right Item
                    if i + 1 < len(stats):
                        icon2, text2 = stats[i + 1]
                        html += (
                            "<td align='left' width='45%'>"
                            f"{span_start}{icon2}{span_end}{nbsp}{text2}"
                            "</td>"
                        )
                    else:
                        # Empty cell to maintain the grid
                        html += "<td width='45%'></td>"
                    html += "</tr>"
                html += "</table>"

            html += "</div>"

            if not stats and not self.settings.value(
                "weather/cb_condition", True, type=bool
            ):
                self.weather_panel.set_text("No data selected.")
            else:
                self.weather_panel.set_html(html)

            self.set_status(f"Forecast updated for {city}.", "success")

        except Exception as exc:
            self.weather_panel.set_error(f"Could not fetch weather: {exc}")
            self.set_status("Could not fetch weather.", "danger")
        finally:
            self.get_weather.setEnabled(True)

    def copy_weather(self):
        # Extract raw text from the HTML table
        text = self.weather_panel.output.text()
        import re

        # Strip tags and fix HTML entities
        clean_text = re.sub("<[^<]+?>", "", text)
        clean_text = clean_text.replace("&nbsp;", " ")

        if not clean_text.strip():
            self.set_status("Nothing to copy yet.", "warning")
            return
        QApplication.clipboard().setText(clean_text)
        self.set_status("Copied to clipboard.", "success")

    def set_status(self, message, kind="info"):
        self.status_label.setText(message)
        if self.status_label.property("kind") != kind:
            self.status_label.setProperty("kind", kind)
        self._status_timer.start(2500)

    def clear_status(self):
        self.status_label.setText("")
        self.status_label.setProperty("kind", "info")


def main():
    app = QApplication(sys.argv)
    app.setOrganizationName("wttrman")
    app.setApplicationName("wttrman")
    window = Wttrman()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
