import os
import sys
import re
import json
try:
    import jsonschema
except ImportError:
    jsonschema = None

def validate_research_md(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    errors = []
    
    mandatory_sections = [
        r'#\s+', # Title
        r'##\s+Methodology',
        r'##\s+Evidence|##\s+Benchmark|##\s+Hypothesis',
        r'##\s+Citations|##\s+References'
    ]
    
    for section in mandatory_sections:
        if not re.search(section, content, re.IGNORECASE):
            errors.append(f"Missing mandatory section or pattern: {section}")
            
    if not re.search(r'Collaborator:|Posted by:', content, re.IGNORECASE):
        errors.append("Missing attribution (Collaborator or Posted by)")

    return errors

def validate_json_schema(file_path, schema_path):
    if not jsonschema:
        return ["jsonschema library not installed. Skipping JSON validation."]
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        with open(schema_path, 'r', encoding='utf-8') as s:
            schema = json.load(s)
        
        jsonschema.validate(instance=data, schema=schema)
        return []
    except json.JSONDecodeError:
        return ["Invalid JSON file format."]
    except jsonschema.exceptions.ValidationError as e:
        return [f"Schema Validation Error: {e.message}"]
    except Exception as e:
        return [f"Unexpected error: {str(e)}"]

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python validator.py <path_to_file> [schema_path]")
        sys.exit(1)
        
    path = sys.argv[1]
    schema_path = sys.argv[2] if len(sys.argv) > 2 else None

    if not os.path.exists(path):
        print(f"Error: File {path} not found.")
        sys.exit(1)
    
    errors = []
    if path.endswith('.md'):
        errors = validate_research_md(path)
    elif path.endswith('.json') and schema_path:
        errors = validate_json_schema(path, schema_path)
    else:
        print("Unsupported file type or missing schema for JSON validation.")
        sys.exit(1)
    
    if errors:
        print(f"❌ Validation Failed for {path}:")
        for err in errors:
            print(f"  - {err}")
        sys.exit(1)
    else:
        print(f"✅ Validation Successful: {path} meets Moltit standards.")
        sys.exit(0)
