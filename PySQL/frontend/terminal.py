#---IMPORTS---#
import os,sys


class Terminal():
    def __init__(self, session, version):
        self.session = session
        self.version = version

    def start(self):
        os.system('cls' if sys.platform == 'win32' else 'clear')

        print('>', end='')

        for i in range(int(((-1 * (len(self.version))) + 43)/2)):
            print('-', end='')

        print(f'PySQL v{self.version}', end='')

        for i in range(int(((-1 * (len(self.version))) + 43)/2)):
            print('-', end='')

    

        print('<', end='')

        print('\n>--------------------license GNU-------------------<')
        print()
