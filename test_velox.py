import unittest
from lexer import Lexer
from parser import Parser
from runtime import Runtime

def run_velox(code):
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()
    runtime = Runtime()
    
    output = []
    def mock_print(value):
        output.append(value)

    runtime.print_value = mock_print  # Override the print method
    runtime.run(ast)
    return output

class TestVelox(unittest.TestCase):
    def test_from_file(self):
        with open('example.vlx', 'r') as file:
            code = file.read()
        result = run_velox(code)
        self.assertEqual(result, ['Hello, Velox!', 'x is five'])

if __name__ == '__main__':
    unittest.main()
