# Import all AST node types used to traverse the program structure
from ast_nodes import ProgramNode, RuleNode, IfNode, ConditionNode, AssignNode


class SemanticAnalyser:
    """
    This class performs semantic analysis (meaning checking).
    It walks through the AST and ensures there are no logical errors.
    """

    def __init__(self):
        # Stores all rule names encountered - used to detect duplicate rules
        self.rule_names: set = set()

        # Stores variables that have been defined/assigned earlier
        # Helps in checking whether a variable is used before definition
        self.defined_vars: set = set()

        # Allowed literal values (booleans) in the language
        self._literal_types = {'True', 'False'}

    # Main function that starts semantic analysis on the entire program
    def analyse(self, program: ProgramNode):
        # Loop through each rule in the program (top to bottom)
        for rule in program.rules:
            # Check each rule individually for errors
            self._check_rule(rule)

    
    # Check a single rule
    def _check_rule(self, rule: RuleNode):

        # Check if this rule name already exists - duplicate rule error
        if rule.name in self.rule_names:
            raise SemanticError(
                f"Line {rule.line}: Duplicate rule name '{rule.name}'. "
                f"Each RULE must have a unique name."
            )

        # Add this rule name to the set after validation
        self.rule_names.add(rule.name)

        # Check the IF condition and assignments inside this rule
        self._check_if(rule.if_node, rule.name)

    
    # Check IF–THEN–ELSE structure
    # This function validates the condition and the assignments in THEN and ELSE parts
    def _check_if(self, if_node: IfNode, rule_name: str):

        # First check whether the IF condition is valid
        self._check_condition(if_node.condition, rule_name)

        # Check the THEN part assignment (e.g., x = value)
        self._check_assign(if_node.then_body, rule_name)

        # After assignment, mark this variable as defined
        # So it can be used in future rules
        self.defined_vars.add(if_node.then_body.variable)

        # If ELSE part exists, validate it as well
        if if_node.else_body is not None:

            # Check ELSE assignment
            self._check_assign(if_node.else_body, rule_name)

            # Add ELSE variable also to defined variables
            self.defined_vars.add(if_node.else_body.variable)

    # Check IF condition
    def _check_condition(self, cond: ConditionNode, rule_name: str):

        # The left side of condition (e.g., age in "age > 18")
        # is treated as input → automatically considered defined
        self.defined_vars.add(cond.left)

        # Store right-hand side value
        right = cond.right

        # Case 1: If right side is a number → valid
        if self._is_number(right):
            return

        # Case 2: If right side is boolean (True/False) → valid
        if right in self._literal_types:
            return

        # Case 3: Otherwise, it must be a previously defined variable
        if right not in self.defined_vars:

            # If not defined earlier → semantic error
            raise SemanticError(
                f"In rule '{rule_name}': "
                f"Variable '{right}' used in condition but never defined. "
                f"Did you forget to assign it in a previous rule?"
            )

    # Check assignment statements
    def _check_assign(self, assign: AssignNode, rule_name: str):

        # Extract the value being assigned (right-hand side)
        value = assign.value

        # Case 1: If value is a number → valid assignment
        if self._is_number(value):
            return

        # Case 2: If value is boolean → valid assignment
        if value in self._literal_types:
            return

        # Case 3: If value is a variable → it must be defined before
        if value in self.defined_vars:
            return

        # If none of the above → invalid assignment
        raise SemanticError(
            f"Line {assign.line}: In rule '{rule_name}': "
            f"Value '{value}' used in assignment but never defined. "
            f"Use a number, True/False, or a variable from a previous rule."
        )

    # Utility function to check numeric values
    @staticmethod
    def _is_number(value: str) -> bool:

        # Try converting the value into an integer
        try:
            int(value)
            return True  # If conversion works → it's a number

        # If conversion fails → not a number
        except (ValueError, TypeError):
            return False


# Custom exception class for semantic errors
class SemanticError(Exception):
    """Raised when a semantic (logical) error is found in the program"""
    pass  # No extra code needed, just a custom error type