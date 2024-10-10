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
                print(f"Syntax error: {e}")
                self.advance()  # Skip the problematic token
        return statements

    def parse_statement(self):
        current_token = self.peek()
        if current_token[0] == 'IDENTIFIER':
            if current_token[1] == 'print':
                return self.parse_print_statement()
            elif current_token[1] == 'if':
                return self.parse_if_statement()
            else:
                return self.parse_assignment()
        elif current_token[0] == 'NEWLINE':
            self.advance()
            return None
        else:
            raise SyntaxError(f"Unexpected token: {current_token}")

    def parse_print_statement(self):
        self.expect('IDENTIFIER', 'print')
        self.expect('LPAREN')
        expression = self.parse_expression()
        self.expect('RPAREN')
        self.expect_optional('SEMICOLON')
        return ('print', expression)

    def parse_expression(self):
        token = self.peek()
        self.advance()
        return token[1]  # Return the token value as a simple expression

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
        body = []
        while self.peek()[0] != 'RBRACE':
            statement = self.parse_statement()
            if statement:
                body.append(statement)
        self.expect('RBRACE')
        return ('if', condition, body)

    def parse_condition(self):
        left = self.expect('IDENTIFIER')[1]
        self.expect('EQUAL')
        self.expect('EQUAL')
        right = self.expect('NUMBER')[1]
        return ('==', left, right)

    def peek(self):
        if self.position < len(self.tokens):
            return self.tokens[self.position]
        return ('EOF', None)

    def expect(self, token_type, value=None):
        if self.position >= len(self.tokens):
            raise SyntaxError(f'Expected token type {token_type}, but reached end of file')
        token = self.tokens[self.position]
        if token[0] != token_type or (value and token[1] != value):
            raise SyntaxError(f'Expected token type {token_type}{f" with value {value}" if value else ""}, but got {token}')
        self.advance()
        return token

    def expect_optional(self, token_type):
        if self.peek()[0] == token_type:
            self.advance()

    def advance(self):
        self.position += 1