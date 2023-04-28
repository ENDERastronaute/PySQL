
from components.token import Token


class Lexer():
    def lexer(input_string):
        tokens = []

        keywords = [
            'let',
            'var',
            'cls',
            'stop',
            'if',
            'elif',
            'else',
            'while',
            'and',
            'or'
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

            match lookahead:

                case ' ':
                    current_pos += 1
                    
                
                case '\n':
                    current_pos += 1
                    tokens.append(Token('NewLine', lookahead, token_start_pos))
                
                case '+':
                    current_pos += 1
                    tokens.append(Token('Plus', lookahead, token_start_pos))
                
                case '-':
                    current_pos += 1
                    tokens.append(Token('Sub', lookahead, token_start_pos))  

                case '*':
                    current_pos += 1
                    tokens.append(Token('Mult', lookahead, token_start_pos))
                
                case '/':
                    current_pos += 1

                    match input_string[current_pos]:
                        
                        case '/':
                            current_pos += 1
                            tokens.append(Token('Flr', lookahead, token_start_pos))
                    
                        case _:
                            tokens.append(Token('Div', lookahead, token_start_pos))

                case '%':
                    current_pos += 1
                    tokens.append(Token('Mod', lookahead, token_start_pos))
                
                case '=':
                    current_pos += 1
                    tokens.append(Token('EQ', lookahead, token_start_pos))

                case '!':
                    current_pos += 1
                    tokens.append(Token('NOT', lookahead, token_start_pos))

                case '>':
                    current_pos += 1
                    tokens.append(Token('SUP', lookahead, token_start_pos))

                case '<':
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

                case num if lookahead.isnumeric():
                    text = ''

                    while current_pos < len(input_string) and input_string[current_pos].isnumeric():
                        text += input_string[current_pos]
                        current_pos += 1

                    tokens.append(Token('Num', text, token_start_pos))

                case alpha if lookahead.isalpha():
                    text = ''

                    while current_pos < len(input_string) and (input_string[current_pos].isalpha() or input_string[current_pos].isnumeric() or input_string[current_pos] == '_'):
                        text += input_string[current_pos]
                        current_pos += 1
                    
                    if current_pos >= len(input_string):
                        current_pos = len(input_string) - 1
                        stop = True

                    match text:

                        case keyword if text in keywords:
                            tokens.append(Token('Keyword', text, token_start_pos))
                        
                        case func if text in functions or input_string[current_pos] == '(':
                            tokens.append(Token('Func', text, token_start_pos))
                        
                        case boolean if text in bools:
                            tokens.append(Token('Bool', text, token_start_pos))
                        
                        case _:
                            tokens.append(Token('Alpha', text, token_start_pos))
                
                case '(':
                    current_pos += 1
                    tokens.append(Token('LPAREN', lookahead, token_start_pos))
                
                case ')':
                    current_pos += 1
                    tokens.append(Token('RPAREN', lookahead, token_start_pos))

                case '{':
                    current_pos += 1
                    tokens.append(Token('LACO', lookahead, token_start_pos))

                case '}':
                    current_pos += 1
                    tokens.append(Token('RACO', lookahead, token_start_pos))

                case '[':
                    current_pos += 1
                    tokens.append(Token('BLACO', lookahead, token_start_pos))
                
                case ']':
                    current_pos += 1
                    tokens.append(Token('BRACO', lookahead, token_start_pos))

                case "'" | '"':
                    text = ''
                    tokens.append(Token('APO', lookahead, token_start_pos))

                    current_pos += 1

                    if not current_pos >= len(input_string) and not start_str:

                        while current_pos < len(input_string) and input_string[current_pos] not in ("'", '"'):
                            text += input_string[current_pos]
                            current_pos += 1
                    
                    start_str = not start_str
                    
                    tokens.append(Token('Str', text, token_start_pos))

                case ',':
                    current_pos += 1
                    tokens.append(Token('COMMA', lookahead, token_start_pos))

                case ':':
                    current_pos += 1
                    tokens.append(Token('DP', lookahead, token_start_pos))
                
                case '_':
                    current_pos += 1
                    text = '_'

                    if input_string[current_pos].isalpha() or input_string[current_pos].isnumeric() or input_string[current_pos] == '_':
                        while current_pos < len(input_string) and (input_string[current_pos].isalpha() or input_string[current_pos].isnumeric() or input_string[current_pos] == '_'):
                            text += input_string[current_pos]
                            current_pos += 1
                        
                        tokens.append(Token('Alpha', text, token_start_pos))
                    
                    else:
                        tokens.append(Token('UNDER', lookahead, token_start_pos))
                
                case '.':
                    current_pos += 1
                    tokens.append(Token('DOT', lookahead, token_start_pos))  

                case '|':
                    current_pos += 1

                    tokens.append(Token('PIPE', lookahead, token_start_pos))
                
                case '&':
                    current_pos += 1
                    
                    tokens.append(Token('COMAND', lookahead, token_start_pos))
                
                case _:
                    raise Exception('Invalid token type')

        

        return tokens