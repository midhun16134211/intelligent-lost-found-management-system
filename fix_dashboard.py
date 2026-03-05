import re

with open('templates/core/dashboard.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix multiline {{ user_rep.reputation_points\n...}} — join lines
content = re.sub(
    r'\{\{\s*user_rep\.reputation_points\s*\}\}',
    '{{ user_rep.reputation_points }}',
    content
)
content = re.sub(
    r'\{\{\s*user_rep\.items_returned\s*\}\}',
    '{{ user_rep.items_returned }}',
    content
)

# Verify fix
if 'user_rep.reputation_points\n' in content or 'reputation_points\r\n' in content:
    print('WARNING: Still has multiline split')
else:
    print('OK: reputation_points is on single lines now')

with open('templates/core/dashboard.html', 'w', encoding='utf-8') as f:
    f.write(content)

print('File saved.')
