import json
import os


class LocationRepository:
    """Loads location data from JSON files under resources/locations/.

    Each file is named by a short country code (usa.json, united_kingdom.json,
    canada.json, ...). The UI displays a friendly name from DISPLAY_NAMES,
    falling back to a title-cased form of the filename when no override exists.
    """

    DISPLAY_NAMES = {
        "usa": "United States",
        "uk": "United Kingdom",
        "united_kingdom": "United Kingdom",
        "uae": "United Arab Emirates",
    }

    def __init__(self, data_dir=None):
        if data_dir is None:
            data_dir = os.path.join(
                os.path.dirname(__file__), "..", "resources", "locations"
            )
        self.data_dir = os.path.abspath(data_dir)
        self._cache = {}
        self._code_by_display = {}

    def countries(self):
        """Return sorted display names of every country with a JSON file."""
        if not os.path.isdir(self.data_dir):
            return []
        display_names = []
        self._code_by_display = {}
        for name in os.listdir(self.data_dir):
            if not name.endswith(".json"):
                continue
            code = os.path.splitext(name)[0]
            display = self.DISPLAY_NAMES.get(code, code.replace("_", " ").title())
            display_names.append(display)
            self._code_by_display[display] = code
        return sorted(display_names)

    def regions(self, country_display):
        return sorted(self._load(country_display).keys())

    def cities(self, country_display, region):
        return sorted(self._load(country_display).get(region, []))

    def country_code(self, country_display):
        """Return the filename stem (e.g. 'usa') for a display name."""
        if not self._code_by_display:
            self.countries()
        return self._code_by_display.get(
            country_display,
            country_display.lower().replace(" ", "_"),
        )

    def _load(self, country_display):
        code = self.country_code(country_display)
        if code not in self._cache:
            path = os.path.join(self.data_dir, f"{code}.json")
            if os.path.exists(path):
                with open(path, "r", encoding="utf-8") as f:
                    self._cache[code] = json.load(f)
            else:
                self._cache[code] = {}
        return self._cache[code]
