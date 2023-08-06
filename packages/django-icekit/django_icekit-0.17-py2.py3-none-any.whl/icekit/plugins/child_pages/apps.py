from django.apps import AppConfig


class AppConfig(AppConfig):
    name = '.'.join(__name__.split('.')[:-1])
    label = "icekit_plugins_child_pages"
    verbose_name = "Child pages"
