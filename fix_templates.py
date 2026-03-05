"""
Fix multiline {{ variable }} tags in all Django templates.
Django cannot parse {{ on one line with }} on the next line.
"""
import re
import os

TEMPLATES_DIR = 'templates'
fixed_files = []

# Regex: match {{ followed by any whitespace+newlines, then content, then }}
# This joins split {{ variable\n   }} into {{ variable }}
multiline_var_pattern = re.compile(
    r'\{\{([^}]*?)\n([^}]*?)\}\}',
    re.DOTALL
)

def collapse_split_tags(content):
    """Collapse multiline {{ }} tags onto single lines."""
    original = content
    # Keep collapsing until stable (handles multiple splits)
    while True:
        new = multiline_var_pattern.sub(
            lambda m: '{{ ' + (m.group(1) + ' ' + m.group(2)).strip() + ' }}',
            content
        )
        if new == content:
            break
        content = new
    return content

for root, dirs, files in os.walk(TEMPLATES_DIR):
    # Skip hidden dirs
    dirs[:] = [d for d in dirs if not d.startswith('.')]
    for fname in files:
        if not fname.endswith('.html'):
            continue
        fpath = os.path.join(root, fname)
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        fixed = collapse_split_tags(content)
        if fixed != content:
            with open(fpath, 'w', encoding='utf-8') as f:
                f.write(fixed)
            fixed_files.append(fpath)
            print(f'FIXED: {fpath}')

if not fixed_files:
    print('No multiline {{ }} splits found — all templates clean.')
else:
    print(f'\nTotal files fixed: {len(fixed_files)}')
