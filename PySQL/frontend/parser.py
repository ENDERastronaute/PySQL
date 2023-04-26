
from runtime.interpreter import Interpreter
from utils.tokener import advance

class Parser:
    def __init__(self, tokens, variables, version):
        self.tokens = tokens
        self.variables = variables
        self.version = version
        self.current_token = None
        self.current_index = -1
        self.interpreter = Interpreter(self.tokens, self.variables, self.version, self.current_token, self.current_index)
        self.current_token, self.current_index = advance(self.current_index, self.tokens)

    def parse(self):
        self.interpreter.current_index = self.current_index
        self.interpreter.current_token = self.current_token

        first = True
        if self.current_token is not None:
            while first is True or self.current_token is not None:

                result, self.current_token, self.current_index = self.interpreter.expr()
                first = False

            if self.current_token is not None:
                raise Exception("Unexpected token")
        
            return result