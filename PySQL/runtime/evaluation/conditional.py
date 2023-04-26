from frontend.lexer import Lexer



def conditional(cond, variables):
    tokens = Lexer.lexer(cond)

    parsed_cond = ''

    for i in range(len(tokens)):

        if tokens[i].type == 'Alpha':
            if tokens[i].lookahead not in variables:
                print(tokens[i].lookahead)
                raise Exception('Var dont exist')
            
            if isinstance(variables[tokens[i].lookahead], str):
                parsed_cond += '"'
                parsed_cond += str(variables[tokens[i].lookahead])
                parsed_cond += '"'

            else:
                parsed_cond += str(variables[tokens[i].lookahead])

        else:
            parsed_cond += tokens[i].lookahead
    
    return eval(parsed_cond.replace("'", '"'))