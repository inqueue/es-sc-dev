import os.path
import ConfigParser

class ConfigError(BaseException):
    pass

class Config:
    _opts = {}

    def __init__(self):
        pass

    def config_present(self):
        return os.path.isfile(self._config_file())

    def load_config(self):
        config = ConfigParser.ConfigParser()
        config.read(self._config_file())

        for section in config.sections():
            section_options = {}

            for option in config.options(section):
                section_options[option] = config.get(section, option)

            self._opts[section] = section_options

        return self._opts

    def _config_dir(self):
        return "%s/.es-soundcloud" % os.path.expanduser("~")

    def _config_file(self):
        return "%s/es-soundcloud.ini" % self._config_dir()