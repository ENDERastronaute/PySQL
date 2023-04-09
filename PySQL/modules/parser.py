
from modules.terminal import Terminal


class Parser:
    def __init__(self, tokens, variables, version, test):
        self.tokens = tokens
        self.current_token = None
        self.current_index = -1
        self.advance()
        self.variables = variables
        self.version = version
        self.test = test

    def advance(self):
        self.current_index += 1

        if self.current_index < len(self.tokens):
            self.current_token = self.tokens[self.current_index]

        else:
            self.current_token = None

    def parse(self):
        first = True

        while first is True or self.current_token is not None:
            result = self.expr()
            first = False

        if self.current_token is not None:
            raise Exception("Unexpected token")
        
        return result

    def expr(self):
        result = self.term()

        while (self.current_token is not None and (self.current_token.type == "Plus" or self.current_token.type == "Sub")):
            if self.current_token.type == "Plus":
                self.advance()
                result += self.term()

            elif self.current_token.type == "Sub":
                self.advance()
                result -= self.term()

        return result

    def term(self):
        result = self.factor()
        while (self.current_token is not None and (self.current_token.type == "Mult" or self.current_token.type == "Div")):
            if self.current_token.type == "Mult":
                self.advance()
                result *= self.factor()

            elif self.current_token.type == "Div":
                self.advance()
                result /= self.factor()

        return result

    def factor(self):
        token = self.current_token
        if token.type == "LPAREN":
            self.advance()
            result = self.expr()

            if self.current_token.type != "RPAREN":
                raise Exception("Expected ')'")
            
            else:
                self.advance()

            return result
        
        elif token.type == "Num":
            self.advance()
            return int(token.lookahead)
        
        elif token.type == "Func":
            func_name = token.lookahead

            if func_name == "log":
                if (self.tokens[self.current_index + 1].type != "LPAREN"):
                    raise Exception("Invalid log() function call")
                
                arg = ""

                while (self.current_token is not None and self.current_token.type != "RPAREN"):
                    self.advance()

                    if self.current_token is not None:
                        if self.current_token.type == 'Num' or self.current_token.type == 'APO':
                            arg = str(self.expr())

                        elif self.current_token.type == 'Alpha':
                            if self.current_token.lookahead not in list(self.variables.keys()):
                                raise Exception("Variable doesn't exist")

                            arg = str(self.variables[self.current_token.lookahead])
                    
                    else:
                        raise Exception("Expected ')'")


                if (self.current_token is None or self.current_token.type != "RPAREN"):
                    raise Exception("Expected ')'")

                self.advance()

                print(arg.removeprefix('log('))

            elif func_name == 'input':
                self.advance()

                if self.current_token.type != 'LPAREN':
                    raise Exception("Invalid input() function call")

                arg = ""

                while (self.current_token is not None and self.current_token.type != "RPAREN"):
                    self.advance()
                    
                    if self.current_token is not None:
                        if self.current_token.type == 'Num' or self.current_token.type == 'APO':
                            arg = str(self.expr())

                        elif self.current_token.type == 'Alpha':
                            if self.current_token.lookahead not in list(self.variables.keys()):
                                raise Exception("Variable doesn't exist")

                            arg = str(self.variables[self.current_token.lookahead])
                    
                    else:
                        raise Exception("Expected ')'")

                if (self.current_token is None or self.current_token.type != "RPAREN"):
                    raise Exception("Expected ')'")

                self.advance()

                return input(arg.removeprefix('input('))

                

            
            else:
                raise Exception("Invalid function name")
            
        elif token.type == "Keyword":
            var_types = ['Bool', 'Num', 'APO', 'Alpha', 'Func']

            if token.lookahead == 'var':
                self.advance()

                if self.current_token.type != 'Alpha':
                    raise Exception("Invalid assignation syntax")
                
                var_name = self.current_token.lookahead

                self.advance()

                if self.current_token.type != 'EQ':
                    raise Exception("Invalid assignation syntax")
                
                self.advance()

                if self.current_token.type not in var_types:
                    raise Exception("Invalid assignation syntax")

                var_value = self.expr()
                
                self.variables[var_name] = var_value

                self.advance()


            elif token.lookahead == 'cls':
                pysql = Terminal('Terminal', f'{self.version}')
                pysql.start()

                self.advance()
            
            elif token.lookahead == 'stop':
                exit()

            elif token.lookahead == 'if':
                operandes = ['EQ', 'SUP', 'INF', 'NOT']

                self.advance()
                
                if self.current_token.type == 'Alpha':
                    first = self.expr()
                    first = self.variables[first]
                
                else:
                    first = self.expr()

                if self.current_token.type not in operandes:
                    raise Exception("Invalid statement syntax")
                
                if self.current_token.type == 'EQ':
                    self.advance()

                    if self.current_token.type != 'EQ':
                        raise Exception("Invalid statement syntax")
                    
                    self.advance()

                    second = self.expr()

                    mode = '=='

                else:
                    raise Exception("Invalid statement syntax")
                

                if self.current_token.type != 'LACO':
                    raise Exception('Invalid statement syntax')
                
                if mode == '==':
                    if first == second:
                        self.advance()
                        self.expr()

                        if self.current_token is not None:

                            if self.current_token.type != 'RACO':
                                raise Exception('Invalid statement syntax')
                        
                        else:
                            raise Exception('Invalid statement syntax')
                        
                        self.advance()
                    
                    else:
                        while self.current_token.type != 'RACO':
                            self.advance()
                        
                        self.advance()
            
            elif token.lookahead == 'else':
                if self.test == None:
                    raise Exception("Invalid statement syntax")
                
                


                    
        
        elif self.current_token.type == 'APO':
            self.advance()
            num = self.current_index
            arg = ''

            while self.current_token.type != 'APO':
                arg += str(self.current_token.lookahead)
                num += 1
                self.advance()

                if num >= len(self.tokens):
                    raise Exception("Expected 'EndStr'")
            
            self.advance()

            self.advance()
                
            return arg
        
        elif self.current_token.type == 'NewLine':
            self.advance()
            self.expr()

        elif self.current_token.type == 'Alpha':
            if self.current_token.lookahead not in self.variables :
                raise Exception("Variable doesn't exist")
            
            arg = self.current_token.lookahead
            
            self.advance()
            
            return arg

        else:
            raise Exception("Invalid token type")