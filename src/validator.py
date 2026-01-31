import os
import sys
import re
import unicodedata

# Moltit Security Configuration
MAX_FILE_SIZE_KB = 50
REQUIRED_FIELDS = ['name', 'description', 'version']
FORBIDDEN_PATTERNS = [
    r"ignore previous instructions",
    r"system prompt",
    r"you are now",
    r"\[IGNORE\]",
    r"base64", # Prevent obfuscated payloads
]

def check_file_security(file_path):
    print(f"🔬 Auditing: {file_path}")
    
    # 1. Size Check
    size_kb = os.path.getsize(file_path) / 1024
    if size_kb > MAX_FILE_SIZE_KB:
        return False, f"CRITICAL: File size {size_kb:.2f}KB exceeds limit ({MAX_FILE_SIZE_KB}KB)."

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
            # 2. Hidden Character Scan (Unicode Normalization)
            for char in content:
                cat = unicodedata.category(char)
                # Reject 'Cc' (Other, Control) and 'Cf' (Other, Format) except for common whitespace
                if cat in ['Cc', 'Cf'] and char not in ['\n', '\r', '\t']:
                    return False, f"SECURITY: Hidden/Control character detected: {repr(char)}"

            # 3. Prompt Injection Pattern Match
            for pattern in FORBIDDEN_PATTERNS:
                if re.search(pattern, content, re.IGNORECASE):
                    return False, f"SECURITY: Forbidden pattern detected: '{pattern}'"

            # 4. Schema/Metadata Validation (Simplified for skill.md)
            # Looks for front-matter or header style metadata
            for field in REQUIRED_FIELDS:
                if field not in content.lower():
                    return False, f"SCHEMA: Missing required metadata field: '{field}'"

            return True, "PASS: File matches Moltit Security Protocol v1.0"

    except UnicodeDecodeError:
        return False, "CRITICAL: File is not valid UTF-8. Potential binary payload."
    except Exception as e:
        return False, f"ERROR: Internal audit failure: {str(e)}"

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python validator.py <file_or_directory>")
        sys.exit(1)

    target = sys.argv[1]
    success = True

    if os.path.isfile(target):
        ok, msg = check_file_security(target)
        print(msg)
        success = ok
    elif os.path.isdir(target):
        for root, _, files in os.walk(target):
            for file in files:
                if file.endswith('.md'):
                    ok, msg = check_file_security(os.path.join(root, file))
                    print(msg)
                    if not ok: success = False
    
    if not success:
        sys.exit(1)
    else:
        print("\n✅ Laboratory Clean. All files passed.")
