class Runtime:
    """A simple interpreter runtime for executing AST nodes."""
    
    def __init__(self):
        """Initialize the runtime environment."""
        self.variables = {}
        self.print_value = print  # Default to built-in print function
        self.debug_mode = False
        
    def run(self, ast):
        """Execute a list of statements from the AST."""
        self._debug("Running AST")
        for statement in ast:
            self._debug(f"Executing statement: {statement}")
            self.execute(statement)
            
    def execute(self, statement):
        """Execute a single statement based on its type."""
        statement_type = statement[0]
        
        statement_handlers = {
            'print': self._handle_print,
            'assign': self._handle_assign,
            'if': self._handle_if,
            'while': self._handle_while
        }
        
        if statement_type in statement_handlers:
            statement_handlers[statement_type](statement)
        else:
            raise ValueError(f"Unknown statement type: {statement_type}")
            
    def _handle_print(self, statement):
        """Handle print statements."""
        value = self.evaluate_expression(statement[1])
        self._debug(f"Printing value: {value}")
        self.print_value(value)
        
    def _handle_assign(self, statement):
        """Handle assignment statements."""
        identifier, expression = statement[1], statement[2]
        self._debug(f"Assigning {identifier} = {expression}")
        self.assign_value(identifier, self.evaluate_expression(expression))
        
    def _handle_if(self, statement):
        """Handle if statements."""
        condition, true_statements = statement[1], statement[2]
        self._debug(f"Evaluating if condition: {condition}")
        self.evaluate_if(condition, true_statements)
        
    def _handle_while(self, statement):
        """Handle while statements."""
        condition, body = statement[1], statement[2]
        self.evaluate_while(condition, body)
        
    def assign_value(self, identifier, value):
        """Assign a value to a variable."""
        self._debug(f"Assigning {identifier} = {value}")
        self.variables[identifier] = value
        
    def evaluate_while(self, condition, body):
        """Evaluate a while loop."""
        while self.evaluate_condition(condition):
            for stmt in body:
                self.execute(stmt)
                
    def evaluate_if(self, condition, true_statements):
        """Evaluate an if statement."""
        result = self.evaluate_condition(condition)
        self._debug(f"If condition result: {result}")
        
        if result:
            for stmt in true_statements:
                if stmt is not None:
                    self._debug(f"Executing if body statement: {stmt}")
                    self.execute(stmt)
                    
    def evaluate_condition(self, condition):
        """Evaluate a comparison condition."""
        op, left, right = condition
        left_value = self.evaluate_expression(left)
        right_value = self.evaluate_expression(right)
        
        self._debug(f"Comparing {left_value} {op} {right_value}")
        
        operators = {
            '==': lambda x, y: x == y,
            '<': lambda x, y: x < y,
            '>': lambda x, y: x > y,
            '<=': lambda x, y: x <= y,
            '>=': lambda x, y: x >= y,
            '!=': lambda x, y: x != y
        }
        
        if op in operators:
            return operators[op](left_value, right_value)
        raise ValueError(f"Unknown operator: {op}")
        
    def evaluate_expression(self, expr):
        """Evaluate an expression and return its value."""
        if isinstance(expr, str):
            if expr.startswith('"') and expr.endswith('"'):
                return expr[1:-1]  # Remove quotes for string literals
            return self.variables.get(expr, expr)
            
        if isinstance(expr, tuple):
            operator, left, right = expr
            left_value = self.evaluate_expression(left)
            right_value = self.evaluate_expression(right)
            
            operators = {
                '+': lambda x, y: str(x) + str(y) if isinstance(x, str) or isinstance(y, str) 
                                                else float(x) + float(y),
                '-': lambda x, y: float(x) - float(y),
                '*': lambda x, y: float(x) * float(y),
                '/': lambda x, y: float(x) / float(y),
                '%': lambda x, y: float(x) % float(y)
            }
            
            if operator in operators:
                return operators[op](left_value, right_value)
            raise ValueError(f"Unknown operator: {operator}")
            
        return expr
        
    def _debug(self, message):
        """Print debug messages if debug mode is enabled."""
        if self.debug_mode:
            print(f"DEBUG: {message}")
