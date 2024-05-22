from dataclasses import dataclass
import os
from string import Template
import tomllib

from mk_build.util import todo

class ConfigFile:
    def __init__(self, name, default_config):
        home_dir = os.getenv('HOME')
        assert home_dir is not None

        xdg_config_home = os.getenv('XDG_CONFIG_HOME', f'{home_dir}/.config')
        xdg_data_home = os.getenv('XDG_DATA_HOME', f'{home_dir}/.local/share')

        dir_path = f'{xdg_config_home}/{name}'
        file_path = f'{dir_path}/{name}.toml'

        default_config = Template(default_config).substitute(
            xdg_data_home=xdg_data_home)

        if not os.path.isfile(file_path):
            if not os.path.isdir(dir_path):
                os.makedirs(dir_path)
            with open(file_path, 'w') as file:
                file.write(default_config)

        with open(file_path, 'rb') as file:
            self.data = tomllib.load(file)
            print(f'dict {self.data}')


@dataclass
class Config:

    @classmethod
    def load(cls):
        default_config_template = ''

        config_file = ConfigFile('config', default_config_template)
        data = config_file.data

        return cls()


dry_run = False
trace = False

todo('use config file here')
builddir = '/p/mforth/_build'
