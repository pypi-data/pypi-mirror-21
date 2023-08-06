from django.apps import AppConfig


class AppConfig(AppConfig):
    name = '.'.join(__name__.split('.')[:-1])
    label = "icekit_plugins_map_with_text"
    verbose_name = "Map with text"
