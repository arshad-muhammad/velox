# shell.py

import lexer
import parser
import runtime

def repl():
    run_time = runtime.Runtime()
    
    while True:
        text = input('velox > ')
        if text.strip() == "": continue

        lex = lexer.Lexer(text)
        tokens = lex.tokenize()

        pars = parser.Parser(tokens)
        ast = pars.parse()

        run_time.run(ast)

if __name__ == "__main__":
    repl()
