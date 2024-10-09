from lexer import Lexer
from parser import Parser
from runtime import Runtime

def main():
    with open('example.vlx', 'r') as file:
        code = file.read()
    # Tokenization, parsing, and running code remains the same


    # Tokenizing the input code
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    print("Tokens:")
    for token in tokens:
        print(token)

    # Parsing the tokens into an AST
    parser = Parser(tokens)
    ast = parser.parse()
    print("\nAbstract Syntax Tree:")
    for statement in ast:
        print(statement)

    # Running the AST
    runtime = Runtime()
    runtime.run(ast)

if __name__ == "__main__":
    main()
