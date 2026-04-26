# SYSTEM IMPORTS 

import sys  # Used to access command-line arguments (like file names) and exit program safely
import os   # Used to check if input file exists before compilation starts

# COMPILER PHASE IMPORTS

# Lexer: converts raw source code into tokens (small meaningful units)
from lexer import Lexer, LexerError

# Parser: converts tokens into AST (structured tree representation)
from parser import Parser, ParseError

# Semantic Analyzer: checks logical/meaning errors in AST
from semantic import SemanticAnalyser, SemanticError

# Code Generator: converts AST into final Python code
from codegen import CodeGenerator


# TERMINAL COLOR CODES 
# These are used to make compiler output more readable and professional

GREEN  = '\033[92m'   # success messages (green text)
RED    = '\033[91m'   # error messages (red text)
YELLOW = '\033[93m'   # warnings / info messages (yellow text)
CYAN   = '\033[96m'   # section headings (cyan text)
BOLD   = '\033[1m'    # bold text formatting
RESET  = '\033[0m'    # resets terminal formatting back to normal


# FUNCTION: header()
# PURPOSE: Prints a clean section header for each compiler phase

def header(title: str):
    width = 60  # width of decorative line for UI formatting

    # Top border line
    print(f'\n{BOLD}{CYAN}{"═"*width}{RESET}')

    # Center-like title display for phase name
    print(f'{BOLD}{CYAN}  {title}{RESET}')

    # Bottom border line
    print(f'{BOLD}{CYAN}{"═"*width}{RESET}')


# Function to print success messages (green)
def success(msg: str):
    print(f'{GREEN}success  {msg}{RESET}')


# Function to print error messages (red)
def error(msg: str):
    print(f'{RED}fail  {msg}{RESET}')


# Function to print informational messages (yellow text)
def info(msg: str):
    print(f'{YELLOW}   {msg}{RESET}')

# MAIN COMPILER PIPELINE FUNCTION

def compile_rulescript(source_path: str, output_path: str = 'output.py'):
    """
    This is the core compiler pipeline.

    It takes a source file and processes it step by step:

    1. Reads source code from file
    2. Converts code → tokens (Lexer)
    3. Converts tokens → AST (Parser)
    4. Checks meaning errors (Semantic Analyzer)
    5. Converts AST → Python code (Code Generator)
    6. Writes final output to file
    """

    # COMPILER START HEADER 
    header("RuleScript Compiler v1.0")

    # Display input and output file paths
    print(f'  Source : {source_path}')
    print(f'  Output : {output_path}')

    # FILE EXISTENCE CHECK 
    # Prevents crash if file does not exist
    if not os.path.exists(source_path):
        error(f"Source file not found: {source_path}")
        sys.exit(1)  # immediately stop compiler execution

    # READ SOURCE FILE 
    with open(source_path, 'r') as f:
        source = f.read()  # entire program loaded as a single string

    # Print source code with line numbers for debugging/visibility
    print(f'\n{BOLD}Source code:{RESET}')
    for i, line in enumerate(source.splitlines(), 1):
        print(f'  {i:3}│ {line}')


    
    # PHASE 1 — LEXICAL ANALYSIS
    # Goal: Convert raw code - tokens (small units like keywords, numbers, symbols)

    header("Phase 1 — Lexical Analysis (Tokenisation)")

    try:
        lexer = Lexer(source)        # create lexer object with source code
        tokens = lexer.tokenize()    # generate token list

        # Show success message with number of tokens
        success(f"Tokenised successfully. {len(tokens)} tokens produced.")

    except LexerError as e:
        # If invalid character found → stop compilation immediately
        error(f"Lexer error: {e}")
        sys.exit(1)

    # Display token table (for debugging and learning)
    print(f'\n  {"#":<4} {"Type":<14} {"Value":<20} {"Line"}')
    print(f'  {"─"*4} {"─"*14} {"─"*20} {"─"*4}')

    for i, tok in enumerate(tokens, 1):
        print(f'  {i:<4} {tok.type:<14} {tok.value!r:<20} {tok.line}')

    # PHASE 2 — SYNTAX ANALYSIS (PARSER)
    # Goal: Convert tokens → AST (structured tree representation)

    header("Phase 2 — Syntax Analysis (Parsing)")

    try:
        parser = Parser(tokens)   # create parser with tokens
        ast = parser.parse()      # build Abstract Syntax Tree

        success(f"Parsed successfully. {len(ast.rules)} rule(s) found.")

    except ParseError as e:
        # If grammar is incorrect- stop compiler
        error(f"Parse error: {e}")
        sys.exit(1)

    # PHASE 3 — AST VISUALIZATION
    # Goal: Show structured representation of program

    header("Phase 3 — Abstract Syntax Tree (AST)")

    for rule in ast.rules:

        # Print rule name and line number
        print(f'\n  {BOLD}RULE:{RESET} {rule.name}  (line {rule.line})')

        # Extract IF condition
        cond = rule.if_node.condition
        print(f'    IF   → {cond.left}  {cond.op}  {cond.right}')

        # Extract THEN block assignment
        tb = rule.if_node.then_body
        print(f'    THEN → {tb.variable} = {tb.value}')

        # Extract ELSE block if exists
        eb = rule.if_node.else_body
        if eb:
            print(f'    ELSE → {eb.variable} = {eb.value}')
        else:
            print('    ELSE → (none)')

    # PHASE 4 — SEMANTIC ANALYSIS
    # Goal: Check logical correctness of program

    header("Phase 4 — Semantic Analysis")

    try:
        analyser = SemanticAnalyser()  # create semantic checker object

        analyser.analyse(ast)          # run semantic validation

        success("Semantic checks passed.")

        # Show internal state of analyzer (for debugging/learning)
        info(f"Rules defined : {sorted(analyser.rule_names)}")
        info(f"Variables seen: {sorted(analyser.defined_vars)}")

    except SemanticError as e:
        # Stop if any logical error is found
        error(f"Semantic error: {e}")
        sys.exit(1)

    # PHASE 5 — CODE GENERATION
    # Goal: Convert AST - final executable Python code

    header("Phase 5 — Code Generation (Python output)")

    gen = CodeGenerator()         # create code generator
    python_src = gen.generate(ast)  # generate Python code string

    # Print generated Python code line by line
    print(f'\n{BOLD}Generated Python:{RESET}')
    for i, line in enumerate(python_src.splitlines(), 1):
        print(f'  {i:3}│ {line}')

    # Write generated code into output file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(python_src)

    # Final success message
    success(f"Output written to '{output_path}'")

    # Show compilation completion banner
    header("Compilation Complete ✔")



# This allows running compiler from terminal

if __name__ == '__main__':

    # If user provides file name - use it
    # Else default input file is "input.rules"
    source_file = sys.argv[1] if len(sys.argv) > 1 else 'input.rules'

    # Optional output file name (default: output.py)
    output_file = sys.argv[2] if len(sys.argv) > 2 else 'output.py'

    # Start full compilation process
    compile_rulescript(source_file, output_file)