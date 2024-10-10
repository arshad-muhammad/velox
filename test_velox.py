import unittest
from lexer import Lexer
from parser import Parser
from runtime import Runtime

def run_velox(code):
    print("Code:")
    print(code)
    
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    print("Tokens:")
    print(tokens)
    
    parser = Parser(tokens)
    ast = parser.parse()
    print("AST:")
    print(ast)
    
    runtime = Runtime()
    
    output = []
    runtime.print_value = output.append  # Override the print method
    runtime.run(ast)
    return output

class TestVelox(unittest.TestCase):
    def test_from_file(self):
        with open('example.vlx', 'r') as file:
            code = file.read()
        result = run_velox(code)
        print("Result:")
        print(result)
        self.assertEqual(result, ['Hello, Velox!', 'success', 'second succedd', 'third succedd'])

if __name__ == '__main__':
    unittest.main()
