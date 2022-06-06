import configparser

class GetConfig:

    def __init__(self, propFile = "app.properties" ):
        self.config = configparser.ConfigParser()
        self.config.read( propFile )

    def getProperty(self, property, section="app"):
        try:
            return self.config.get( section, property )
        except:
            return "NULL"
