# parser.py

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0

    def parse(self):
        statements = []
        while self.position < len(self.tokens):
            statement = self.parse_statement()
            if statement:
                statements.append(statement)
        return statements

def parse_statement(self):
    token_type, token_value = self.tokens[self.position]
    if token_type == 'IDENTIFIER' and token_value == 'print':
        return self.parse_print_statement()
    elif token_type == 'IDENTIFIER':
        if self.tokens[self.position + 1][0] == 'EQUAL':
            return self.parse_assignment()
        elif self.tokens[self.position][1] == 'if':
            return self.parse_if_statement()
    else:
        self.position += 1  
        return None


    def parse_print_statement(self):
        self.position += 1  
        self.expect('LPAREN')
        self.expect('STRING')  
        string_value = self.tokens[self.position - 1][1]
        self.expect('RPAREN')
        self.expect('SEMICOLON')
        return ('PRINT', string_value)

    def parse_assignment(self):
        identifier = self.tokens[self.position][1]
        self.expect('IDENTIFIER')
        self.expect('EQUAL')
        self.expect('NUMBER')  
        number_value = self.tokens[self.position - 1][1]
        self.expect('SEMICOLON')
        return ('ASSIGN', identifier, number_value)

    def parse_if_statement(self):
        self.expect('IDENTIFIER')  
        self.expect('LPAREN')
        identifier = self.tokens[self.position][1]
        self.expect('IDENTIFIER')  
        self.expect('EQUAL')
        self.expect('EQUAL')
        self.expect('NUMBER')  
        number_value = self.tokens[self.position - 1][1]
        self.expect('RPAREN')
        self.expect('LBRACE')
        true_statements = []
        while self.tokens[self.position][0] != 'RBRACE':
            true_statements.append(self.parse_statement())
        self.expect('RBRACE')
        return ('IF', identifier, number_value, true_statements)

    def expect(self, token_type):
        if self.position < len(self.tokens) and self.tokens[self.position][0] == token_type:
            self.position += 1
        else:
            raise SyntaxError(f'Expected token type {token_type}, but got {self.tokens[self.position][0]}')
