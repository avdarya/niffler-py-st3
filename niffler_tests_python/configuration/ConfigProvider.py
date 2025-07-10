import configparser
import os


global_config = configparser.ConfigParser()
config_path = os.path.join(os.path.dirname(__file__), '..', 'config.ini')
global_config.read(os.path.abspath(config_path))

class ConfigProvider:

    def __init__(self) -> None:
        self.config = global_config

    def get_prop(self, section: str, prop: str):
        return self.config[section].get(prop)

    def get_timeout(self) -> float:
        return float(self.config['ui'].get('timeout'))

    def get_poll(self) -> float:
        return float(self.config['ui'].get('poll'))