
from modules.token import Token


class Lexer():
    def lexer(input_string):
        tokens = []

        keywords = [
            'var',
            'cls',
            'stop',
            'if',
            'else'
        ]

        functions = [
            'log',
            'input'
        ]

        current_pos = 0
        stop = False

        while current_pos < len(input_string) and stop == False:
            token_start_pos = current_pos
            lookahead = input_string[current_pos]

            if lookahead == ' ':
                current_pos += 1
            
            elif lookahead == '\n':
                current_pos += 1
                tokens.append(Token('NewLine', lookahead, token_start_pos))
            
            elif lookahead == '+':
                current_pos += 1
                tokens.append(Token('Plus', lookahead, token_start_pos))
            
            elif lookahead == '-':
                current_pos += 1
                tokens.append(Token('Sub', lookahead, token_start_pos))  

            elif lookahead == '*':
                current_pos += 1
                tokens.append(Token('Mult', lookahead, token_start_pos))
            
            elif lookahead == '/':
                current_pos += 1
                tokens.append(Token('Div', lookahead, token_start_pos))
            
            elif lookahead == '=':
                current_pos += 1
                tokens.append(Token('EQ', lookahead, token_start_pos))

            elif lookahead == '!':
                current_pos += 1
                tokens.append(Token('NOT', lookahead, token_start_pos))

            elif lookahead == '>':
                current_pos += 1
                tokens.append(Token('SUP', lookahead, token_start_pos))

            elif lookahead == '<':
                current_pos += 1
                tokens.append(Token('INF', lookahead, token_start_pos))

            elif lookahead.isnumeric():
                text = ''

                while current_pos < len(input_string) and input_string[current_pos].isnumeric():
                    text += input_string[current_pos]
                    current_pos += 1

                tokens.append(Token('Num', text, token_start_pos))

            elif lookahead.isalpha():
                text = ''

                while current_pos < len(input_string) and input_string[current_pos].isalpha():
                    text += input_string[current_pos]
                    current_pos += 1
                
                if current_pos >= len(input_string):
                    current_pos = len(input_string) - 1
                    stop = True

                if text in keywords:
                    tokens.append(Token('Keyword', text, token_start_pos))
                
                elif text in functions or input_string[current_pos] == '(':
                    tokens.append(Token('Func', text, token_start_pos))
                
                else:
                    tokens.append(Token('Alpha', text, token_start_pos))
            
            elif lookahead == '(':
                current_pos += 1
                tokens.append(Token('LPAREN', lookahead, token_start_pos))
            
            elif lookahead == ')':
                current_pos += 1
                tokens.append(Token('RPAREN', lookahead, token_start_pos))

            elif lookahead == '{':
                current_pos += 1
                tokens.append(Token('LACO', lookahead, token_start_pos))    

            elif lookahead == '}':
                current_pos += 1
                tokens.append(Token('RACO', lookahead, token_start_pos))            

            elif lookahead == "'":
                text = ''
                tokens.append(Token('APO', lookahead, token_start_pos))

                current_pos += 1

                if not current_pos >= len(input_string):

                    if input_string[current_pos].isalpha():

                        while current_pos < len(input_string) and input_string[current_pos] != "'":
                            text += input_string[current_pos]
                            current_pos += 1
                
                tokens.append(Token('Alpha', text, token_start_pos))

        

        return tokens