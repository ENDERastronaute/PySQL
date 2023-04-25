
def is_APO(num, tokens):
    if tokens[num].type == 'APO':
        num += 1
    
    return num

def create_dictionnary(self):

    input_dict = ''

    while self.current_token.type != 'RACO':
        input_dict += self.current_token.lookahead
        self.advance()
        
        if self.current_index >= len(self.tokens):
            raise Exception("Expected '}'")
    
    input_dict += self.current_token.lookahead
        
    return eval(input_dict)

def evaluate_num(current_index, token):
    pass