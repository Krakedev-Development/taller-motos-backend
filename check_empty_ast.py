import os
import ast

def check_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        try:
            tree = ast.parse(f.read(), filename=filepath)
        except Exception:
            return
            
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            # Check for empty functions: usually have only a 'pass' or a docstring + 'pass'
            body = node.body
            
            # Filter docstrings
            if isinstance(body[0], ast.Expr) and isinstance(body[0].value, ast.Constant):
                body = body[1:]
                
            if len(body) == 0:
                print(f"{filepath}:{node.lineno} Empty function {node.name}")
            elif len(body) == 1:
                stmt = body[0]
                if isinstance(stmt, ast.Pass):
                    print(f"{filepath}:{node.lineno} Empty function {node.name} (pass)")
                elif isinstance(stmt, ast.Return):
                    if isinstance(stmt.value, ast.Dict) and len(stmt.value.keys) == 0:
                        print(f"{filepath}:{node.lineno} Function {node.name} returns empty dict")
                    elif stmt.value is None:
                        print(f"{filepath}:{node.lineno} Function {node.name} returns None")
                    
for root, _, files in os.walk('src'):
    for f in files:
        if f.endswith('.py'):
            check_file(os.path.join(root, f))
