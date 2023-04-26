from components.test import Test
import psycopg2
from frontend.terminal import Terminal
from modules.tabulate.tabulate import tabulate
from runtime.evaluation.beacons import *
from runtime.evaluation.expressions import *
from utils.tokener import advance
from frontend.lexer import Lexer
from runtime.evaluation.conditional import *


class Interpreter:
    def __init__(self, tokens, variables, version, current_token, current_index):
        self.tokens = tokens
        self.variables = variables
        self.version = version
        self.current_token = current_token
        self.current_index = current_index
        self.test = None
        self.stack = []
        self.islastnumeric = False
        self.intest = False
    
    def expr(self):
        result = self.term()

        while (self.current_token is not None and (self.current_token.type == "Plus" or self.current_token.type == "Sub")):
            if self.current_token.type == "Plus":
                self.current_token, self.current_index = advance(self.current_index, self.tokens)
                result += self.term()

            elif self.current_token.type == "Sub":
                self.current_token, self.current_index = advance(self.current_index, self.tokens)
                result -= self.term()

        return result, self.current_token, self.current_index
    
    def term(self):
        result = self.factor()
        while (self.current_token is not None and self.current_token.type in ("Mult", "Div", "Mod", "Flr")):
            if self.current_token.type == "Mult":
                self.current_token, self.current_index = advance(self.current_index, self.tokens)
                result *= self.factor()

            elif self.current_token.type == "Div":
                self.current_token, self.current_index = advance(self.current_index, self.tokens)
                result /= self.factor()

            elif self.current_token.type == "Mod":
                self.current_token, self.current_index = advance(self.current_index, self.tokens)
                result %= self.factor()

            elif self.current_token.type == "Flr":
                self.current_token, self.current_index = advance(self.current_index, self.tokens)
                result //= self.factor()

        return result
    
    def factor(self):
        token = self.current_token

        if token.lookahead not in ('else', 'elif', 'NewLine') and self.intest is False:
            self.test = None
            self.stack.clear()
        
        match token.type:

            case 'LPAREN':
                self.current_token, self.current_index = advance(self.current_index, self.tokens)
                result, self.current_token, self.current_index = self.expr()

                match self.current_token.type:
                    case 'RPAREN':
                        self.current_token, self.current_index = advance(self.current_index, self.tokens)

                    case _:
                        raise Exception("Expected ')'")

                return result
        
            case 'Num':
                alpha = token.lookahead
                tsp = self.current_index

                self.current_token, self.current_index = advance(self.current_index, self.tokens)
                
                if self.current_token is not None:
                    if self.current_token.type in ('Alpha', 'UNDER'):
                        self.current_index, self.current_token, self.tokens[self.current_index].type, self.tokens[self.current_index].lookahead, self.tokens[self.current_index].token_start_pos, self.islastnumeric = evaluate_num(self.current_index, self.current_token, self.tokens, alpha, tsp)
                        
                        return self.expr()
                    
                    else:  
                        return int(token.lookahead)
                
                else:
                    return int(token.lookahead)
        
            case 'Func':
                func_name = token.lookahead

                match func_name:

                    case 'log':
                        if (self.tokens[self.current_index + 1].type != "LPAREN"):
                            raise Exception("Invalid log() function call")
                        
                        arg = ""

                        while (self.current_token is not None and self.current_token.type != "RPAREN"):
                            self.current_token, self.current_index = advance(self.current_index, self.tokens)

                            if self.current_token is not None:
                                if self.current_token.type in ('Num', 'APO', 'Bool', 'Func'):
                                    argu, self.current_token, self.current_index = self.expr()
                                    arg += str(argu)

                                elif self.current_token.type in ('Alpha'):
                                    argu, self.current_token, self.current_index = self.expr()
                                    arg += str(argu)
                            
                            else:
                                raise Exception("Expected ')'")


                        if (self.current_token is None or self.current_token.type != "RPAREN"):
                            raise Exception("Expected ')'")

                        self.current_token, self.current_index = advance(self.current_index, self.tokens)

                        print(arg.removeprefix('log('))

                    case 'input':
                        self.current_token, self.current_index = advance(self.current_index, self.tokens)

                        if self.current_token.type != 'LPAREN':
                            raise Exception("Invalid input() function call")

                        arg = ""

                        while (self.current_token is not None and self.current_token.type != "RPAREN"):
                            self.current_token, self.current_index = advance(self.current_index, self.tokens)
                            
                            if self.current_token is not None:
                                if self.current_token.type == 'Num' or self.current_token.type == 'APO':
                                    argu, self.current_token, self.current_index = self.expr()
                                    arg += str(argu)

                                elif self.current_token.type == 'Alpha':
                                    argu, self.current_token, self.current_index = self.expr()
                                    arg += str(argu)
                            
                            else:
                                raise Exception("Expected ')'")

                        if (self.current_token is None or self.current_token.type != "RPAREN"):
                            raise Exception("Expected ')'")

                        self.current_token, self.current_index = advance(self.current_index, self.tokens)

                        return input(arg.removeprefix('input('))
    
                    case _:
                        raise Exception("Invalid function name")
            
            case 'Keyword':
                var_types = ['Bool', 'Num', 'APO', 'Alpha', 'Func', 'LACO']

                match token.lookahead:
                    case 'let' | 'var':
                        self.current_token, self.current_index = advance(self.current_index, self.tokens)
                        
                        var_name = self.current_token.lookahead

                        if self.current_token.type != 'Alpha':
                            raise Exception("Invalid assignation syntax")
                        
                        self.current_token, self.current_index = advance(self.current_index, self.tokens)

                        if self.current_token.type != 'EQ':
                            raise Exception("Invalid assignation syntax")
                        
                        self.current_token, self.current_index = advance(self.current_index, self.tokens)

                        if self.current_token.type not in var_types:
                            raise Exception("Invalid assignation syntax")

                        var_value, self.current_token, self.current_index = self.expr()
                        
                        self.variables[var_name] = var_value

                        self.current_token, self.current_index = advance(self.current_index, self.tokens)


                    case 'cls':
                        pysql = Terminal('Terminal', f'{self.version}')
                        pysql.start()

                        self.current_token, self.current_index = advance(self.current_index, self.tokens)
                    
                    case 'stop':
                        exit()

                    case 'if':
                        self.current_token, self.current_index = advance(self.current_index, self.tokens)

                        cond = ''

                        while self.current_token.type != 'LACO':
                            cond += self.current_token.lookahead
                            self.current_token, self.current_index = advance(self.current_index, self.tokens)

                            if self.current_index >= len(self.tokens):
                                raise Exception('ph')
                        
                        self.current_token, self.current_index = advance(self.current_index, self.tokens)
                        condition = conditional(cond, self.variables)

                        if condition:
                            self.intest = True
                            self.expr()
                            self.intest = False
                            self.test = None
                        
                        else:
                            self.test = condition
                            
                        while self.current_token.type != 'RACO':
                            self.current_token, self.current_index = advance(self.current_index, self.tokens)
                        
                        self.current_token, self.current_index = advance(self.current_index, self.tokens)

                        self.stack.append(1)

                    
                    case 'elif':
                        if self.test is None and len(self.stack) == 0:
                            raise Exception('sus')
                        
                        elif self.test is not None:
                            self.current_token, self.current_index = advance(self.current_index, self.tokens)

                            cond = ''

                            while self.current_token.type != 'LACO':
                                cond += self.current_token.lookahead
                                self.current_token, self.current_index = advance(self.current_index, self.tokens)

                                if self.current_index >= len(self.tokens):
                                    raise Exception('ph')
                            
                            self.current_token, self.current_index = advance(self.current_index, self.tokens)
                            condition = conditional(cond, self.variables)

                            if condition and not self.test:
                                self.intest = True
                                self.expr()
                                self.intest = False
                                self.test = None
                            
                            else:
                                self.test = condition

                        else:
                            while self.current_token.type != 'RACO':
                                self.current_token, self.current_index = advance(self.current_index, self.tokens)

                        while self.current_token.type != 'RACO':
                            self.current_token, self.current_index = advance(self.current_index, self.tokens)

                        self.current_token, self.current_index = advance(self.current_index, self.tokens)                      

                        self.stack.append(1)

                    
                    case 'else':
                        if self.test is None and len(self.stack) == 0:
                            raise Exception('sus')
                        
                        elif self.test is not None:
                            self.current_token, self.current_index = advance(self.current_index, self.tokens)

                            if self.current_token.type != 'LACO':
                                raise Exception('sus')
                            
                            self.current_token, self.current_index = advance(self.current_index, self.tokens)

                            if not self.test:
                                self.expr()

                        while self.current_token.type != 'RACO':
                            self.current_token, self.current_index = advance(self.current_index, self.tokens)
                        
                        self.current_token, self.current_index = advance(self.current_index, self.tokens)

                    case 'while':
                        self.current_token, self.current_index = advance(self.current_index, self.tokens)

                        condition, self.current_token, self.current_index = self.expr()

                        print(self.current_token.type)

                        first_token = self.current_token
                        first_index = self.current_index

                        if self.current_token.type not in ('EQ', 'LACO', 'INF', 'SUP', 'NOT'):
                            raise Exception("Expected '{'")

                        self.current_token, self.current_index = advance(self.current_index, self.tokens)
                        
                        self.stack.append(self.current_token)

                        while condition:
                            self.expr()

                            if self.current_token.type == 'RACO':
                                self.current_index = first_index
                                self.current_token = first_token

                        self.current_token, self.current_index = advance(self.current_index, self.tokens)
                    

                    case _:
                        self.current_token, self.current_index = advance(self.current_index, self.tokens)

            case 'APO':
                self.current_token, self.current_index = advance(self.current_index, self.tokens)
                num = self.current_index
                arg = ''

                while self.current_token.type != 'APO':
                    arg += str(self.current_token.lookahead)
                    num += 1
                    self.current_token, self.current_index = advance(self.current_index, self.tokens)

                    if num >= len(self.tokens):
                        raise Exception("Expected 'EndStr'")

                self.current_token, self.current_index = advance(self.current_index, self.tokens)

                self.current_token, self.current_index = advance(self.current_index, self.tokens)
                    
                return arg
        
            case 'NewLine':
                self.current_token, self.current_index = advance(self.current_index, self.tokens)
                return self.expr()

            case 'Alpha':
                name = self.current_token.lookahead

                if name not in self.variables :
                    raise Exception("Variable doesn't exist")
                
                self.current_token, self.current_index = advance(self.current_index, self.tokens)

                if self.current_token.type == 'EQ':
                    self.current_token, self.current_index = advance(self.current_index, self.tokens)

                    if self.current_token.type not in ('Bool', 'Num', 'APO', 'Alpha', 'Func', 'LACO'):
                        raise Exception('Invalid reassignation syntax')
                    
                    self.variables[name], self.current_token, self.current_index = self.expr()
                
                arg = self.variables[name]
                
                return arg
        
            case 'Bool':
                match self.current_token.lookahead:

                    case 'true':
                        return True
                    
                    case 'false':
                        return False
                    
                    case _:
                        return None
        
            case 'LACO':
                dictionnary = create_dictionnary()
                self.current_token, self.current_index = advance(self.current_index, self.tokens)

                return dictionnary


            case 'RACO':
                if len(self.stack) == 0:
                    raise Exception("Syntax error : No matching '{'")
                
                self.stack.pop()
                self.current_token, self.current_index = advance(self.current_index, self.tokens)

            case 'INF':
                self.current_token, self.current_index = advance(self.current_index, self.tokens)
                infos, self.current_token, self.current_index = check_balise(self.current_token, self.current_index, self.tokens)

                db = infos[0]
                usr = infos[1]
                pwd = infos[2]
                hst = infos[3]
                prt = infos[4]
                query_pos = infos[5]

                query = self.tokens[query_pos].lookahead

                try:

                    connection = psycopg2.connect(user=usr, password=pwd, host=hst, port=prt, database=db)

                    cursor = connection.cursor()

                    cursor.execute(query)

                    fetched_datas = cursor.fetchall()

                    headers = [desc[0] for desc in cursor.description]

                    print(tabulate(fetched_datas, headers=headers, tablefmt='fancy_grid'))
                
                except psycopg2.DatabaseError as e:
                    raise Exception(f"Database error: {e}")
                
                except psycopg2.Error as e:
                    raise Exception(f"Other SQL error : {e}")

                while self.current_token.type != 'LEndBeacon':
                    self.current_token, self.current_index = advance(self.current_index, self.tokens)

                while self.current_token.type != 'REndBeacon':
                    self.current_token, self.current_index = advance(self.current_index, self.tokens)
                
                self.current_token, self.current_index = advance(self.current_index, self.tokens)

            case _:
                raise Exception("Invalid token type")