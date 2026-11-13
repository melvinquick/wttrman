from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QComboBox,
    QLabel,
    QVBoxLayout,
    QWidget,
)


class LocationPanel(QWidget):
    """Country / region / city selectors."""

    selection_changed = Signal(str, str, str)

    def __init__(self, repo, parent=None):
        super().__init__(parent)
        self.repo = repo
        self._build_ui()
        self._wire()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)

        layout.addWidget(QLabel("Country", objectName="sectionLabel"))
        self.country = QComboBox()
        self.country.setMaxVisibleItems(10)
        layout.addWidget(self.country)

        layout.addSpacing(8)
        layout.addWidget(QLabel("State / Province", objectName="sectionLabel"))
        self.region = QComboBox()
        self.region.setMaxVisibleItems(10)
        layout.addWidget(self.region)

        layout.addSpacing(8)
        layout.addWidget(QLabel("City", objectName="sectionLabel"))
        self.city = QComboBox()
        self.city.setMaxVisibleItems(10)
        layout.addWidget(self.city)

        layout.addStretch()

        self.region.setEnabled(False)
        self.city.setEnabled(False)

    def _wire(self):
        self.country.currentTextChanged.connect(self._on_country_changed)
        self.region.currentTextChanged.connect(self._on_region_changed)
        self.country.currentTextChanged.connect(self._emit_selection)
        self.region.currentTextChanged.connect(self._emit_selection)
        self.city.currentTextChanged.connect(self._emit_selection)

    def set_location(self, country=None, region=None, city=None):
        """Sets the initial location. If None, picks the first available."""
        self.country.blockSignals(True)
        self.country.clear()
        self.country.addItems(self.repo.countries())

        if country and self.country.findText(country) >= 0:
            self.country.setCurrentText(country)
        elif self.country.count() > 0:
            self.country.setCurrentIndex(0)

        self.country.blockSignals(False)

        # Manually trigger population since we blocked signals
        self._on_country_changed(self.country.currentText())

        if region and self.region.findText(region) >= 0:
            self.region.setCurrentText(region)
            # Manually trigger cities
            self._on_region_changed(region)

        if city and self.city.findText(city) >= 0:
            self.city.setCurrentText(city)

        # Emit once to update the UI
        self._emit_selection()

    def _on_country_changed(self, country):
        self.region.clear()
        self.region.addItems(self.repo.regions(country))
        self.region.setEnabled(bool(self.region.count()))
        if self.region.count() > 0:
            self.region.setCurrentIndex(0)
        else:
            self.city.clear()
            self.city.setEnabled(False)

    def _on_region_changed(self, region):
        country = self.country.currentText()
        self.city.clear()
        self.city.addItems(self.repo.cities(country, region))
        self.city.setEnabled(bool(self.city.count()))

    def _emit_selection(self, *_):
        country, region, city = self.selection()
        self.selection_changed.emit(country, region, city)

    def selection(self):
        return (
            self.country.currentText(),
            self.region.currentText(),
            self.city.currentText(),
        )
