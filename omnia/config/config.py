import os
import ConfigParser

class Config(object):
    """Configuration Object"""
    def __init__(self, path="/etc/procure.conf"):
        self.path = path
        self.config = ConfigParser.ConfigParser()
        self.config.read(self.path)
    
    def get(self, group, key):
        return self.config.get(group, key)
