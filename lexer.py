# lexer.py

import re

TOKEN_TYPES = [
    ("LESS", r'<'),
    ("GREATER", r'>'),
    ("LESSEQUAL", r'<='),
    ("GREATEREQUAL", r'>='),
    ("NUMBER", r'\d+(\.\d+)?'),  
    ("STRING", r'"(.*?)"'),      
    ("IDENTIFIER", r'[a-zA-Z_]\w*'),  
    ("PLUS", r'\+'),             
    ("MINUS", r'-'),             
    ("TIMES", r'\*'),            
    ("DIVIDE", r'/'),            
    ("EQUAL", r'='),             
    ("LPAREN", r'\('),           
    ("RPAREN", r'\)'),           
    ("LBRACE", r'{'),            
    ("RBRACE", r'}'),            
    ("SEMICOLON", r';'),         
    ("NEWLINE", r'\n'),          
    ("WHITESPACE", r'\s+'),      
]

TOKEN_REGEX = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in TOKEN_TYPES)
token_re = re.compile(TOKEN_REGEX)

class Lexer:
    def __init__(self, source):
        self.source = source
        self.position = 0

    def tokenize(self):
        tokens = []
        while self.position < len(self.source):
            match = token_re.match(self.source, self.position)
            if not match:
                raise SyntaxError(f'Illegal character: {self.source[self.position]}')

            type_ = match.lastgroup
            value = match.group(type_)
            if type_ == 'WHITESPACE':
                pass  
            elif type_ == 'NEWLINE':
                tokens.append(('NEWLINE', None))  
            else:
                tokens.append((type_, value))

            self.position = match.end()
        return tokens
