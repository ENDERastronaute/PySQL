
from utils.tokener import advance

def is_APO(num, tokens):
    if tokens[num].type == 'APO':
        num += 1
    
    return num

def create_dictionnary(current_token, current_index, tokens):
    """Not Implemented Yet"""
    pass

def evaluate_num(current_index, current_token, tokens, alpha, tsp):
    while current_token.type in ('Alpha', 'UNDER'):
        alpha += current_token.lookahead
        current_token, current_index = advance(current_index, tokens)
    
    current_index -= 1
    current_token = tokens[current_index]
    
    tokens[current_index].type = 'Alpha'
    tokens[current_index].lookahead = alpha
    tokens[current_index].token_start_pos = tsp

    islastnumeric = True

    return current_index, current_token, tokens[current_index].type, tokens[current_index].lookahead, tokens[current_index].token_start_pos, islastnumeric