
class Token():
    def __init__(self, type, lookahead, token_start_pos):
        self.type = type
        self.lookahead = lookahead
        self.token_start_pos = token_start_pos
        self.endof = None