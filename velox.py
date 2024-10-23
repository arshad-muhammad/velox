from lexer import Lexer
from parser import Parser
from runtime import Runtime
import sys
from typing import List, Optional

def load_source_file(filename: str) -> Optional[str]:
    """
    Load source code from a file.
    
    Args:
        filename (str): Path to the source code file
        
    Returns:
        Optional[str]: The file contents if successful, None if file operation fails
    
    Raises:
        FileNotFoundError: If the source file cannot be found
    """
    try:
        with open(filename, 'r') as file:
            return file.read()
    except FileNotFoundError:
        print(f"Error: Could not find file '{filename}'")
        return None
    except Exception as e:
        print(f"Error reading file: {str(e)}")
        return None

def process_code(code: str, debug: bool = False) -> bool:
    """
    Process the source code through lexing, parsing, and runtime stages.
    
    Args:
        code (str): Source code to process
        debug (bool): Whether to print debug information
        
    Returns:
        bool: True if processing was successful, False otherwise
    """
    try:
        # Tokenization
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        if debug:
            print("\nTokens:")
            for token in tokens:
                print(f"  {token}")
        
        # Parsing
        parser = Parser(tokens)
        ast = parser.parse()
        if debug:
            print("\nAbstract Syntax Tree:")
            for statement in ast:
                print(f"  {statement}")
        
        # Runtime execution
        runtime = Runtime()
        runtime.run(ast)
        return True
        
    except Exception as e:
        print(f"Error during processing: {str(e)}")
        return False

def main() -> int:
    """
    Main entry point for the interpreter.
    
    Returns:
        int: Exit code (0 for success, 1 for failure)
    """
    # Check command line arguments
    if len(sys.argv) < 2:
        print("Usage: python interpreter.py <filename> [--debug]")
        return 1
    
    filename = sys.argv[1]
    debug_mode = "--debug" in sys.argv
    
    # Load and process the source code
    source_code = load_source_file(filename)
    if source_code is None:
        return 1
        
    success = process_code(source_code, debug=debug_mode)
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())
