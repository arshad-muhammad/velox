# lexer.py
from dataclasses import dataclass
from enum import Enum, auto
from typing import List, Optional

class TokenType(Enum):
    NUMBER = auto()
    PLUS = auto()
    MINUS = auto()
    MULTIPLY = auto()
    DIVIDE = auto()
    ASSIGN = auto()
    IDENTIFIER = auto()
    PRINT = auto()
    LPAREN = auto()
    RPAREN = auto()
    EOF = auto()

@dataclass
class Token:
    type: TokenType
    value: Optional[str]
    line: int
    column: int

    def __str__(self):
        return f"Token({self.type}, '{self.value}', line={self.line}, col={self.column})"

class Lexer:
    def __init__(self, source: str):
        self.source = source
        self.position = 0
        self.line = 1
        self.column = 1
        self.current_char = self.source[0] if source else None

    def advance(self):
        """Move to next character in the source code."""
        self.position += 1
        if self.current_char == '\n':
            self.line += 1
            self.column = 1
        else:
            self.column += 1
            
        self.current_char = self.source[self.position] if self.position < len(self.source) else None

    def skip_whitespace(self):
        """Skip whitespace characters."""
        while self.current_char and self.current_char.isspace():
            self.advance()

    def read_number(self) -> Token:
        """Read a numeric token."""
        result = ''
        start_column = self.column
        
        while self.current_char and (self.current_char.isdigit() or self.current_char == '.'):
            result += self.current_char
            self.advance()
            
        return Token(TokenType.NUMBER, result, self.line, start_column)

    def read_identifier(self) -> Token:
        """Read an identifier or keyword token."""
        result = ''
        start_column = self.column
        
        while self.current_char and (self.current_char.isalnum() or self.current_char == '_'):
            result += self.current_char
            self.advance()
            
        if result == 'print':
            return Token(TokenType.PRINT, result, self.line, start_column)
        return Token(TokenType.IDENTIFIER, result, self.line, start_column)

    def tokenize(self) -> List[Token]:
        """Convert source code into a list of tokens."""
        tokens = []
        
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue
                
            if self.current_char.isdigit():
                tokens.append(self.read_number())
                continue
                
            if self.current_char.isalpha():
                tokens.append(self.read_identifier())
                continue
                
            # Single-character tokens
            current_char = self.current_char
            current_column = self.column
            
            if current_char == '+':
                tokens.append(Token(TokenType.PLUS, '+', self.line, current_column))
            elif current_char == '-':
                tokens.append(Token(TokenType.MINUS, '-', self.line, current_column))
            elif current_char == '*':
                tokens.append(Token(TokenType.MULTIPLY, '*', self.line, current_column))
            elif current_char == '/':
                tokens.append(Token(TokenType.DIVIDE, '/', self.line, current_column))
            elif current_char == '=':
                tokens.append(Token(TokenType.ASSIGN, '=', self.line, current_column))
            elif current_char == '(':
                tokens.append(Token(TokenType.LPAREN, '(', self.line, current_column))
            elif current_char == ')':
                tokens.append(Token(TokenType.RPAREN, ')', self.line, current_column))
            else:
                raise SyntaxError(f"Invalid character '{current_char}' at line {self.line}, column {current_column}")
                
            self.advance()
            
        tokens.append(Token(TokenType.EOF, None, self.line, self.column))
        return tokens

# parser.py
from dataclasses import dataclass
from typing import List, Union, Optional

@dataclass
class NumberNode:
    value: float

@dataclass
class VariableNode:
    name: str

@dataclass
class BinOpNode:
    left: Union['NumberNode', 'VariableNode', 'BinOpNode']
    operator: TokenType
    right: Union['NumberNode', 'VariableNode', 'BinOpNode']

@dataclass
class AssignmentNode:
    name: str
    value: Union['NumberNode', 'VariableNode', 'BinOpNode']

@dataclass
class PrintNode:
    expression: Union['NumberNode', 'VariableNode', 'BinOpNode']

class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.current = 0

    def advance(self) -> Token:
        self.current += 1
        return self.tokens[self.current - 1]

    def peek(self) -> Token:
        return self.tokens[self.current]

    def parse(self) -> List[Union[AssignmentNode, PrintNode]]:
        """Parse tokens into an AST."""
        statements = []
        
        while self.peek().type != TokenType.EOF:
            if self.peek().type == TokenType.PRINT:
                statements.append(self.parse_print_statement())
            elif self.peek().type == TokenType.IDENTIFIER:
                statements.append(self.parse_assignment())
            else:
                raise SyntaxError(f"Unexpected token {self.peek()}")
                
        return statements

    def parse_print_statement(self) -> PrintNode:
        """Parse a print statement."""
        self.advance()  # consume 'print'
        expr = self.parse_expression()
        return PrintNode(expr)

    def parse_assignment(self) -> AssignmentNode:
        """Parse a variable assignment."""
        name = self.advance().value
        
        if self.peek().type != TokenType.ASSIGN:
            raise SyntaxError(f"Expected '=', got {self.peek()}")
            
        self.advance()  # consume '='
        value = self.parse_expression()
        return AssignmentNode(name, value)

    def parse_expression(self) -> Union[NumberNode, VariableNode, BinOpNode]:
        """Parse an arithmetic expression."""
        left = self.parse_term()
        
        while self.peek().type in (TokenType.PLUS, TokenType.MINUS):
            operator = self.advance().type
            right = self.parse_term()
            left = BinOpNode(left, operator, right)
            
        return left

    def parse_term(self) -> Union[NumberNode, VariableNode, BinOpNode]:
        """Parse a term (product/quotient)."""
        left = self.parse_factor()
        
        while self.peek().type in (TokenType.MULTIPLY, TokenType.DIVIDE):
            operator = self.advance().type
            right = self.parse_factor()
            left = BinOpNode(left, operator, right)
            
        return left

    def parse_factor(self) -> Union[NumberNode, VariableNode]:
        """Parse a factor (number/variable)."""
        token = self.advance()
        
        if token.type == TokenType.NUMBER:
            return NumberNode(float(token.value))
        elif token.type == TokenType.IDENTIFIER:
            return VariableNode(token.value)
        else:
            raise SyntaxError(f"Unexpected token {token}")

# runtime.py
class Runtime:
    def __init__(self):
        self.variables = {}

    def evaluate(self, node: Union[NumberNode, VariableNode, BinOpNode]) -> float:
        """Evaluate an expression node."""
        if isinstance(node, NumberNode):
            return node.value
            
        if isinstance(node, VariableNode):
            if node.name not in self.variables:
                raise RuntimeError(f"Variable '{node.name}' is not defined")
            return self.variables[node.name]
            
        if isinstance(node, BinOpNode):
            left = self.evaluate(node.left)
            right = self.evaluate(node.right)
            
            if node.operator == TokenType.PLUS:
                return left + right
            elif node.operator == TokenType.MINUS:
                return left - right
            elif node.operator == TokenType.MULTIPLY:
                return left * right
            elif node.operator == TokenType.DIVIDE:
                if right == 0:
                    raise RuntimeError("Division by zero")
                return left / right
                
        raise RuntimeError(f"Invalid node type: {type(node)}")

    def run(self, statements: List[Union[AssignmentNode, PrintNode]]):
        """Execute the program."""
        for statement in statements:
            if isinstance(statement, AssignmentNode):
                value = self.evaluate(statement.value)
                self.variables[statement.name] = value
            elif isinstance(statement, PrintNode):
                value = self.evaluate(statement.expression)
                print(value)
            else:
                raise RuntimeError(f"Invalid statement type: {type(statement)}")
