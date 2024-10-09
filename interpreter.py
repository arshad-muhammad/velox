# interpreter.py
from lexer import Lexer
from parser import Parser

class Interpreter:
    def __init__(self):
        self.environment = {}  # Stores variables

    def interpret(self, ast):
        for statement in ast:
            self.execute(statement)

    # interpreter.py

class Interpreter:
    def interpret(self, ast):
        for node in ast:
            self.execute(node)

    def execute(self, node):
        if node[0] == 'PRINT':
            print(node[1].strip('"'))  # Print the string without quotes
        elif node[0] == 'ASSIGN':
            # Handle assignment logic here
            pass
        elif node[0] == 'IF':
            # Handle if condition logic here
            pass
        elif node[0] == 'FUNCTION':
            # Handle function declaration logic here
            pass
        # Add more cases as needed for your AST nodes

        # Add more cases as needed

    def execute_print(self, statement):
        value = self.evaluate_expression(statement[1])
        print(value)

    def execute_var_decl(self, statement):
        name = statement[1]
        value = self.evaluate_expression(statement[2])
        self.environment[name] = value

    def execute_if(self, statement):
        condition = self.evaluate_expression(statement[1])
        if condition:
            self.execute_block(statement[2])

    def evaluate_expression(self, expr):
        if expr[0] == 'NUMBER':
            return float(expr[1])
        elif expr[0] == 'STRING':
            return expr[1][1:-1]  # Strip quotes
        elif expr[0] == 'IDENTIFIER':
            return self.environment.get(expr[1], None)
        elif expr[0] == 'OP':
            left = self.evaluate_expression(expr[1])
            op = expr[2]
            right = self.evaluate_expression(expr[3])
            return self.apply_operator(left, op, right)

    def apply_operator(self, left, op, right):
        if op == '+':
            return left + right
        elif op == '-':
            return left - right
        elif op == '*':
            return left * right
        elif op == '/':
            return left / right
        else:
            raise RuntimeError(f'Unknown operator: {op}')

    def execute_block(self, block):
        for statement in block:
            self.execute(statement)

# Sample usage
if __name__ == '__main__':
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
