class Variable:
    def __init__(self, name):
        self.name = name

class Loop:
    def __init__(self, loop_type, args):
        """loop_type -> 0 - while, 1 - for, 2 - while"""
        self.loop_type = loop_type
        self.args = list(args)

class Constant:
    def __init__(self, value):
        self.value = value

class Function:
    def __init__(self, function_name, return_type, args):
        self.function_name = function_name
        self.args = list(args)
        self.return_type = return_type

class Decision:
    def __init__(self, decision_type, arg, cases = None):
        """decision_type -> 0 - if, 1 - switch"""
        self.decision_type = decision_type
        self.arg = arg
        if(decision_type == 1 and cases != None):
            self.cases = list(cases)

class Others:
    def __init__(self, 
