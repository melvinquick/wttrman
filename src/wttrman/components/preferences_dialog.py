from PySide6.QtCore import QSettings, Qt, Signal
from PySide6.QtWidgets import (
    QApplication,
    QCheckBox,
    QComboBox,
    QDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QGridLayout,
)

from .theme_manager import ThemeManager
from .location_repository import LocationRepository


class PreferencesDialog(QDialog):
    theme_changed = Signal(str)

    def __init__(
        self,
        settings: QSettings,
        theme_manager: ThemeManager,
        repo: LocationRepository,
        parent=None,
    ):
        super().__init__(parent)
        self.settings = settings
        self.theme_manager = theme_manager
        self.repo = repo

        self.current_theme = self.settings.value("theme", ThemeManager.DEFAULT_THEME)

        self.setWindowTitle("Preferences")
        self.setFixedWidth(450)

        self.setStyleSheet(self.theme_manager._render(self.current_theme))

        self._build_ui()
        self._load_settings()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(16)

        # --- Appearance Card ---
        appearance_card = QFrame()
        appearance_card.setObjectName("Card")
        card_layout = QVBoxLayout(appearance_card)
        card_layout.setContentsMargins(16, 16, 16, 16)
        card_layout.setSpacing(12)

        title = QLabel("Appearance")
        title.setObjectName("DialogTitle")
        title.setStyleSheet("font-size: 10pt; font-weight: 600;")
        card_layout.addWidget(title)

        theme_row = QHBoxLayout()
        theme_label = QLabel("Theme:")
        theme_label.setFixedWidth(60)

        self.theme_combo = QComboBox()
        for name in sorted(self.theme_manager.themes.keys()):
            label = name.replace("_", " ").title()
            self.theme_combo.addItem(label, userData=name)

        idx = self.theme_combo.findData(self.current_theme)
        if idx >= 0:
            self.theme_combo.setCurrentIndex(idx)

        self.theme_combo.currentIndexChanged.connect(self._on_theme_selected)

        theme_row.addWidget(theme_label)
        theme_row.addWidget(self.theme_combo, 1)
        card_layout.addLayout(theme_row)
        layout.addWidget(appearance_card)

        # --- Weather Output Card ---
        weather_card = QFrame()
        weather_card.setObjectName("Card")
        weather_layout = QVBoxLayout(weather_card)
        weather_layout.setContentsMargins(16, 16, 16, 16)
        weather_layout.setSpacing(12)

        title2 = QLabel("Weather Output")
        title2.setObjectName("DialogTitle")
        title2.setStyleSheet("font-size: 10pt; font-weight: 600;")
        weather_layout.addWidget(title2)

        # Units
        units_row = QHBoxLayout()
        units_label = QLabel("Units:")
        units_label.setFixedWidth(60)
        self.units_combo = QComboBox()
        self.units_combo.addItem("Metric (°C, km/h)", userData="m")
        self.units_combo.addItem("USCS (°F, mph)", userData="u")
        units_row.addWidget(units_label)
        units_row.addWidget(self.units_combo, 1)
        weather_layout.addLayout(units_row)

        # Icons
        icons_row = QHBoxLayout()
        icons_label = QLabel("Icons:")
        icons_label.setFixedWidth(60)
        self.icons_combo = QComboBox()
        self.icons_combo.addItem("Enabled", userData="1")
        self.icons_combo.addItem("Disabled", userData="")
        icons_row.addWidget(icons_label)
        icons_row.addWidget(self.icons_combo, 1)
        weather_layout.addLayout(icons_row)

        # Metrics Grid
        grid = QGridLayout()
        grid.setSpacing(8)

        self.cb_condition = QCheckBox("Condition")
        self.cb_temp = QCheckBox("Temperature")
        self.cb_feels_like = QCheckBox("Feels Like")
        self.cb_wind = QCheckBox("Wind")
        self.cb_humidity = QCheckBox("Humidity")
        self.cb_precip = QCheckBox("Precipitation")
        self.cb_pressure = QCheckBox("Pressure")
        self.cb_uv = QCheckBox("UV Index")

        grid.addWidget(self.cb_condition, 0, 0)
        grid.addWidget(self.cb_temp, 0, 1)
        grid.addWidget(self.cb_feels_like, 1, 0)
        grid.addWidget(self.cb_wind, 1, 1)
        grid.addWidget(self.cb_humidity, 2, 0)
        grid.addWidget(self.cb_precip, 2, 1)
        grid.addWidget(self.cb_pressure, 3, 0)
        grid.addWidget(self.cb_uv, 3, 1)

        weather_layout.addLayout(grid)
        layout.addWidget(weather_card)

        # --- Startup Defaults Card ---
        defaults_card = QFrame()
        defaults_card.setObjectName("Card")
        defaults_layout = QVBoxLayout(defaults_card)
        defaults_layout.setContentsMargins(16, 16, 16, 16)
        defaults_layout.setSpacing(12)

        title3 = QLabel("Startup Defaults")
        title3.setObjectName("DialogTitle")
        title3.setStyleSheet("font-size: 10pt; font-weight: 600;")
        defaults_layout.addWidget(title3)

        self.def_country = QComboBox()
        self.def_country.addItem("None (Last Used)")
        self.def_country.addItems(self.repo.countries())

        self.def_region = QComboBox()
        self.def_city = QComboBox()

        self.def_country.currentTextChanged.connect(self._on_def_country_changed)
        self.def_region.currentTextChanged.connect(self._on_def_region_changed)

        defaults_layout.addWidget(QLabel("Country"))
        defaults_layout.addWidget(self.def_country)
        defaults_layout.addWidget(QLabel("State / Province"))
        defaults_layout.addWidget(self.def_region)
        defaults_layout.addWidget(QLabel("City"))
        defaults_layout.addWidget(self.def_city)

        layout.addWidget(defaults_card)
        layout.addStretch()

        # --- Footer Buttons ---
        btn_layout = QHBoxLayout()
        btn_layout.setAlignment(Qt.AlignmentFlag.AlignRight)

        save_btn = QPushButton("Save")
        save_btn.setObjectName("PrimaryButton")
        save_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        save_btn.clicked.connect(self.accept)

        btn_layout.addWidget(save_btn)
        layout.addLayout(btn_layout)

    def _load_settings(self):
        # Load Units
        saved_units = self.settings.value("weather/units", "m")
        idx = self.units_combo.findData(saved_units)
        if idx >= 0:
            self.units_combo.setCurrentIndex(idx)

        # Load Icons
        saved_icons = self.settings.value("weather/icons", "1")
        idx = self.icons_combo.findData(saved_icons)
        if idx >= 0:
            self.icons_combo.setCurrentIndex(idx)

        # Load Metrics
        self.cb_condition.setChecked(
            self.settings.value("weather/cb_condition", True, type=bool)
        )
        self.cb_temp.setChecked(self.settings.value("weather/cb_temp", True, type=bool))

        # Load the last known state of Feels Like
        last_state = self.settings.value(
            "weather/last_feels_like_state",
            self.settings.value("weather/cb_feels_like", False, type=bool),
            type=bool,
        )
        self.cb_feels_like.setChecked(last_state)

        self.cb_wind.setChecked(self.settings.value("weather/cb_wind", True, type=bool))
        self.cb_humidity.setChecked(
            self.settings.value("weather/cb_humidity", False, type=bool)
        )
        self.cb_precip.setChecked(
            self.settings.value("weather/cb_precip", True, type=bool)
        )
        self.cb_pressure.setChecked(
            self.settings.value("weather/cb_pressure", False, type=bool)
        )
        self.cb_uv.setChecked(self.settings.value("weather/cb_uv", False, type=bool))

        # Wire up the dynamic enabling of "Feels Like"
        self.cb_temp.toggled.connect(self._on_temp_toggled)

        # Track manual changes so we remember them
        self.cb_feels_like.toggled.connect(self._on_feels_like_toggled)

        # Force initial state
        self._on_temp_toggled(self.cb_temp.isChecked())
        self.cb_feels_like.setToolTip("Requires Temperature to be enabled.")

        # Load Defaults
        d_country = self.settings.value("defaults/country", "")
        if d_country:
            idx = self.def_country.findText(d_country)
            if idx >= 0:
                self.def_country.setCurrentIndex(idx)
                self._on_def_country_changed(d_country)

                d_region = self.settings.value("defaults/region", "")
                if d_region:
                    self.def_region.setCurrentText(d_region)
                    self._on_def_region_changed(d_region)

                    d_city = self.settings.value("defaults/city", "")
                    if d_city:
                        self.def_city.setCurrentText(d_city)

    def _on_temp_toggled(self, checked):
        self.cb_feels_like.setEnabled(checked)

        if checked:
            # Restore the last state from QSettings
            last_state = self.settings.value(
                "weather/last_feels_like_state", False, type=bool
            )
            self.cb_feels_like.setChecked(last_state)
        else:
            # Save the current state to QSettings before forcing it off
            current_state = self.cb_feels_like.isChecked()
            self.settings.setValue("weather/last_feels_like_state", current_state)
            self.cb_feels_like.setChecked(False)

    def _on_feels_like_toggled(self, checked):
        # Only update the QSettings memory if the checkbox is actually enabled
        if self.cb_feels_like.isEnabled():
            self.settings.setValue("weather/last_feels_like_state", checked)

    def _on_def_country_changed(self, country):
        self.def_region.clear()
        if country == "None (Last Used)":
            self.def_region.setEnabled(False)
            self.def_city.setEnabled(False)
        else:
            self.def_region.setEnabled(True)
            self.def_region.addItems(self.repo.regions(country))
            if self.def_region.count() > 0:
                self.def_region.setCurrentIndex(0)

    def _on_def_region_changed(self, region):
        country = self.def_country.currentText()
        self.def_city.clear()
        if country == "None (Last Used)" or not region:
            self.def_city.setEnabled(False)
        else:
            self.def_city.setEnabled(True)
            self.def_city.addItems(self.repo.cities(country, region))

    def _on_theme_selected(self, index):
        new_theme = self.theme_combo.itemData(index)
        if new_theme and new_theme != self.current_theme:
            self.current_theme = new_theme
            self.settings.setValue("theme", new_theme)

            qss = self.theme_manager._render(self.current_theme)
            QApplication.instance().setStyleSheet(qss)

            self.theme_changed.emit(new_theme)

    def accept(self):
        # Save Units
        self.settings.setValue("weather/units", self.units_combo.currentData())
        # Save Icons
        self.settings.setValue("weather/icons", self.icons_combo.currentData())

        # Save Metrics
        self.settings.setValue("weather/cb_condition", self.cb_condition.isChecked())
        self.settings.setValue("weather/cb_temp", self.cb_temp.isChecked())
        self.settings.setValue("weather/cb_feels_like", self.cb_feels_like.isChecked())
        self.settings.setValue("weather/cb_wind", self.cb_wind.isChecked())
        self.settings.setValue("weather/cb_humidity", self.cb_humidity.isChecked())
        self.settings.setValue("weather/cb_precip", self.cb_precip.isChecked())
        self.settings.setValue("weather/cb_pressure", self.cb_pressure.isChecked())
        self.settings.setValue("weather/cb_uv", self.cb_uv.isChecked())

        # Save Defaults
        country = self.def_country.currentText()
        if country == "None (Last Used)":
            self.settings.remove("defaults/country")
            self.settings.remove("defaults/region")
            self.settings.remove("defaults/city")
        else:
            self.settings.setValue("defaults/country", country)
            self.settings.setValue("defaults/region", self.def_region.currentText())
            self.settings.setValue("defaults/city", self.def_city.currentText())

        super().accept()
