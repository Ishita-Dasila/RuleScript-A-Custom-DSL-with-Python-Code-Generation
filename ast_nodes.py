class ProgramNode:
    """
    Root node of the AST.
    Holds a list of all RULE definitions found in the source file.
    """
    def __init__(self, rules: list):
        self.rules = rules          # list of RuleNode

    def __repr__(self):
        rules_str = '\n  '.join(repr(r) for r in self.rules)
        return f'ProgramNode(\n  {rules_str}\n)'


class RuleNode:
    """
    Represents one complete RULE block.

      RULE <name>
        IF   <condition>
        THEN <then_statement>
        ELSE <else_statement>   ← optional
    """
    def __init__(self, name: str, if_node, line: int = 0):
        self.name    = name       # rule identifier string
        self.if_node = if_node    # IfNode
        self.line    = line       # source line (for error messages)

    def __repr__(self):
        return (f'RuleNode(name={self.name!r}, line={self.line},\n'
                f'    if_node={self.if_node!r})')


class IfNode:
    """
    Represents the IF / THEN / ELSE structure inside a rule.

      IF   <condition>
      THEN <then_body>
      ELSE <else_body>   ← may be None if no ELSE branch
    """
    def __init__(self, condition, then_body, else_body=None):
        self.condition = condition    # ConditionNode
        self.then_body = then_body    # AssignNode
        self.else_body = else_body    # AssignNode or None

    def __repr__(self):
        return (f'IfNode(\n'
                f'      condition={self.condition!r},\n'
                f'      then={self.then_body!r},\n'
                f'      else={self.else_body!r})')


class ConditionNode:
    """
    Represents a boolean condition expression.

      <left> <operator> <right>
      e.g.   age  >=  18

    left  – an identifier (variable name)
    op    – comparison operator string: >=, <=, ==, !=, >, <
    right – a number or boolean literal
    """
    def __init__(self, left: str, op: str, right):
        self.left  = left
        self.op    = op
        self.right = right

    def __repr__(self):
        return f'ConditionNode({self.left} {self.op} {self.right})'


class AssignNode:
    """
    Represents an assignment statement.

      <variable> = <value>
      e.g.   eligible = True

    variable – identifier string (left-hand side)
    value    – a number, boolean, or identifier (right-hand side)
    """
    def __init__(self, variable: str, value, line: int = 0):
        self.variable = variable
        self.value    = value
        self.line     = line

    def __repr__(self):
        return f'AssignNode({self.variable} = {self.value})'
