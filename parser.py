class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0

    def parse(self):
        statements = []
        while self.position < len(self.tokens):
            try:
                statement = self.parse_statement()
                if statement:
                    statements.append(statement)
            except SyntaxError as e:
                print(f"Syntax error at token {self.peek()}: {e}")
                self.advance()  # Skip the problematic token
        return statements

    def parse_statement(self):
        current_token = self.peek()
        if current_token[0] == 'IDENTIFIER':
            return self.handle_identifier(current_token)
        elif current_token[0] == 'NEWLINE':
            self.advance()
            return None
        else:
            raise SyntaxError(f"Unexpected token: {current_token}")

    def handle_identifier(self, current_token):
        if current_token[1] == 'print':
            return self.parse_print_statement()
        elif current_token[1] == 'if':
            return self.parse_if_statement()
        elif current_token[1] == 'while':
            return self.parse_while_statement()
        else:
            return self.parse_assignment()

    def parse_print_statement(self):
        self.expect('IDENTIFIER', 'print')
        self.expect('LPAREN')
        expression = self.parse_expression()
        self.expect('RPAREN')
        self.expect_optional('SEMICOLON')
        return ('print', expression)

    def parse_expression(self):
        left = self.parse_term()
        while self.peek()[0] in ('PLUS', 'MINUS'):
            operator = self.advance()[1]
            right = self.parse_term()
            left = (operator, left, right)  # Create a binary operation
        return left

    def parse_term(self):
        token = self.peek()
        if token[0] == 'IDENTIFIER':
            self.advance()
            return ('var', token[1])  # Variable
        elif token[0] == 'NUMBER':
            self.advance()
            return ('num', token[1])  # Literal
        else:
            raise SyntaxError(f"Unexpected token in expression: {token}")

    def parse_assignment(self):
        identifier = self.expect('IDENTIFIER')[1]
        self.expect('EQUAL')
        value = self.parse_expression()
        self.expect_optional('SEMICOLON')
        return ('assign', identifier, value)

    def parse_if_statement(self):
        self.expect('IDENTIFIER', 'if')
        self.expect('LPAREN')
        condition = self.parse_condition()
        self.expect('RPAREN')
        self.expect('LBRACE')
        body = self.parse_block()
        return ('if', condition, body)

    def parse_condition(self):
        left = self.expect('IDENTIFIER')[1]
        operator = self.expect('IDENTIFIER')[1]  # Expecting a comparison operator (like <, >, ==)
        right = self.expect('NUMBER')[1]
        return (operator, left, right)  # Return condition tuple

    def parse_while_statement(self):
        self.expect('IDENTIFIER', 'while')
        self.expect('LPAREN')
        condition = self.parse_condition()  # Parse the condition (e.g., x < 5)
        self.expect('RPAREN')
        self.expect('LBRACE')
        body = self.parse_block()
        return ('while', condition, body)

    def parse_block(self):
        body = []
        while self.peek()[0] != 'RBRACE':
            statement = self.parse_statement()
            if statement:
                body.append(statement)
        self.expect('RBRACE')
        return body

    def peek(self):
        if self.position < len(self.tokens):
            return self.tokens[self.position]
        return ('EOF', None)

    def expect(self, token_type, value=None):
        if self.position >= len(self.tokens):
            raise SyntaxError(f'Expected token type {token_type}, but reached end of file')
        token = self.tokens[self.position]
        if token[0] != token_type or (value and token[1] != value):
            raise SyntaxError(f'Expected token {token_type} {value}, but got {token}')
        self.position += 1
        return token

    def expect_optional(self, token_type):
        if self.position < len(self.tokens) and self.tokens[self.position][0] == token_type:
            self.position += 1

    def advance(self):
        self.position += 1
