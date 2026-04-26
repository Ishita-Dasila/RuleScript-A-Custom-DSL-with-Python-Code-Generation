# RuleScript: A Custom DSL with Python Code Generation

## Project Overview

RuleScript is a domain-specific programming language (DSL) built from scratch that allows users to write simple rule-based instructions which are automatically converted into executable Python programs. The system implements a complete compiler pipeline consisting of five sequential stages that work together to process and transform source code written in the RuleScript language.

The project also integrates an AI-powered assistant using a Groq API-based backend built with Node.js and Express. This assistant helps users debug compiler errors and understand compiler concepts through multi-turn conversational interaction.

---
---

## Repository

https://github.com/Ishita-Dasila/RuleScript-A-Custom-DSL-with-Python-Code-Generation

---

## Features

- Custom DSL with keywords: RULE, IF, THEN, ELSE, TRUE, FALSE
- Five-stage compiler pipeline: Lexer, Parser, AST Builder, Semantic Analyzer, Code Generator
- Strict hard-error handling: compilation stops immediately at any detected error
- Generated Python code runs as a fully standalone program
- HTML dashboard to view tokens, AST, logs, and compiler output
- AI assistant for error explanation and compiler concept learning
- Multi-turn conversational debugging support via Groq API

---

## Compiler Pipeline

### Stage 1 - Lexical Analysis (lexer.py)

The Lexer reads raw RuleScript source code and breaks it into meaningful tokens such as keywords, identifiers, operators, numbers, and boolean values. It uses ordered regex patterns to prevent keyword misclassification. Whitespace and comments are ignored. If any invalid or unrecognized character is found, a LexerError is raised immediately and compilation stops.

### Stage 2 - Syntax Analysis (parser.py)

The Parser takes the token stream and validates it against the RuleScript grammar using recursive descent parsing. Each grammar rule is handled by a dedicated function, making the code modular and easy to maintain. If any structural error is found such as a missing keyword, wrong ordering, or unexpected token, a ParseError is raised and compilation stops immediately.

### Stage 3 - AST Construction (ast_nodes.py)

After successful parsing, an Abstract Syntax Tree (AST) is built to represent the logical structure of the program in a hierarchical form. The tree is composed of five node types: ProgramNode, RuleNode, IfNode, ConditionNode, and AssignNode. Since this stage operates on already-validated syntax, it completes reliably when the previous stages pass.

### Stage 4 - Semantic Analysis (semantic.py)

The Semantic Analyzer traverses the AST and checks for logical errors that cannot be caught at the syntax level. This includes detection of duplicate rule names and references to undefined variables. Input variables are pre-registered to avoid false positives. A SemanticError is raised for any critical issue found, stopping the compilation.

### Stage 5 - Code Generation (codegen.py)

The Code Generator converts the validated AST into clean, executable Python code. Each RULE defined in RuleScript becomes a separate Python function in the output file. IF conditions are translated into Python if/else logic, and THEN assignments define the outputs. The final generated file runs independently without any external dependencies.

---

## AI Assistant

The AI assistant is built using a Node.js and Express backend integrated with the Groq API. It is aware of the full RuleScript compiler pipeline, all five stages, error formats, and project architecture.

Key capabilities:
- Identifies which compiler stage an error belongs to (lexical, syntax, or semantic)
- Explains the root cause of errors in simple, human-readable language
- Guides users step-by-step on how to fix their code
- Answers general compiler design questions
- Supports multi-turn conversations for continuous debugging and learning

---

## Project Structure

```
RuleScript/
|
|-- lexer.py                   # Tokenizer using regex patterns
|-- parser.py                  # Recursive descent parser
|-- ast_nodes.py               # AST node class definitions
|-- semantic.py                # Semantic validation checks
|-- codegen.py                 # Python code generator from AST
|-- main.py                    # Main pipeline driver with colored terminal output
|-- server.js                  # Node.js + Express backend with Groq API integration
|
|-- input.rules                # Main input file for RuleScript source code
|-- output.py                  # Final generated Python file
|-- error_examples.rules       # Intentional error test cases for all stages
|
|-- rulescript_dashboard.html  # Main compiler dashboard (tokens, AST, output, AI)
|-- index.html                 # Entry point / landing page
|-- login.html                 # Login page
|-- about.html                 # About page describing the project
|-- auth.js                    # Frontend login and session management
|-- navbar.js                  # Navigation bar controller
|-- style.css                  # Styling for all pages
|
|-- README.md                  # Project documentation
```

---

## RuleScript Language Syntax

A RuleScript program consists of one or more rules. Each rule follows this structure:

```
RULE rule_name
IF variable operator value
THEN output_variable = result
ELSE output_variable = result
```

### Keywords

| Keyword | Description |

| RULE | Declares a new rule block |
| IF | Begins the condition |
| THEN | Action to take if condition is true |
| ELSE | Action to take if condition is false |
| TRUE | Boolean true value |
| FALSE | Boolean false value |

### Supported Operators

=, >=, <=, >, <, !=

### Example Input (input.rules)

```
RULE check_age
IF age >= 18
THEN eligible = True
ELSE eligible = False

RULE check_score
IF score >= 50
THEN result = True
ELSE result = False
```

### Generated Python Output (output.py)

```python
def check_age(age):
    if age >= 18:
        eligible = True
    else:
        eligible = False
    return eligible

def check_score(score):
    if score >= 50:
        result = True
    else:
        result = False
    return result
```

---

## Error Handling

The compiler uses a strict hard-error system. Compilation stops immediately upon detecting any error in any phase. No invalid or partially valid program proceeds further in the pipeline.

### Error Types

| Stage | Error Type | Example Trigger |

| Lexical Analysis | LexerError | Invalid character such as @ in source |
| Syntax Analysis | ParseError | Missing THEN keyword, wrong token order |
| Semantic Analysis | SemanticError | Duplicate rule name, undefined variable |

---

## Testing and Validation

| Test Case | Status | Notes |

| Normal compilation with 5 rules | PASS | All 5 phases complete, output.py generated correctly |
| Phase 1 Error: invalid character @ | PASS | LexerError raised at correct line |
| Phase 2 Error: missing THEN keyword | PASS | ParseError raised at correct line |
| Phase 2 Error: == instead of = in THEN | PASS | ParseError: Expected OPERATOR(=) but got OPERATOR(==) |
| Phase 2 Error: missing rule name after RULE | PASS | ParseError: Expected IDENTIFIER but got NEWLINE |
| Phase 4 Error: duplicate rule name | PASS | SemanticError raised, compilation stopped |
| Phase 4 Error: undefined variable | PASS | SemanticError raised, compilation stopped |
| Generated output.py runs as Python | PASS | Functions execute correctly |
| Dashboard loads in browser | PASS | All sections render correctly |
| AI Agent: basic compiler query | PASS | Correct phase explanation returned |
| AI Agent: error explanation | PASS | Correctly identifies stage, explains cause, suggests fix |
| Backend API (/ask route) | PASS | Returns valid responses from Groq API |
| End-to-end system test | PASS | Full system works without crashes |

---

## How to Run

### Prerequisites

- Python 3.x
- Node.js and npm
- Groq API key

### Running the Compiler

1. Write your RuleScript code in `input.rules`
2. Run the compiler pipeline:

```bash
python main.py
```

3. The compiled Python code will be saved to `output.py`
4. Terminal output will show color-coded stage-by-stage results

### Running the AI Assistant Backend

1. Install dependencies:

```bash
npm install
```

2. Add your Groq API key to the environment or server configuration
3. Start the server:

```bash
node server.js
```

### Opening the Dashboard

Open `rulescript_dashboard.html` in a browser to view the interactive interface showing tokens, AST structure, compiler output, logs, and the AI assistant chat.

---

## Key Design Decisions

- Keywords are matched before general identifiers in the lexer to prevent misclassification of reserved words such as RULE, IF, THEN, ELSE, TRUE, and FALSE as variable names.
- All file operations use explicit UTF-8 encoding to ensure compatibility across operating systems including Windows.
- Each compiler stage is implemented in a separate Python file for modularity, readability, and easy debugging.
- The hard-error system ensures that no invalid program state propagates through the pipeline.

---

## Challenges Faced and Solutions

**Error propagation strategy:** Decided to use a strict hard-error approach where any critical error in any phase stops compilation immediately. This prevents incorrect programs from producing misleading output in later stages.

**Windows encoding issue:** Writing certain characters to the output Python file caused crashes on Windows systems due to encoding mismatches. Fixed by explicitly setting UTF-8 encoding in all file-handling operations inside main.py.

**Lexer pattern ordering:** Initially, general identifier patterns were placed before keyword patterns, causing reserved words to be misclassified as variable names. Fixed by reordering patterns so keywords are matched first.

**Naming conflict in main.py:** A variable name accidentally overlapped with a helper function name, causing runtime errors. Fixed by renaming the function to a more distinct identifier.

---

## Future Scope

- Support for nested conditions and multiple IF branches
- Type system with type inference
- Loop constructs within rules
- Import/export of rule modules
- Extended operator support including string comparisons
- Direct browser-based compiler execution
- Expanded AI assistant capabilities with code suggestion and auto-correction

---

## License

This project was developed as part of the Compiler Design course at Graphic Era (Deemed to be) University, Dehradun, by the CodeCrafters team (CD-VI-T166).
