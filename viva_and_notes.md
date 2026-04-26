# RuleScript Compiler — Viva Q&A and Phase Notes

---

## Short Explanation of Compiler Phases

A compiler transforms source code written in one language into
another language (usually machine code or, in our case, Python).
The process is divided into well-defined phases:

| Phase | Module | Input | Output |
|---|---|---|---|
| 1. Lexical Analysis | `lexer.py` | Raw source string | List of tokens |
| 2. Syntax Analysis | `parser.py` | List of tokens | AST |
| 3. AST | `ast_nodes.py` | (data structure) | Tree of node objects |
| 4. Semantic Analysis | `semantic.py` | AST | Validated AST (or errors) |
| 5. Code Generation | `codegen.py` | Validated AST | Python source code |

**Think of it like this:**

```
Source Code
    ↓  Lexer        → breaks text into words (tokens)
    ↓  Parser       → checks grammar, builds tree
    ↓  Semantic     → checks meaning (types, names)
    ↓  Code Gen     → translates tree to Python
    ↓
Python Code
```

---

## Viva Questions and Answers

---

### Q1. What is a compiler? How is it different from an interpreter?

**Answer:**
A **compiler** translates the entire source program into a target language
*before* execution. The user runs the translated output separately.

An **interpreter** reads and executes source code *line by line*, directly,
without producing a separate output file.

**Example:** Python itself is (mostly) interpreted. GCC for C is a compiler.
In our project, RuleScript *compiles* `.rules` files into `.py` files, which
Python then interprets.

---

### Q2. What is Lexical Analysis? What does a token look like?

**Answer:**
Lexical analysis (scanning/tokenising) is the first phase. The lexer reads
the raw source text character by character, groups characters into meaningful
units called **tokens**, and labels each with a *type*.

A token in our project has three fields:
- `type`  – e.g. KEYWORD, IDENTIFIER, NUMBER, OPERATOR
- `value` – the actual text, e.g. `'IF'`, `'age'`, `'18'`, `'>='`
- `line`  – source line number (for error messages)

Example:
```
RULE check_age
↓ tokenised as ↓
Token(KEYWORD,    'RULE',       line=1)
Token(IDENTIFIER, 'check_age',  line=1)
Token(NEWLINE,    '\n',         line=1)
```

---

### Q3. What is a Regular Expression and why is it used in the Lexer?

**Answer:**
A **regular expression (regex)** is a pattern that describes a set of strings.
The lexer uses regexes to match different categories of text:

| Token type | Regex pattern |
|---|---|
| NUMBER | `\b\d+\b` |
| IDENTIFIER | `\b[a-zA-Z_][a-zA-Z0-9_]*\b` |
| OPERATOR | `>=|<=|==|!=|>|<|=` |

Python's `re` module applies these patterns at the *current position* in the
source string using `regex.match(source, position)`.

Regexes are ideal for lexers because token patterns are *regular languages*
(they don't require nested matching, which would need a parser).

---

### Q4. What is a Recursive Descent Parser?

**Answer:**
A **recursive descent parser** is a top-down parser where *each grammar rule
is implemented as a function*, and those functions call each other recursively
to match nested constructs.

In `parser.py`:
- `parse()` calls `parse_rule()` for each RULE found.
- `parse_rule()` calls `parse_condition()` and `parse_assignment()`.

This mirrors the grammar directly in code, making it easy to read and debug.

The parser is called *recursive* because complex rules (like nested IF blocks
in a real language) would call themselves recursively.

---

### Q5. What is an Abstract Syntax Tree (AST)? Draw one for a simple rule.

**Answer:**
An **AST** is a tree data structure that captures the *logical structure* of
the program, stripping away punctuation and keywords that are no longer needed
after parsing.

For `RULE check_age  IF age >= 18  THEN eligible = True  ELSE eligible = False`:

```
ProgramNode
  └── RuleNode("check_age")
        └── IfNode
              ├── condition: ConditionNode(age, >=, 18)
              ├── then_body: AssignNode(eligible = True)
              └── else_body: AssignNode(eligible = False)
```

Each node is a Python object defined in `ast_nodes.py`.

---

### Q6. What is Semantic Analysis? Give two errors it can catch.

**Answer:**
**Semantic analysis** checks that the program is *meaningful*, not just
grammatically correct. It walks the AST and applies logical rules.

Two errors our semantic analyser catches:

1. **Duplicate rule names** — Two rules cannot be named `check_age`.
   ```
   SemanticError: Line 9: Duplicate rule name 'check_age'.
   ```

2. **Undefined variable** — A condition references a variable that was never
   assigned by any previous rule.
   ```
   SemanticError: Variable 'ghost_var' used in condition but never defined.
   ```

Note: The *parser* only catches grammar errors (wrong token order).
The *semantic analyser* catches logical errors (wrong meaning).

---

### Q7. What is Code Generation? What is the target language in this project?

**Answer:**
**Code generation** is the final phase. It traverses the validated AST and
emits target-language code.

In RuleScript the target language is **Python**.

Each DSL rule becomes a Python function:

```
# DSL (source)              →   # Python (target)
RULE check_age                  def check_age(age):
IF age >= 18                        if age >= 18:
THEN eligible = True                    eligible = True
ELSE eligible = False               else:
                                        eligible = False
                                    return eligible
```

---

### Q8. What is the difference between a keyword and an identifier?

**Answer:**

| | Keyword | Identifier |
|---|---|---|
| Defined by | The language designer | The programmer |
| Examples in RuleScript | `RULE`, `IF`, `THEN`, `ELSE` | `age`, `eligible`, `check_age` |
| Can be used as a variable name? | No | Yes |

In `lexer.py`, keywords are matched **before** identifiers in
`TOKEN_PATTERNS` so that `RULE` is never mistakenly labelled an IDENTIFIER.

---

### Q9. What is the role of `main.py` in the compiler?

**Answer:**
`main.py` is the **driver** (or controller) of the compiler.
It does not implement any phase itself — it:

1. Reads the source file from disk.
2. Creates and calls each phase object in order:
   Lexer → Parser → SemanticAnalyser → CodeGenerator.
3. Prints phase-by-phase output to the terminal.
4. Writes the generated Python code to `output.py`.

It is the glue that connects all five modules into a working pipeline.

---

### Q10. What is a Domain-Specific Language (DSL)? How does RuleScript qualify?

**Answer:**
A **Domain-Specific Language (DSL)** is a small programming language designed
for a *specific problem domain*, unlike general-purpose languages (Python, C).

| Property | RuleScript |
|---|---|
| Domain | Rule-based logic / business rules |
| Keywords | Only 4: RULE, IF, THEN, ELSE |
| Expressiveness | Deliberately limited to one pattern |
| Target users | Non-programmers who write business rules |

Famous DSLs: SQL (databases), HTML (web layout), CSS (styling), Makefile
(build automation).

RuleScript qualifies because it has its own syntax, is only useful for
writing conditional rules, and compiles to a general-purpose language (Python).

---

## Quick-reference: Error Types in RuleScript

| Error Class | Module | Caused by |
|---|---|---|
| `LexerError` | `lexer.py` | Unknown character (e.g. `@`, `$`) |
| `ParseError` | `parser.py` | Wrong token order; missing keyword |
| `SemanticError` | `semantic.py` | Duplicate rule name; undefined variable |

---

*End of viva notes*
