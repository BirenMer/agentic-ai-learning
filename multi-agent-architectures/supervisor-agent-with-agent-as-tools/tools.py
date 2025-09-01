from langchain_tavily import TavilySearch
from dotenv import load_dotenv
from langchain_core.tools import tool

load_dotenv()

web_search = TavilySearch(max_results=3)

@tool
def add(a: float, b: float):
    """Add two numbers."""
    return a + b

@tool
def multiply(a: float, b: float):
    """Multiply two numbers."""
    return a * b

@tool
def divide(a: float, b: float):
    """Divide two numbers."""
    return a / b

@tool
def calculator_tool(expression: str) -> str:
    """Calculate mathematical expressions. Input should be a valid mathematical expression."""
    try:
        # Safe evaluation of mathematical expressions
        import ast
        import operator
        
        # Supported operations
        ops = {
            ast.Add: operator.add,
            ast.Sub: operator.sub,
            ast.Mult: operator.mul,
            ast.Div: operator.truediv,
            ast.Pow: operator.pow,
            ast.USub: operator.neg,
        }
        
        def eval_expr(expr):
            return eval_node(ast.parse(expr, mode='eval').body)
        
        def eval_node(node):
            if isinstance(node, ast.Constant):
                return node.value
            elif isinstance(node, ast.BinOp):
                return ops[type(node.op)](eval_node(node.left), eval_node(node.right))
            elif isinstance(node, ast.UnaryOp):
                return ops[type(node.op)](eval_node(node.operand))
            else:
                raise TypeError(node)
        
        result = eval_expr(expression)
        return f"The result of {expression} is {result}"
    except Exception as e:
        return f"Error calculating {expression}: {str(e)}"

## Test the Tool
# web_search_results = web_search.invoke("who is the mayor of NYC?")
# print(web_search_results["results"][0]["content"])