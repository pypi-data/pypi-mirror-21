from django.apps import AppConfig


class APIConfig(AppConfig):
    name = '.'.join(__name__.split('.')[:-1])  # Package with `apps` module
    label = '_'.join(__name__.split('.')[:-1])
    verbose_name = 'ICEkitAPI'
