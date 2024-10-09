# runtime.py

class Runtime:
    def __init__(self):
        self.variables = {}

    def run(self, ast):
        for statement in ast:
            self.execute(statement)

    def execute(self, statement):
        if statement[0] == 'PRINT':
            self.print_value(statement[1])
        elif statement[0] == 'ASSIGN':
            self.assign_value(statement[1], statement[2])
        elif statement[0] == 'IF':
            self.evaluate_if(statement[1], statement[2], statement[3])

    def print_value(self, value):
        print(value)

    def assign_value(self, identifier, value):
        self.variables[identifier] = value

    def evaluate_if(self, identifier, value, true_statements):
        if self.variables.get(identifier) == value:
            for stmt in true_statements:
                if stmt is not None:  
                    self.execute(stmt)
