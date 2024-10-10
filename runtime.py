class Runtime:
    def __init__(self):
        self.variables = {}
        self.print_value = print  # Default to built-in print function
        self.debug_mode = False  # Set this to True to enable debug logging

    def run(self, ast):
        if self.debug_mode:
            print("DEBUG: Running AST")
        for statement in ast:
            if self.debug_mode:
                print(f"DEBUG: Executing statement: {statement}")
            self.execute(statement)

    def execute(self, statement):
        if statement[0] == 'print':
            value = self.evaluate_expression(statement[1])
            if self.debug_mode:
                print(f"DEBUG: Printing value: {value}")
            self.print_value(value)
        elif statement[0] == 'assign':
            if self.debug_mode:
                print(f"DEBUG: Assigning {statement[1]} = {statement[2]}")
            self.assign_value(statement[1], self.evaluate_expression(statement[2]))
        elif statement[0] == 'if':
            if self.debug_mode:
                print(f"DEBUG: Evaluating if condition: {statement[1]}")
            self.evaluate_if(statement[1], statement[2])

    def assign_value(self, identifier, value):
        if self.debug_mode:
            print(f"DEBUG: Assigning {identifier} = {value}")
        self.variables[identifier] = value

    def evaluate_if(self, condition, true_statements):
        result = self.evaluate_condition(condition)
        if self.debug_mode:
            print(f"DEBUG: If condition result: {result}")
        if result:
            for stmt in true_statements:
                if stmt is not None:
                    if self.debug_mode:
                        print(f"DEBUG: Executing if body statement: {stmt}")
                    self.execute(stmt)

    def evaluate_condition(self, condition):
        op, left, right = condition
        if op == '==':
            left_value = self.evaluate_expression(left)
            right_value = self.evaluate_expression(right)
            if self.debug_mode:
                print(f"DEBUG: Comparing {left_value} == {right_value}")
            return left_value == right_value

    def evaluate_expression(self, expr):
        if isinstance(expr, str):
            if expr.startswith('"') and expr.endswith('"'):
                return expr[1:-1]
            return self.variables.get(expr, expr)
        return expr
