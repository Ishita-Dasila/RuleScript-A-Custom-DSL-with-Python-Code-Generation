process.env.GROQ_API_KEY = "your-api-key-here";
require("dotenv").config();
const express = require("express");
const cors = require("cors");
const bodyParser = require("body-parser");
const fetch = require("node-fetch");

const app = express();
const PORT = 3000;

app.use(cors());
app.use(bodyParser.json());
const path = require("path");

// Serve all frontend files (VERY IMPORTANT)
app.use(express.static(path.join(__dirname)));

app.get("/", (req, res) => {
  res.sendFile(path.join(__dirname, "index.html"));
});

//  Existing route: Quiz explanation 
app.post("/explain", async (req, res) => {
  const { question, options, userAnswer, correctAnswer } = req.body;

  if (!question || !options || !correctAnswer) {
    return res.status(400).json({ reply: "Invalid request data" });
  }

  try {
    const response = await fetch("https://api.groq.com/openai/v1/chat/completions", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${process.env.GROQ_API_KEY}`
      },
      body: JSON.stringify({
        model: "llama-3.3-70b-versatile",
        max_tokens: 300,
        messages: [
          {
            role: "user",
            content: `You are a helpful quiz tutor. Explain why the answer is correct in 2-3 simple lines.

Question: ${question}
Options: ${options}
User's Answer: ${userAnswer}
Correct Answer: ${correctAnswer}

Keep it short and beginner friendly.`
          }
        ]
      })
    });

    const data = await response.json();
    const reply = data.choices[0].message.content;
    res.json({ reply });

  } catch (err) {
    console.log(err);
    res.status(500).json({ reply: "Something went wrong, please try again." });
  }
});


//  NEW route: RuleScript Compiler AI Agent 
// The system prompt tells the AI everything about our project
// AND general compiler design theory, so it can answer both.

const COMPILER_SYSTEM_PROMPT = `You are an expert teaching assistant for the RuleScript Compiler project.
You also have deep knowledge of general compiler design theory and concepts.
Answer any question the user asks — whether it is about this specific project or about compilers in general.

--- PROJECT OVERVIEW ---
RuleScript is a custom mini-language that lets users write simple business rules like:
  RULE check_age
  IF age >= 18
  THEN eligible = True
  ELSE eligible = False

The compiler reads a .rules file and translates it into working Python functions.

--- THE 5 COMPILER PHASES (in this project) ---

PHASE 1 - LEXICAL ANALYSIS (lexer.py):
- Reads the source code character by character
- Breaks it into tokens: KEYWORD, IDENTIFIER, NUMBER, OPERATOR, BOOLEAN, NEWLINE, EOF
- Keywords are: RULE, IF, THEN, ELSE
- Raises a LexerError (hard stop) if it finds an invalid character like @, $, %, &, ~
- Example tokens for "age >= 18": IDENTIFIER(age), OPERATOR(>=), NUMBER(18)

PHASE 2 - SYNTAX ANALYSIS (parser.py):
- Takes the list of tokens and checks they are in the correct ORDER (grammar)
- Builds an AST (Abstract Syntax Tree) from them
- Grammar rule: RULE <name>  IF <var> <op> <val>  THEN <var> = <val>  [ELSE <var> = <val>]
- Raises a ParseError (hard stop) if grammar is wrong
- Common errors: missing THEN, using == instead of =, no rule name after RULE

PHASE 3 - AST (Abstract Syntax Tree):
- The tree is already built in Phase 2; Phase 3 just prints/displays it
- Nodes: ProgramNode (root) > RuleNode > IfNode > ConditionNode / AssignNode
- Never raises errors — always completes successfully

PHASE 4 - SEMANTIC ANALYSIS (semantic.py):
- Checks meaning, not just grammar
- Detects: duplicate rule names, undefined variables used in conditions
- Never raises errors — gives WARNINGS only, compilation always continues
- Collects all variable names and rule names

PHASE 5 - CODE GENERATION (codegen.py):
- Converts the AST into Python functions
- Each RULE becomes a def function
- The condition becomes an if/else block in Python
- The output is saved to output.py
- Never raises errors — always completes

--- FILES IN THE PROJECT ---
- input.rules       : the source code written in RuleScript language
- lexer.py          : Phase 1 — tokenisation
- parser.py         : Phase 2 — grammar checking, builds AST
- ast_nodes.py      : data classes: ProgramNode, RuleNode, IfNode, ConditionNode, AssignNode
- semantic.py       : Phase 4 — semantic checks, warnings only
- codegen.py        : Phase 5 — generates Python code
- main.py           : runs all 5 phases, also runs error example files
- output.py         : generated Python code (output of compiler)
- result.json       : full compiler output in JSON (used by dashboard)
- dashboard.html    : web page showing all 5 phases visually
- server.js         : Node.js/Express backend, serves /explain and /ask routes

--- ERROR FILES USED IN DEMO ---
- error1_lexer.rules         : has a bad character like @
- error2_missing_then.rules  : THEN keyword is missing
- error3_double_equals.rules : uses == instead of = in THEN/ELSE
- error4_missing_rulename.rules : no name given after RULE
- error5_duplicate_rule.rules   : two rules with the same name (Phase 4 warning)
- error6_undefined_var.rules    : variable used in condition but never defined (Phase 4 warning)

--- KEY CONCEPTS (project-specific) ---
- Token: the smallest meaningful piece of code (like a word in English)
- Lexer/Tokenizer: splits source code into tokens
- Parser: checks if tokens are in the right grammatical order
- AST: a tree that represents the structure of the program
- Semantic analysis: checks the meaning, not just the structure
- Code generation: converts the AST into another language (here, Python)
- Hard error: stops compilation immediately (Phase 1 and 2 only)
- Warning: noted but compilation continues (Phase 4 only)

--- GENERAL COMPILER DESIGN KNOWLEDGE ---
You also know everything about compiler design theory. Answer any general compiler question even if it is not about this project. Topics include:

PHASES OF A COMPILER (general):
- Lexical Analysis: tokenisation, regular expressions, DFA/NFA, symbol table intro
- Syntax Analysis: CFG (Context Free Grammar), Top-Down parsing (Recursive Descent, LL(1)) and Bottom-Up parsing (LR, SLR, LALR, CLR)
- Semantic Analysis: type checking, scope resolution, symbol table management
- Intermediate Code Generation: three-address code, quadruples, triples, DAG
- Code Optimisation: constant folding, dead code elimination, loop optimisation, common subexpression elimination
- Code Generation: register allocation, instruction selection, target machine code

OTHER IMPORTANT COMPILER CONCEPTS:
- Symbol Table: stores identifier names, types, scope, memory location
- Error Recovery: panic mode, phrase level, error productions, global correction
- Ambiguous Grammars: one string has more than one parse tree
- Left Recursion and Left Factoring: grammar transformations needed for top-down parsing
- FIRST and FOLLOW sets: used to build LL(1) parsing tables
- Shift-Reduce and Reduce-Reduce Conflicts in LR parsing
- Activation Records / Stack Frames: memory layout during function calls
- Compiler vs Interpreter vs Assembler: key differences
- Bootstrapping a compiler
- Single-pass vs multi-pass compilers
- Front end vs back end of a compiler
- Linker and Loader

When answering general theory questions, give clear definitions with simple examples.
When helpful, connect the concept back to this RuleScript project to make it more relatable.

IMPORTANT - for broad questions like "explain compiler design", "tell me everything about compilers",
"explain all phases", or "what is compiler design as a subject":
- Give a COMPLETE, structured answer covering the full subject
- Use clear headings for each topic/phase
- Explain each concept with a definition, how it works, and a small example
- Do NOT cut your answer short — cover everything thoroughly
- Go phase by phase, concept by concept, like a proper study guide

If the question is completely unrelated to compilers or computer science, politely redirect them.`;

app.post("/ask", async (req, res) => {
  // history is an array of { role: "user" | "assistant", content: "..." }
  // this allows multi-turn chat (the user can ask follow-up questions)
  const { message, history } = req.body;

  if (!message) {
    return res.status(400).json({ reply: "No message provided." });
  }

  // Build the messages array: system prompt + past conversation + new user message
  var messages = [];

  // Add past conversation turns (so the AI remembers what was said)
  if (history && Array.isArray(history)) {
    for (var i = 0; i < history.length; i++) {
      messages.push(history[i]);
    }
  }

  // Add the new user message
  messages.push({ role: "user", content: message });

  try {
    const response = await fetch("https://api.groq.com/openai/v1/chat/completions", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${process.env.GROQ_API_KEY}`
      },
      body: JSON.stringify({
        model: "llama-3.3-70b-versatile",
        max_tokens: 2000,
        messages: [
          // System prompt goes first — tells AI its role and all project + theory knowledge
          { role: "system", content: COMPILER_SYSTEM_PROMPT },
          ...messages
        ]
      })
    });

    const data = await response.json();
    console.log("AI Agent response:", JSON.stringify(data));

    if (!data.choices || !data.choices[0]) {
      return res.status(500).json({ reply: "AI did not return a response." });
    }

    const reply = data.choices[0].message.content;
    res.json({ reply: reply });

  } catch (err) {
    console.log("Error in /ask route:", err);
    res.status(500).json({ reply: "Something went wrong. Please try again." });
  }
});


app.listen(PORT, function() {
  console.log("Server running at http://localhost:" + PORT);
});
