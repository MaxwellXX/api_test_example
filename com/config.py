import os
import configparser


class Config(object):
    # 使用_new关键字实现单例模式， 节约内存
    def __new__(cls):
        if not hasattr(cls, "_ins"):
            cls._ins = super().__new__(cls)
            # print('in __new__')
        return cls._ins

    def __init__(self):
        file_path = '../config/config.ini'
        super().__init__()
        # file_path = 'config/config.ini'
        path_current_directory = os.path.dirname(__file__)
        self.path_config_file = os.path.join(path_current_directory, file_path)
        config = configparser.ConfigParser()
        config.read(self.path_config_file)  # read configurations from config file
        self.config = config

    def get_config(self, section, key):
        return self.config[section][key]

    def get_section(self, section):
        return self.config[section]

    def get_env(self):
        debug = self.get_config('DEFAULT', 'DEBUG')
        return  self.get_section('DEV') if debug == 'True' else self.get_section('PRD')
        #return env

if __name__ == '__main__':
    c = Config()
    c1 = Config()
    print(id(c))
    print(id(c1))
    print(type(c.config))
    print(c.path_config_file)
    print(type(c.get_section('DEV')))
    print(c.get_config('DEFAULT', 'DEBUG'))
    print(c.get_env())
    #print(c.get_config('CSV','API_CSV_PATH'))
    #print(c.get_config('LOG', 'LOG_FILE_PATH'))
    #print(c.get_env()['HOST'])