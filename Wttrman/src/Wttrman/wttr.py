from requests import get


class Wttr:
    def __init__(self):
        self.base_url = "https://wttr.in/"

    def get_weather(self, city="", state="", country="USA"):
        city = self.city_fixer(city)
        state = self.state_fixer(state)
        output_format = r"?format=Condition:+%C+\nPrecip:+%p/3 hours+\nTemps:+%t(%f)"
        url = f"{self.base_url}{city}+{state}+{country}{output_format}"
        weather = get(url, timeout=5)
        return weather.text

    def city_fixer(self, city=""):
        counter = 0
        city = list(city)
        for character in city:
            if city[counter] == " ":
                city[counter] = "+"
            counter += 1

        return "".join(city)

    def state_fixer(self, state=""):
        counter = 0
        state = list(state)
        for character in state:
            if state[counter] == " ":
                state[counter] = "+"
            counter += 1

        return "".join(state)

    def country_fixer(self, country=""):
        counter = 0
        country = list(country)
        for character in country:
            if country[counter] == " ":
                country[counter] = "+"
            counter += 1

        return "".join(country)
