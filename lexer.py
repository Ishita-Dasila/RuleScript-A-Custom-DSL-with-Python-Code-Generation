import re  # Python's regular expression library

#  Token Types 
# Each constant is just a string label for readability.

KEYWORD    = 'KEYWORD'      # Reserved words: RULE, IF, THEN, ELSE
IDENTIFIER = 'IDENTIFIER'   # Variable/rule names: age, eligible
NUMBER     = 'NUMBER'        # Integer literals: 18, 0, 100
OPERATOR   = 'OPERATOR'      # Comparison & assignment: >=, <=, ==, !=, =, >, <
BOOLEAN    = 'BOOLEAN'       # True / False literals
NEWLINE    = 'NEWLINE'       # Line endings (used by parser)
EOF        = 'EOF'           # End of input sentinel


#  Reserved Keywords 
KEYWORDS = {'RULE', 'IF', 'THEN', 'ELSE'}


#  Token Class 
class Token:
    """
    Represents a single token with:
      type  – what kind of token it is (KEYWORD, NUMBER, etc.)
      value – the actual text from the source code
      line  – which line number it appeared on (for error messages)
    """
    def __init__(self, type_, value, line=0):
        self.type  = type_
        self.value = value
        self.line  = line

    def __repr__(self):
        return f'Token({self.type}, {repr(self.value)}, line={self.line})'


#  Lexer Class 
class Lexer:
    """
    Converts a source-code string into a list of Token objects.

    Usage:
        lexer  = Lexer(source_code)
        tokens = lexer.tokenize()
    """

    # Token patterns ordered from MOST specific to LEAST specific.
    # Each tuple: (token_type, regex_pattern)
    TOKEN_PATTERNS = [
        (BOOLEAN,    r'\b(True|False)\b'),          # Boolean literals first
        (KEYWORD,    r'\b(RULE|IF|THEN|ELSE)\b'),   # DSL keywords
        (NUMBER,     r'\b\d+\b'),                    # Integer numbers
        (OPERATOR,   r'>=|<=|==|!=|>|<|='),          # Multi-char ops before single-char
        (IDENTIFIER, r'\b[a-zA-Z_][a-zA-Z0-9_]*\b'),# Variable names
        (NEWLINE,    r'\n'),                          # Line breaks
    ]

    def __init__(self, source: str):
        self.source = source

    def tokenize(self) -> list:
        """
        Walk through the source string left-to-right.
        At each position, try every pattern in order.
        When a pattern matches at the current position, emit a token
        and advance past the matched text.
        Whitespace (spaces/tabs) is skipped silently.
        Unrecognised characters raise a LexerError.
        """
        tokens   = []
        position = 0          # current index into self.source
        line_num = 1          # track line number for error messages

        while position < len(self.source):
            char = self.source[position]

            #  Skip spaces and tabs 
            if char in (' ', '\t'):
                position += 1
                continue

            #  Skip single-line comments (# …) 
            if char == '#':
                while position < len(self.source) and self.source[position] != '\n':
                    position += 1
                continue

            matched = False

            #  Try every pattern 
            for token_type, pattern in self.TOKEN_PATTERNS:
                regex = re.compile(pattern)
                match = regex.match(self.source, position)  # anchor at current pos

                if match:
                    value = match.group(0)

                    if token_type == NEWLINE:
                        line_num += 1            # increment line counter
                    
                    tokens.append(Token(token_type, value, line_num))
                    position += len(value)       # advance past matched text
                    matched = True
                    break                        # stop trying other patterns

            if not matched:
                raise LexerError(
                    f"Unknown character '{char}' at line {line_num}"
                )

        # Always append EOF so the parser knows when to stop
        tokens.append(Token(EOF, 'EOF', line_num))
        return tokens


#  Custom Error Class 
class LexerError(Exception):
    """Raised when an unrecognised character is encountered."""
    pass
