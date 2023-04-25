
from runtime.evaluation.expressions import *
from runtime.evaluation.tokener import advance

def check_balise(current_token, current_index, tokens):
    db = None
    usr = None
    pwd = None
    prt = None
    hst = None
    query_pos = None

    if current_token.type == 'Query':
        query_pos = current_index
        current_token, current_index = advance(current_index, tokens)

    if current_token.lookahead != 'SQL':
        raise Exception('Invalid beacon')
    
    current_token, current_index = advance(current_index, tokens)

    if current_token.lookahead == 'from':
        pass

    if current_token.type != 'SUP':
        raise Exception('No end of beacon')

    num = current_index - 1

    while tokens[num].type != 'INF':
        if num >= len(tokens) - 1:
            raise Exception('No end of beacon')
        
        num += 1

    base_num = num
    num += 1

    while tokens[num].type != 'SUP':
        test = tokens[num].lookahead

        if num >= len(tokens) - 1:
            raise Exception('No end of beacon')
        
        if tokens[num].lookahead == 'db':
            num += 1
            num = is_APO(num, tokens)
            db = tokens[num].lookahead

        elif tokens[num].lookahead == 'user':
            num += 1
            num = is_APO(num, tokens)
            usr = tokens[num].lookahead
        
        elif tokens[num].lookahead == 'pwd':
            num += 1
            num = is_APO(num, tokens)
            pwd = tokens[num].lookahead

        elif tokens[num].lookahead == 'host':
            num += 1
            num = is_APO(num, tokens)
            hst = tokens[num].lookahead

        elif tokens[num].lookahead == 'port':
            num += 1
            num = is_APO(num, tokens)
            prt = tokens[num].lookahead

        test = tokens[num].lookahead

        num += 1
        num = is_APO(num, tokens)

        test = tokens[num].type

        if tokens[num].type not in ('COMMA', 'SUP', 'Alpha'):
            raise Exception('Invalid query informations')

    for i in (db, usr, pwd, hst, prt, query_pos):
        if i is None:
            raise Exception('Not enough request informations')
            

    tokens[base_num].type = 'LEndBeacon'
    tokens[num].type = 'REndBeacon'

    return [db, usr, pwd, hst, prt, query_pos], current_token, current_index