import configparser
import os


global_config = configparser.ConfigParser()
# global_config.read('config.ini')
config_path = os.path.join(os.path.dirname(__file__), '..', 'config.ini')
global_config.read(os.path.abspath(config_path))

class ConfigProvider:

    def __init__(self) -> None:
        self.config = global_config

    def get_prop(self, section: str, prop: str):
        return self.config[section].get(prop)

    def get_timeout(self) -> float:
        return float(self.config['ui'].getint('timeout'))

    def get_ui_base_url(self) -> str:
        return self.config['ui'].get('base_url')

    def get_ui_auth_url(self) -> str:
        return self.config['ui'].get('auth_url')