
# Error function

def throw():
    pass

# Errors

class SyntaxicError:
    def __init__(self, msg, line, filename, offset):
        self.msg = msg
        self.line = line
        self.filename = filename
        self.offset = offset


class AssignationError(SyntaxicError):
    def __init__(self, msg, line, filename, offset, varname):
        super().__init__(msg, line, filename, offset)
        
        self.varname = varname