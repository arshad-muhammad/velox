# interpreter.py
from typing import Any, Dict, List, Union
from dataclasses import dataclass

@dataclass
class Environment:
    """Stores the interpreter's variable environment."""
    variables: Dict[str, Any] = None
    
    def __post_init__(self):
        self.variables = self.variables or {}
    
    def define(self, name: str, value: Any) -> None:
        """Define a variable in the current environment."""
        self.variables[name] = value
    
    def get(self, name: str) -> Any:
        """Get a variable's value from the environment."""
        if name in self.variables:
            return self.variables[name]
        raise RuntimeError(f"Undefined variable '{name}'")
    
    def assign(self, name: str, value: Any) -> None:
        """Assign a value to an existing variable."""
        if name in self.variables:
            self.variables[name] = value
        else:
            raise RuntimeError(f"Undefined variable '{name}'")

class Interpreter:
    """Interprets the AST nodes and executes the program."""
    
    def __init__(self):
        self.environment = Environment()
    
    def interpret(self, ast: List) -> None:
        """Interpret a list of AST nodes."""
        try:
            for node in ast:
                self.execute(node)
        except Exception as e:
            raise RuntimeError(f"Runtime error: {str(e)}")
    
    def execute(self, node: tuple) -> None:
        """Execute a single AST node."""
        node_type = node[0]
        
        # Mapping of node types to their handler methods
        handlers = {
            'PRINT': self.execute_print,
            'VAR_DECL': self.execute_var_decl,
            'ASSIGN': self.execute_assign,
            'IF': self.execute_if,
            'WHILE': self.execute_while,
            'FUNCTION': self.execute_function,
            'RETURN': self.execute_return,
            'BLOCK': self.execute_block
        }
        
        if node_type in handlers:
            handlers[node_type](node)
        else:
            raise RuntimeError(f"Unknown node type: {node_type}")
    
    def execute_print(self, node: tuple) -> None:
        """Execute a print statement."""
        value = self.evaluate_expression(node[1])
        print(str(value))
    
    def execute_var_decl(self, node: tuple) -> None:
        """Execute a variable declaration."""
        name = node[1]
        value = self.evaluate_expression(node[2])
        self.environment.define(name, value)
    
    def execute_assign(self, node: tuple) -> None:
        """Execute a variable assignment."""
        name = node[1]
        value = self.evaluate_expression(node[2])
        self.environment.assign(name, value)
    
    def execute_if(self, node: tuple) -> None:
        """Execute an if statement."""
        condition = self.evaluate_expression(node[1])
        
        if self.is_truthy(condition):
            self.execute_block(node[2])
        elif len(node) > 3:  # Has else block
            self.execute_block(node[3])
    
    def execute_while(self, node: tuple) -> None:
        """Execute a while loop."""
        while self.is_truthy(self.evaluate_expression(node[1])):
            self.execute_block(node[2])
    
    def execute_function(self, node: tuple) -> None:
        """Execute a function declaration."""
        name = node[1]
        params = node[2]
        body = node[3]
        self.environment.define(name, {'params': params, 'body': body})
    
    def execute_return(self, node: tuple) -> Any:
        """Execute a return statement."""
        if len(node) > 1:
            return self.evaluate_expression(node[1])
        return None
    
    def execute_block(self, statements: List) -> None:
        """Execute a block of statements."""
        for statement in statements:
            self.execute(statement)
    
    def evaluate_expression(self, expr: Union[tuple, str, float]) -> Any:
        """Evaluate an expression and return its value."""
        if isinstance(expr, (str, float, int)):
            return expr
        
        expr_type = expr[0]
        
        evaluators = {
            'NUMBER': lambda: float(expr[1]),
            'STRING': lambda: expr[1][1:-1],  # Strip quotes
            'IDENTIFIER': lambda: self.environment.get(expr[1]),
            'BINARY': lambda: self.evaluate_binary(expr[1], expr[2], expr[3]),
            'UNARY': lambda: self.evaluate_unary(expr[1], expr[2]),
            'CALL': lambda: self.evaluate_call(expr[1], expr[2])
        }
        
        if expr_type in evaluators:
            return evaluators[expr_type]()
        
        raise RuntimeError(f"Unknown expression type: {expr_type}")
    
    def evaluate_binary(self, left: Any, operator: str, right: Any) -> Any:
        """Evaluate a binary expression."""
        left_val = self.evaluate_expression(left)
        right_val = self.evaluate_expression(right)
        
        operators = {
            '+': lambda: left_val + right_val,
            '-': lambda: left_val - right_val,
            '*': lambda: left_val * right_val,
            '/': lambda: left_val / right_val,
            '%': lambda: left_val % right_val,
            '==': lambda: left_val == right_val,
            '!=': lambda: left_val != right_val,
            '<': lambda: left_val < right_val,
            '<=': lambda: left_val <= right_val,
            '>': lambda: left_val > right_val,
            '>=': lambda: left_val >= right_val
        }
        
        if operator in operators:
            return operators[operator]()
        
        raise RuntimeError(f"Unknown operator: {operator}")
    
    def evaluate_unary(self, operator: str, operand: Any) -> Any:
        """Evaluate a unary expression."""
        value = self.evaluate_expression(operand)
        
        if operator == '-':
            return -float(value)
        elif operator == '!':
            return not self.is_truthy(value)
        
        raise RuntimeError(f"Unknown unary operator: {operator}")
    
    def evaluate_call(self, callee: str, arguments: List) -> Any:
        """Evaluate a function call."""
        function = self.environment.get(callee)
        if not isinstance(function, dict) or 'params' not in function:
            raise RuntimeError(f"Can only call functions. Got: {callee}")
        
        # Create new environment for function scope
        previous_env = self.environment
        self.environment = Environment()
        
        try:
            # Bind arguments to parameters
            for param, arg in zip(function['params'], arguments):
                self.environment.define(param, self.evaluate_expression(arg))
            
            # Execute function body
            for statement in function['body']:
                if statement[0] == 'RETURN':
                    return self.execute_return(statement)
                self.execute(statement)
            
            return None
        finally:
            self.environment = previous_env
    
    @staticmethod
    def is_truthy(value: Any) -> bool:
        """Determine if a value is truthy."""
        if isinstance(value, bool):
            return value
        if value is None:
            return False
        if isinstance(value, (int, float)):
            return value != 0
        if isinstance(value, str):
            return len(value) > 0
        return True

if __name__ == '__main__':
    # Sample usage
    code = '''
    print("Hello, Velox!");
    var x = 5;
    if (x == 5) {
        print("x is five");
    }
    '''
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()
    interpreter = Interpreter()
    interpreter.interpret(ast)
