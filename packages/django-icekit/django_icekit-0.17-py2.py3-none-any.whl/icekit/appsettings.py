from django.conf import settings

ICEKIT = getattr(settings, 'ICEKIT', {})

# Sources for `icekit.plugins.FileSystemLayoutPlugin`.
LAYOUT_TEMPLATES = ICEKIT.get('LAYOUT_TEMPLATES', [])

# File class referenced by `icekit.plugins.file.abstract_models.AbstractFileItem`.
FILE_CLASS = ICEKIT.get('FILE_CLASS', 'icekit_plugins_file.File')

DASHBOARD_FEATURED_APPS = ICEKIT.get('DASHBOARD_FEATURED_APPS', ())
DASHBOARD_SORTED_APPS = ICEKIT.get('DASHBOARD_SORTED_APPS', ())
