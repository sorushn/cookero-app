import configparser

class Settings:
    def __init__(self, config_file):
        self.config = configparser.ConfigParser()
        self.config.read(config_file)

    def get(self, section, option):
        return self.config.get(section, option)


settings = Settings("..//settings.ini")