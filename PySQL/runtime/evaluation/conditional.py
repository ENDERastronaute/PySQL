from frontend.lexer import Lexer
from utils.tokener import advance


def create_cond(tokens, current_index, current_token):
    cond = ''

    while current_token.type != 'LACO':
        if current_token.type not in ('Str', 'APO'):
            cond += current_token.lookahead + ' '

        else:
            cond += current_token.lookahead
        current_token, current_index = advance(current_index, tokens)

        if current_index >= len(tokens):
            raise Exception('ph')
    
    current_token, current_index = advance(current_index, tokens)

    return cond, current_token, current_index

def conditional(cond, variables):
    tokens = Lexer.lexer(cond)

    parsed_cond = ''

    for i in range(len(tokens)):

        match tokens[i].type:
            case 'Alpha':

                if tokens[i].lookahead not in variables:
                    print(tokens[i].lookahead)
                    raise Exception('Var dont exist')
                
                if isinstance(variables[tokens[i].lookahead], str):
                    parsed_cond += '"'
                    parsed_cond += str(variables[tokens[i].lookahead])
                    parsed_cond += '"'

                else:
                    parsed_cond += str(variables[tokens[i].lookahead])

            case 'Keyword':
                parsed_cond += ' ' + tokens[i].lookahead + ' '

            case _:
                parsed_cond += tokens[i].lookahead
    
    return eval(parsed_cond)