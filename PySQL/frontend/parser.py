
import psycopg2
from frontend.terminal import Terminal
from modules.tabulate.tabulate import tabulate



class Test:
    def __init__(self, first, mode, second):
        self.first = first
        self.mode = mode
        self.second = second


class Parser:
    def __init__(self, tokens, variables, version):
        self.tokens = tokens
        self.current_token = None
        self.current_index = -1
        self.advance()
        self.variables = variables
        self.version = version
        self.test = None
        self.stack = []

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
        while (self.current_token is not None and self.current_token.type in ("Mult", "Div", "Mod", "Flr")):
            if self.current_token.type == "Mult":
                self.advance()
                result *= self.factor()

            elif self.current_token.type == "Div":
                self.advance()
                result /= self.factor()

            elif self.current_token.type == "Mod":
                self.advance()
                result %= self.factor()

            elif self.current_token.type == "Flr":
                self.advance()
                result //= self.factor()

        return result

    def factor(self):
        token = self.current_token

        if token.lookahead != 'else' and token.type != 'NewLine' and len(self.stack) == 0:
            self.test = None

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
            var_types = ['Bool', 'Num', 'APO', 'Alpha', 'Func', 'LACO']

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
                    if self.current_token.type != 'NewLine':
                        raise Exception('Invalid statement syntax')
                
                self.stack.append(self.current_token)
                
                if mode == '==':
                    if first == second:
                        self.advance()
                        self.expr()

                        if self.current_token is not None:

                            if self.current_token.type != 'RACO':
                                if self.current_token.type != 'NewLine':
                                    raise Exception('Invalid statement syntax')
                                
                                else:
                                    valid = False
                                    num = self.current_index

                                    while num < len(self.tokens):
                                        num += 1
                                        
                                        if self.tokens[num].type == 'RACO':
                                            valid = True
                                            break

                                    if not valid:
                                        raise Exception("Invalid statement syntax")
                        
                        else:
                            raise Exception('Invalid statement syntax')
                        
                        self.advance()
                    
                    else:
                        while self.current_token.type != 'RACO':
                            self.advance()
                        
                        self.advance()
                    
                self.test = Test(first, mode, second)
            
            elif token.lookahead == 'else':
                if self.test == None:
                    raise Exception("No if statement")
                
                first = self.test.first
                mode = self.test.mode
                second = self.test.second

                self.advance()

                if self.current_token.type != 'LACO':
                    if self.current_token.type != 'NewLine':
                        raise Exception('Invalid statement syntax')
                
                self.stack.append(self.current_token)
                
                if mode == '==':
                    if first != second:
                        self.advance()
                        self.expr()

                        if self.current_token is not None:

                            if self.current_token.type != 'RACO':
                                if self.current_token.type != 'NewLine':
                                    raise Exception('Invalid statement syntax')
                                
                                else:
                                    valid = False
                                    num = self.current_index

                                    while num < len(self.tokens):
                                        num += 1
                                        
                                        if self.tokens[num].type == 'RACO':
                                            valid = True
                                            break

                                    if not valid:
                                        raise Exception("Invalid statement syntax")
                        
                        else:
                            raise Exception('Invalid statement syntax')
                        
                        self.advance()
                    
                    else:
                        while self.current_token.type != 'RACO':
                            self.advance()
                        
                        self.advance()
            
            elif token.lookahead == 'while':
                self.advance()

                condition = self.expr()

                print(self.current_token.type)

                first_token = self.current_token
                first_index = self.current_index

                if self.current_token.type not in ('EQ', 'LACO', 'INF', 'SUP', 'NOT'):
                    raise Exception("Expected '{'")

                self.advance()
                
                self.stack.append(self.current_token)

                while condition:
                    self.expr()

                    if self.current_token.type == 'RACO':
                        self.current_index = first_index
                        self.current_token = first_token

                self.advance()
                            


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
            return self.expr()

        elif self.current_token.type == 'Alpha':
            if self.current_token.lookahead not in self.variables :
                raise Exception("Variable doesn't exist")
            
            arg = self.current_token.lookahead
            
            self.advance()
            
            return arg
        
        elif self.current_token.type == 'LACO':
            dictionnary = self.create_dictionnary()
            self.advance()

            return dictionnary


        elif self.current_token.type == 'RACO':
            if len(self.stack) == 0:
                raise Exception("Syntax error : No matching '{'")
            
            self.stack.pop()
            self.advance()

        elif self.current_token.type == 'INF':
            self.advance()
            infos = self.check_balise()

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
                self.advance()

            while self.current_token.type != 'REndBeacon':
                self.advance()
            
            self.advance()

        else:
            raise Exception("Invalid token type")

    def check_balise(self):
        db = None
        usr = None
        pwd = None
        prt = None
        hst = None
        query_pos = None

        if self.current_token.type == 'Query':
            query_pos = self.current_index
            self.advance()

        if self.current_token.lookahead != 'SQL':
            raise Exception('Invalid beacon')
        
        self.advance()

        if self.current_token.lookahead == 'from':
            pass

        if self.current_token.type != 'SUP':
            raise Exception('No end of beacon')

        num = self.current_index - 1

        while self.tokens[num].type != 'INF':
            if num >= len(self.tokens) - 1:
                raise Exception('No end of beacon')
            
            num += 1

        base_num = num
        num += 1

        while self.tokens[num].type != 'SUP':
            test = self.tokens[num].lookahead

            if num >= len(self.tokens) - 1:
                raise Exception('No end of beacon')
            
            if self.tokens[num].lookahead == 'db':
                num += 1
                num = self.is_APO(num)
                db = self.tokens[num].lookahead

            elif self.tokens[num].lookahead == 'user':
                num += 1
                num = self.is_APO(num)
                usr = self.tokens[num].lookahead
            
            elif self.tokens[num].lookahead == 'pwd':
                num += 1
                num = self.is_APO(num)
                pwd = self.tokens[num].lookahead

            elif self.tokens[num].lookahead == 'host':
                num += 1
                num = self.is_APO(num)
                hst = self.tokens[num].lookahead

            elif self.tokens[num].lookahead == 'port':
                num += 1
                num = self.is_APO(num)
                prt = self.tokens[num].lookahead

            test = self.tokens[num].lookahead

            num += 1
            num = self.is_APO(num)

            test = self.tokens[num].type

            if self.tokens[num].type not in ('COMMA', 'SUP', 'Alpha'):
                raise Exception('Invalid query informations')

        for i in (db, usr, pwd, hst, prt, query_pos):
            if i is None:
                raise Exception('Not enough request informations')
                

        self.tokens[base_num].type = 'LEndBeacon'
        self.tokens[num].type = 'REndBeacon'

        return [db, usr, pwd, hst, prt, query_pos]

    def is_APO(self, num):
        if self.tokens[num].type == 'APO':
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