from lexer      import Token, KEYWORD, IDENTIFIER, NUMBER, OPERATOR, BOOLEAN, NEWLINE, EOF
from ast_nodes  import ProgramNode, RuleNode, IfNode, ConditionNode, AssignNode


class Parser:
    """
    Recursive-descent parser for RuleScript.

    Usage:
        parser = Parser(tokens)
        ast    = parser.parse()
    """

    def __init__(self, tokens: list):
        self.tokens  = tokens   # full token list from the lexer
        self.pos     = 0        # current read position

    #  Helpers 

    def current(self) -> Token:
        """Return the token at the current position."""
        return self.tokens[self.pos]

    def peek(self) -> Token:
        """Look one token ahead (doesn't advance)."""
        if self.pos + 1 < len(self.tokens):
            return self.tokens[self.pos + 1]
        return self.tokens[-1]          # return EOF if past end

    def advance(self) -> Token:
        """Consume and return the current token, then move forward."""
        tok = self.tokens[self.pos]
        if self.pos < len(self.tokens) - 1:
            self.pos += 1
        return tok

    def expect(self, type_: str, value: str = None) -> Token:
        """
        Consume the current token only if it matches the expected
        type (and optionally value).  Raises ParseError otherwise.
        """
        tok = self.current()

        type_match  = (tok.type  == type_)
        value_match = (value is None) or (tok.value == value)

        if type_match and value_match:
            return self.advance()

        expected = f'{type_}({value!r})' if value else type_
        raise ParseError(
            f"Line {tok.line}: Expected {expected} but got "
            f"{tok.type}({tok.value!r})"
        )

    def skip_newlines(self):
        """Skip any number of consecutive NEWLINE tokens."""
        while self.current().type == NEWLINE:
            self.advance()

    #  Grammar Rules 

    def parse(self) -> ProgramNode:
        """
        Entry point.
        program → rule*
        Parse every rule until we hit EOF.
        """
        rules = []
        self.skip_newlines()

        while self.current().type != EOF:
            rules.append(self.parse_rule())
            self.skip_newlines()

        return ProgramNode(rules)

    def parse_rule(self) -> RuleNode:
        """
        rule → RULE IDENTIFIER NEWLINE
               IF condition NEWLINE
               THEN assignment NEWLINE
               (ELSE assignment NEWLINE)?
        """
        #  RULE keyword 
        rule_tok = self.expect(KEYWORD, 'RULE')
        line     = rule_tok.line

        #  Rule name (identifier) 
        name_tok = self.expect(IDENTIFIER)
        name     = name_tok.value

        self.skip_newlines()

        #  IF keyword 
        self.expect(KEYWORD, 'IF')
        condition = self.parse_condition()
        self.skip_newlines()

        #  THEN keyword 
        self.expect(KEYWORD, 'THEN')
        then_body = self.parse_assignment()
        self.skip_newlines()

        #  ELSE keyword (optional) 
        else_body = None
        if self.current().type == KEYWORD and self.current().value == 'ELSE':
            self.advance()                    # consume ELSE
            else_body = self.parse_assignment()
            self.skip_newlines()

        if_node = IfNode(condition, then_body, else_body)
        return RuleNode(name, if_node, line)

    def parse_condition(self) -> ConditionNode:
        """
        condition → IDENTIFIER OPERATOR (NUMBER | BOOLEAN | IDENTIFIER)

        Parses the boolean expression after IF.
        """
        # Left-hand side must be an identifier (variable name)
        left_tok = self.expect(IDENTIFIER)

        # Operator: >=, <=, ==, !=, >, <
        op_tok = self.expect(OPERATOR)

        # Right-hand side: a number, boolean, or another variable
        right_tok = self.current()
        if right_tok.type in (NUMBER, BOOLEAN, IDENTIFIER):
            self.advance()
            right_val = right_tok.value
        else:
            raise ParseError(
                f"Line {right_tok.line}: Expected a value (number, True/False, "
                f"or variable) after operator, got {right_tok.type}({right_tok.value!r})"
            )

        return ConditionNode(left_tok.value, op_tok.value, right_val)

    def parse_assignment(self) -> AssignNode:
        """
        assignment → IDENTIFIER '=' (NUMBER | BOOLEAN | IDENTIFIER)

        Parses a single assignment statement (THEN or ELSE body).
        """
        var_tok = self.expect(IDENTIFIER)
        line    = var_tok.value

        # The assignment operator must be exactly '=' (not '==')
        op_tok = self.expect(OPERATOR, '=')

        val_tok = self.current()
        if val_tok.type in (NUMBER, BOOLEAN, IDENTIFIER):
            self.advance()
            return AssignNode(var_tok.value, val_tok.value, var_tok.line)
        else:
            raise ParseError(
                f"Line {val_tok.line}: Expected a value after '=', "
                f"got {val_tok.type}({val_tok.value!r})"
            )


#  Custom Error 
class ParseError(Exception):
    """Raised when the token stream violates the grammar."""
    pass
