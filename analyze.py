import re

try:
    with open('template.yml', 'r', encoding='utf-8') as f:
        content = f.read()

    # Split by functions
    blocks = content.split('Type: AWS::Serverless::Function')
    
    for block in blocks[1:]:
        # Find CodeUri
        code_uri_match = re.search(r'CodeUri:\s*([^\n]+)', block)
        code_uri = code_uri_match.group(1).strip() if code_uri_match else 'N/A'
        
        # Find Path
        path_match = re.search(r'Path:\s*([^\n]+)', block)
        path = path_match.group(1).strip() if path_match else 'N/A'
        
        # Find Method
        method_match = re.search(r'Method:\s*([^\n]+)', block)
        method = method_match.group(1).strip().upper() if method_match else 'N/A'
        
        if path != 'N/A' and method != 'N/A':
            print(f"{method} {path} | {code_uri}")
except Exception as e:
    print('Error:', e)
