
from environment.token import Token


class Lexer():
    def lexer(input_string):
        tokens = []

        keywords = [
            'let',
            'cls',
            'stop',
            'if',
            'else',
            'while'
        ]

        functions = [
            'log',
            'input'
        ]

        bools = [
            'true',
            'false',
            'none'
        ]

        current_pos = 0
        stop = False
        start_str = False

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
                
                if input_string[current_pos] != '/':
                    tokens.append(Token('Div', lookahead, token_start_pos))
                
                else:
                    current_pos += 1
                    tokens.append(Token('Flr', lookahead, token_start_pos))

            elif lookahead == '%':
                current_pos += 1
                tokens.append(Token('Mod', lookahead, token_start_pos))
            
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

                is_query = True

                try:
                    for i in range(3):
                        if input_string[current_pos + i] not in ('S', 'Q', 'L'):
                            is_query = False

                except:
                    pass

                if is_query:
                    query = ''
                    c_pos = current_pos + 3

                    while input_string[c_pos] != '<':
                        query += input_string[c_pos]
                        c_pos += 1

                    tokens.append(Token('Query', query.removeprefix('>'), token_start_pos))

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
                
                elif text in bools:
                    tokens.append(Token('Bool', text, token_start_pos))
                
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

            elif lookahead == '[':
                current_pos += 1
                tokens.append(Token('BLACO', lookahead, token_start_pos))
            
            elif lookahead == ']':
                current_pos += 1
                tokens.append(Token('BRACO', lookahead, token_start_pos))

            elif lookahead in ("'", '"'):
                text = ''
                tokens.append(Token('APO', lookahead, token_start_pos))

                current_pos += 1

                if not current_pos >= len(input_string) and not start_str:

                    while current_pos < len(input_string) and input_string[current_pos] not in ("'", '"'):
                        text += input_string[current_pos]
                        current_pos += 1
                
                start_str = not start_str
                
                tokens.append(Token('Alpha', text, token_start_pos))

            elif lookahead == ',':
                current_pos += 1
                tokens.append(Token('COMMA', lookahead, token_start_pos))

            elif lookahead == ':':
                current_pos += 1
                tokens.append(Token('DP', lookahead, token_start_pos))
               
            elif lookahead == '_':
                current_pos += 1
                tokens.append(Token('UNDER', lookahead, token_start_pos))
            
            else:
                raise Exception('Invalid token type')

        

        return tokens