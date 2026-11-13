DEFAULT_THEME = "wttrman_dark"


class ThemeManager:
    """Applies a QSS template with theme tokens and re-polishes registered widgets."""

    DEFAULT_THEME = DEFAULT_THEME

    def __init__(self, themes, qss_template):
        # Pop 'general' instead of 'geometry'
        self.general = themes.pop("general", {})
        self.themes = themes
        self.qss_template = qss_template
        self._registered = []

    def register(self, widget):
        if widget not in self._registered:
            self._registered.append(widget)

    def apply(self, widget, theme_name):
        if theme_name not in self.themes:
            theme_name = self.DEFAULT_THEME
        widget.setStyleSheet(self._render(theme_name))
        for w in self._registered:
            self._repolish(w)
        return theme_name

    def _render(self, theme_name):
        # Merge the general tokens with the specific theme tokens
        tokens = {**self.general, **self.themes[theme_name]}
        qss = self.qss_template
        for key, value in tokens.items():
            qss = qss.replace(f"@{key}", value)
        return qss

    def _repolish(self, widget):
        widget.style().unpolish(widget)
        widget.style().polish(widget)
        widget.update()
