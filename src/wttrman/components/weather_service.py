import requests
from urllib.parse import quote


class WeatherError(Exception):
    """Raised when the weather service cannot be reached or returns an error."""


class WeatherService:
    BASE_URL = "https://wttr.in"
    TIMEOUT = 5

    def get_weather(
        self,
        city: str,
        region: str,
        country: str,
        custom_format: str = None,
        units: str = "m",
    ) -> str:
        location = ", ".join(p for p in (city, region, country) if p)

        # Default fallback if the user hasn't configured anything
        if not custom_format:
            custom_format = "Condition: %C%nPrecip: %p%nTemps: %t (%f)"

        # Safe-encode just the location string
        encoded_location = quote(location)

        # Construct the URL manually to prevent requests from
        # encoding the '%' characters in the format string.
        url = f"{self.BASE_URL}/{encoded_location}?format={custom_format}&{units}"

        try:
            response = requests.get(url, timeout=self.TIMEOUT)
            response.raise_for_status()
        except requests.RequestException as exc:
            raise WeatherError(f"Could not reach weather service: {exc}") from exc
        return response.text
