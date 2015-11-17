from django.conf import settings


STYLUS_EXECUTABLE = getattr(settings, "STYLUS_EXECUTABLE", "stylus")
STYLUS_USE_CACHE = getattr(settings, "STYLUS_USE_CACHE", True)
STYLUS_CACHE_TIMEOUT = getattr(settings, "STYLUS_CACHE_TIMEOUT", 60 * 60 * 24 * 30) # 30 days
STYLUS_MTIME_DELAY = getattr(settings, "STYLUS_MTIME_DELAY", 10) # 10 seconds
STYLUS_OUTPUT_DIR = getattr(settings, "STYLUS_OUTPUT_DIR", "STYLUS_CACHE")
