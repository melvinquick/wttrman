<p align="center">
  <img src="https://raw.githubusercontent.com/melvinquick/wttrman/main/src/wttrman/resources/images/wttrman-256.png" alt="Wttrman Logo" />
</p>

<div align="center">
  <a href="https://github.com/melvinquick/wttrman#about">About</a> | 
  <a href="https://github.com/melvinquick/wttrman#installation">Installation</a> | 
  <a href="https://github.com/melvinquick/wttrman#useful-information">Useful Information</a>
</div>

<br>

<p align="center"><a href="https://pypi.org/project/wttrman/"><img src="https://img.shields.io/pypi/v/wttrman?style=for-the-badge&labelColor=F85149&color=F85149&logo=pypi&logoColor=FFFFFF&label=PyPI" alt="PyPI Version"></a>&nbsp;&nbsp;<a href="https://github.com/melvinquick/wttrman"><img src="https://img.shields.io/badge/GitHub-21262D?style=for-the-badge&labelColor=21262D&logo=github&logoColor=FFFFFF&color=21262D" alt="GitHub"></a></p>

<p align="center"><a href="https://ko-fi.com/melvinquick"><img src="https://img.shields.io/badge/Ko--fi-FFA657?style=for-the-badge&labelColor=FFA657&logo=kofi&logoColor=FFFFFF&color=FFA657" alt="Ko-fi"></a>&nbsp;&nbsp;<a href="https://github.com/sponsors/melvinquick"><img src="https://img.shields.io/badge/GitHub%20Sponsors-D2A8FF?style=for-the-badge&labelColor=D2A8FF&logo=githubsponsors&logoColor=FFFFFF&color=D2A8FF" alt="GitHub Sponsors"></a></p>

<br>

## About

Wttrman is a GUI front-end for [wttr.in](https://wttr.in). It was built to provide a clean, condensed weather report without the clutter of traditional weather websites.

I built Wttrman because I wanted a fast, native desktop app that gave me exactly the weather metrics I cared about, in a format that was easy to read at a glance.

### Features

✅ Support for multiple countries (US, UK, Canada, and more!)  
✅ Fully customizable weather output (Condition, Temp, Wind, Humidity, Precip, Pressure, UV)  
✅ Metric and USCS unit support  
✅ Custom emoji integration for weather conditions  
✅ Multiple themes for accessibility  
✅ Configurable startup defaults (country, state, city, etc.)

## Installation

The installer sets up a dedicated venv and creates a desktop shortcut.

```
curl -s https://raw.githubusercontent.com/melvinquick/wttrman/main/install.py | python3 - wttrman
```

### Supported Operating Systems

✅ Linux  
❌ Mac  
❌ Windows

## Useful Information

### Customization

Wttrman is designed to give you exactly the data you want. Open **Preferences** from the menu bar to:

- **Select your Theme:** Choose from 12 built-in themes, including the custom Wttrman Dark/Light palettes. Themes apply instantly.
- **Choose your Units:** Toggle between Metric (°C, km/h) and USCS (°F, mph).
- **Toggle Weather Metrics:** Check or uncheck specific data points (e.g., if you don't care about UV Index or Pressure, simply turn them off).
- **Enable Emojis:** Toggle the emoji icons for weather conditions on or off.
- **Set Startup Defaults:** Pin a specific country, state, and city to load every time you open the app. (If set to "None", the app will remember your last searched location instead).

### Location Support

Wttrman currently includes hand-curated location data for the following countries:

- Australia
- Canada
- France
- Germany
- Ireland
- Japan
- New Zealand
- United Kingdom
- United States

If you want to add more countries, you can easily drop a new `.json` file into the `resources/locations/` directory. Wttrman will automatically detect it and add it to the dropdown on the next launch.
