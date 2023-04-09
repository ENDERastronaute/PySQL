
#---IMPORTS---#

from modules.terminal import Terminal
from modules.lexer import Lexer
from modules.parser import Parser
import os,sys

version = '0.5'


#---MAIN---#

def main():
    variables = {}
    test = None
    print(sys.argv)

    if len(sys.argv) == 1:

        pysql = Terminal('Terminal', f'{version}')
        pysql.start()

        while True:
            input_string = input('~$ ')
            tokens = Lexer.lexer(input_string)

            parser = Parser(tokens, variables, version, test)
            result = parser.parse()
    
    elif sys.argv[1] == '-r':
        if len(sys.argv) == 3:
            with open(f'{sys.argv[2]}', mode='r', encoding='utf-8') as f:
                content = f.read()

            tokens = Lexer.lexer(content)

            parser = Parser(tokens, variables, version)
            result = parser.parse()

        else:
            raise Exception('Not enough args')




if __name__ == '__main__':
    main()
