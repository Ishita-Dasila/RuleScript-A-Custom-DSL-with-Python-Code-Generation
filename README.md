# 🧠 RuleScript — A Custom DSL Compiler in Python

> A fully working compiler that transforms a simple rule-based Domain-Specific Language into executable Python code — built from scratch with zero external dependencies.

---

## 📌 Table of Contents

- [What is RuleScript?](#what-is-rulescript)
- [Project Structure](#project-structure)
- [Compiler Phases](#compiler-phases)
- [How to Run](#how-to-run)
- [Writing Your Own Rules](#writing-your-own-rules)
- [Sample Input & Output](#sample-input--output)
- [Error Examples](#error-examples)
- [Viva / Interview Q&A](#viva--interview-qa)
- [Future Improvements](#future-improvements)
- [Resume Tips](#resume-tips)

---

## What is RuleScript?

RuleScript is a **Domain-Specific Language (DSL)** designed for writing simple conditional business rules. You write rules in plain English-like syntax, and the compiler converts them into clean, executable Python functions.

**Example — you write this:**
```
RULE check_age
IF age >= 18
THEN eligible = True
ELSE eligible = False
```

**Compiler generates this:**
```python
def check_age(age):
    """Auto-generated rule: check_age"""
    if age >= 18:
        eligible = True
    else:
        eligible = False
    return eligible
```

---

## Project Structure

```
RuleScript/
│
├── lexer.py            # Phase 1 — Tokenises source code using regex
├── parser.py           # Phase 2 — Recursive descent parser, builds AST
├── ast_nodes.py        # AST node class definitions
├── semantic.py         # Phase 4 — Semantic checks (names, variables)
├── codegen.py          # Phase 5 — Generates Python source code
├── main.py             # Driver — runs all phases end-to-end
│
├── input.rules         # Your DSL source file (edit this!)
├── output.py           # Auto-generated Python output
├── error_examples.rules# Intentional error demonstrations
└── README.md           # This file
```

---

## Compiler Phases

The compiler runs in **5 sequential phases**, each building on the previous:

```
input.rules  (raw text)
     │
     ▼
┌─────────────────────────────────────┐
│  Phase 1 — Lexical Analysis         │  lexer.py
│  Breaks text into tokens            │
│  "age >= 18" → [IDENTIFIER, OP, NUM]│
└──────────────────┬──────────────────┘
                   │ tokens
                   ▼
┌─────────────────────────────────────┐
│  Phase 2 — Syntax Analysis          │  parser.py
│  Checks grammar, builds tree        │
│  Validates IF/THEN/ELSE structure   │
└──────────────────┬──────────────────┘
                   │ AST
                   ▼
┌─────────────────────────────────────┐
│  Phase 3 — AST                      │  ast_nodes.py
│  Tree of node objects               │
│  RuleNode → IfNode → ConditionNode  │
└──────────────────┬──────────────────┘
                   │ AST
                   ▼
┌─────────────────────────────────────┐
│  Phase 4 — Semantic Analysis        │  semantic.py
│  Checks meaning, not just structure │
│  Catches duplicate rules, bad vars  │
└──────────────────┬──────────────────┘
                   │ validated AST
                   ▼
┌─────────────────────────────────────┐
│  Phase 5 — Code Generation          │  codegen.py
│  Walks AST, emits Python code       │
│  Each RULE → Python function        │
└──────────────────┬──────────────────┘
                   │
                   ▼
             output.py  (Python code)
```

---

## How to Run

**Requirements:** Python 3.6 or above. No external libraries needed.

```bash
# Step 1 — Clone or download the project
cd RuleScript

# Step 2 — Run the compiler (reads input.rules, writes output.py)
python main.py

# Step 3 — Run the generated Python code
python output.py

# Optional — specify custom files
python main.py my_rules.rules my_output.py
```

---

## Writing Your Own Rules

Open `input.rules` and write rules using this syntax:

```
RULE <rule_name>
IF <variable> <operator> <value>
THEN <variable> = <value>
ELSE <variable> = <value>
```

`ELSE` is **optional**. You can skip it if not needed.

### Supported Operators

| Operator | Meaning               |
|----------|-----------------------|
| `>=`     | Greater than or equal |
| `<=`     | Less than or equal    |
| `==`     | Equal to              |
| `!=`     | Not equal to          |
| `>`      | Greater than          |
| `<`      | Less than             |

### Rules for Valid Input

- Rule names must be **unique** (no duplicates)
- Rule names **cannot contain spaces** — use `check_marks` not `check marks`
- Values can be a **number** (`18`, `500`) or **boolean** (`True` / `False`)
- Each of `IF`, `THEN`, `ELSE` must be on its **own line**
- Lines starting with `#` are **comments** and are ignored

### Example Input

```
# Check exam result
RULE check_marks
IF marks >= 90
THEN grade = True
ELSE grade = False

# Check fever
RULE check_temperature
IF temp > 100
THEN fever = True
ELSE fever = False

# Check withdrawal eligibility (no ELSE needed)
RULE check_balance
IF balance >= 500
THEN can_withdraw = True
```

---

## Sample Input & Output

**Input (`input.rules`):**
```
RULE check_age
IF age >= 18
THEN eligible = True
ELSE eligible = False
```

**Terminal output (from `main.py`):**
```
Phase 1 — Lexical Analysis
✔  Tokenised successfully. 24 tokens produced.

Phase 2 — Syntax Analysis
✔  Parsed successfully. 1 rule(s) found.

Phase 3 — AST
  RULE: check_age  (line 1)
    IF   → age  >=  18
    THEN → eligible = True
    ELSE → eligible = False

Phase 4 — Semantic Analysis
✔  Semantic checks passed.

Phase 5 — Code Generation
✔  Output written to 'output.py'
```

**Generated `output.py`:**
```python
def check_age(age):
    """Auto-generated rule: check_age"""
    if age >= 18:
        eligible = True
    else:
        eligible = False
    return eligible
```

---

## Error Examples

The compiler gives clear, helpful error messages for all three error types:

### Lexer Error — Unknown character
```
# Input
RULE bad_char
IF age @@ 18
THEN eligible = True

# Error
LexerError: Unknown character '@' at line 2
```

### Parse Error — Missing keyword
```
# Input
RULE missing_then
IF age >= 18
eligible = True       ← missing THEN

# Error
ParseError: Line 3: Expected KEYWORD('THEN') but got IDENTIFIER('eligible')
```

### Semantic Error — Duplicate rule name
```
# Input
RULE check_age
IF age >= 18
THEN eligible = True

RULE check_age        ← same name used again
IF score >= 50
THEN result = True

# Error
SemanticError: Line 6: Duplicate rule name 'check_age'.
```

### Semantic Error — Undefined variable
```
# Input
RULE check_ghost
IF age >= ghost_var    ← ghost_var was never defined

# Error
SemanticError: Variable 'ghost_var' used in condition but never defined.
```

---

## Viva / Interview Q&A

**Q1. What is a compiler?**
A compiler translates source code from one language to another (usually to machine code or, in our case, Python) before execution. Unlike an interpreter which runs code line-by-line, a compiler processes the entire program first.

**Q2. What is Lexical Analysis?**
The first compiler phase. It reads raw source text and breaks it into tokens — small labelled units like KEYWORD, IDENTIFIER, NUMBER, OPERATOR. Example: `age >= 18` becomes three tokens.

**Q3. What is a Regular Expression and why is it used in the Lexer?**
A regex is a pattern that describes a set of strings. The lexer uses regexes to match token categories (numbers, identifiers, operators) at each position in the source string. Regex is ideal because token patterns are regular languages.

**Q4. What is a Recursive Descent Parser?**
A top-down parser where each grammar rule is a function, and those functions call each other to match nested structures. It mirrors the grammar directly in code, making it easy to read and debug.

**Q5. What is an AST?**
Abstract Syntax Tree — a tree that captures the logical structure of a program, stripping away punctuation. Each node is a Python object. Example: `RuleNode → IfNode → ConditionNode`.

**Q6. What is Semantic Analysis?**
Checks that the program is *meaningful*, not just grammatically correct. Catches things the parser cannot: duplicate rule names, undefined variables, type mismatches.

**Q7. What is the difference between a Lexer error and a Parse error?**
A Lexer error is an unrecognised *character* (e.g. `@`). A Parse error is a wrong *token order* (e.g. missing `THEN` keyword).

**Q8. What is a DSL?**
Domain-Specific Language — a small programming language designed for one specific problem area. Examples: SQL (databases), HTML (web), CSS (styling). RuleScript is a DSL for writing business rules.

**Q9. What is Code Generation?**
The final compiler phase. It walks the validated AST and emits target-language code. In RuleScript, each DSL rule becomes a Python function.

**Q10. Why do we need a Symbol Table?**
A symbol table stores information about every identifier (name, type, scope, where defined). It is used during semantic analysis and code generation to verify and look up variables.

---

## Future Improvements

This section lists features you can add to make RuleScript more powerful and production-ready. Each is a potential mini-project on its own.

---

### 🔵 Beginner Level

#### 1. Flask Web Interface
Build a browser UI where users type rules and see generated Python live — no terminal needed.
- **Tech:** Python Flask, HTML, JavaScript
- **What to build:** A text area for input, a compile button, and a code output panel
- **Resume line:** *"Built a web-based compiler interface with real-time DSL-to-Python code generation"*

#### 2. Better Error Messages
Add suggestions alongside errors to guide the user:
```
ParseError: Line 3 — Did you forget the THEN keyword?
Expected: THEN <variable> = <value>
Got:      eligible = True
```

#### 3. Line-by-Line Error Highlighting
When an error occurs, print the actual source line with a `^` pointer under the problem character — just like Python itself does.
```
IF age @@ 18
       ^^
LexerError: Unknown character '@'
```

#### 4. Support String Values
Allow string literals on the right-hand side of assignments:
```
THEN status = "approved"
THEN message = "access denied"
```

---

### 🟡 Intermediate Level

#### 5. AND / OR Compound Conditions
Extend the grammar to support compound boolean expressions:
```
RULE check_senior_discount
IF age >= 60 AND purchase >= 500
THEN discount = True
ELSE discount = False
```
This requires changes to `lexer.py` (new keywords), `parser.py` (new grammar rule), and `ast_nodes.py` (new `CompoundConditionNode`).

#### 6. Multi-Target Code Generation
Add a `--target` flag to generate Java or JavaScript instead of Python:
```bash
python main.py input.rules --target java
python main.py input.rules --target javascript
```
- **What to build:** Separate `codegen_java.py` and `codegen_js.py` modules
- **Resume line:** *"Implemented multi-target code generation supporting Python, Java, and JavaScript"*

#### 7. Symbol Table with Types
Build a proper symbol table that tracks the type of every variable (boolean, integer, string) and raises an error when types are mismatched:
```
SemanticError: Cannot compare integer 'age' with boolean 'True'
```

#### 8. Unit Tests with pytest
Add a `tests/` folder with test cases for every phase:
```
tests/
  test_lexer.py      ← test all token types, error cases
  test_parser.py     ← test valid and invalid grammar
  test_semantic.py   ← test duplicate rules, undefined vars
  test_codegen.py    ← test generated Python is correct
```
- **Resume line:** *"Achieved 90%+ test coverage across all compiler phases using pytest"*

#### 9. WHILE Loop Support
Add looping constructs to the DSL:
```
RULE apply_interest
WHILE balance < 1000
THEN balance = balance + 10
```

#### 10. Multiple Statements in THEN / ELSE
Allow more than one assignment per branch:
```
RULE check_vip
IF purchase >= 5000
THEN discount = True
THEN points = 500
THEN status = "VIP"
```

---

### 🔴 Advanced Level

#### 11. Optimizer Phase (Phase 6)
Add a sixth compiler phase between semantic analysis and code generation that simplifies the AST:
- **Constant folding:** `IF 5 >= 3` → always True → remove dead branch
- **Dead code elimination:** Rules that can never execute
- **Resume line:** *"Implemented AST optimization pass with constant folding and dead-code elimination"*

#### 12. Intermediate Representation (IR)
Add a phase that converts the AST into a simple three-address code (like LLVM IR) before generating the final target language. This is how real-world compilers work.
```
t1 = age >= 18
IF t1 GOTO L1
eligible = False
GOTO L2
L1: eligible = True
L2:
```

#### 13. REPL (Interactive Shell)
Build a Read-Eval-Print Loop so users can type and compile rules interactively in the terminal, one at a time — like Python's interactive shell.
```
RuleScript> RULE check_age
RuleScript> IF age >= 18
RuleScript> THEN eligible = True
RuleScript> (compiling...)
✔ Generated: def check_age(age): ...
```

#### 14. VS Code Extension
Build a VS Code syntax highlighting extension for `.rules` files so keywords like `RULE`, `IF`, `THEN`, `ELSE` are coloured differently. Uses TextMate grammar files (JSON).
- **Resume line:** *"Published a VS Code language extension for RuleScript syntax highlighting"*

#### 15. Rule Execution Engine
Instead of generating Python code, build a runtime interpreter that directly evaluates rules against a data dictionary:
```python
engine = RuleEngine()
engine.load("input.rules")
result = engine.run("check_age", {"age": 20})
# → {"eligible": True}
```

---

### 📊 Complexity Roadmap

| Feature | Difficulty | Time Estimate | Impact |
|---|---|---|---|
| Flask Web UI | Beginner | 3–4 hrs | ⭐⭐⭐⭐⭐ |
| Unit Tests | Beginner | 2–3 hrs | ⭐⭐⭐⭐ |
| Better Error Messages | Beginner | 1–2 hrs | ⭐⭐⭐ |
| String Values | Beginner | 1–2 hrs | ⭐⭐⭐ |
| AND / OR Conditions | Intermediate | 3–4 hrs | ⭐⭐⭐⭐ |
| Multi-Target Codegen | Intermediate | 4–5 hrs | ⭐⭐⭐⭐⭐ |
| Symbol Table | Intermediate | 3–4 hrs | ⭐⭐⭐⭐ |
| Optimizer Phase | Advanced | 5–6 hrs | ⭐⭐⭐⭐⭐ |
| VS Code Extension | Advanced | 4–6 hrs | ⭐⭐⭐⭐⭐ |
| REPL Shell | Advanced | 3–4 hrs | ⭐⭐⭐⭐ |

---

## Resume Tips

### How to describe this project on your resume:

```
RuleScript — Custom DSL Compiler                           Python
• Designed and implemented a full 5-phase compiler pipeline (Lexer → Parser →
  AST → Semantic Analyser → Code Generator) for a Domain-Specific Language
• Built recursive descent parser and regex-based tokeniser from scratch
• Implemented semantic analysis catching duplicate rules and undefined variables
• Compiler generates clean, executable Python functions from DSL rule definitions
• Published on GitHub with full documentation, sample inputs, and error examples
```

### After adding future features, upgrade to:

```
RuleScript — Custom DSL Compiler                  Python | Flask | pytest
• Architected a 6-phase compiler (Lexer, Parser, AST, Semantic, Optimizer,
  CodeGen) for a custom business-rule DSL, generating Python/Java/JavaScript
• Built a Flask web interface for live DSL-to-Python compilation in the browser
• Extended grammar to support compound AND/OR conditions and string literals
• Achieved 92% test coverage across all compiler phases using pytest
• Published open-source on GitHub with CI pipeline and full documentation
```

---

## Tech Stack

| Component | Technology |
|---|---|
| Language | Python 3.6+ |
| Tokeniser | Python `re` (regex) module |
| Parser | Hand-written Recursive Descent |
| Testing (future) | pytest |
| Web UI (future) | Flask |
| Version Control | Git / GitHub |

---

## Author

Built as a Compiler Design college project demonstrating all major phases of a compiler pipeline using a custom Domain-Specific Language.

---

*"Any sufficiently advanced compiler is indistinguishable from magic."*
