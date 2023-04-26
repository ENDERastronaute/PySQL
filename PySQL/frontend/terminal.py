#---IMPORTS---#
import os,sys


class Terminal():
    def __init__(self, session, version):
        self.session = session
        self.version = version

    def start(self):
        os.system('cls' if sys.platform == 'win32' else 'clear')
        print(f'>--------------------PySQL v{self.version}--------------------<')
        print('>--------------------license GNU-------------------<')
        print()
