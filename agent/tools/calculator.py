from langchain_core.tools import tool

@tool
def calculate(expression: str) -> str:
    """
    Safely evaluates a simple mathematical expression string (e.g., '340 * 1.16' or '2 + 2').
    Supports the 4 core operations: +, -, *, and / with two operands.
    """
    expression = expression.replace(" ", "")
    op = None
    op_idx = -1
    
    # Find the operator, ignoring a leading negative sign
    for i, char in enumerate(expression):
        if i == 0 and char == '-':
            continue
        if char in ('+', '-', '*', '/'):
            op = char
            op_idx = i
            break
            
    if not op:
        return "Error: No supported operator (+, -, *, /) found."
        
    try:
        a = float(expression[:op_idx])
        b = float(expression[op_idx+1:])
        
        if op == '+':
            return str(a + b)
        elif op == '-':
            return str(a - b)
        elif op == '*':
            return str(a * b)
        elif op == '/':
            if b == 0:
                return "Error: Division by zero."
            return str(a / b)
    except ValueError:
        return "Error: Could not parse operands as numbers."
