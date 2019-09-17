import appdirs

__title__ = "webget"
__author__ = "modora"
__version__ = "0.0.1"

app_data = appdirs.user_data_dir(__title__, roaming=True)
app_config = appdirs.user_cache_dir(__title__)