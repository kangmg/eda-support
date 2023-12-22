import sys

filename = sys.argv[1]
order = sys.argv[2:]

with open(filename, 'r',encoding='utf-8') as f:
    content = f.read().strip('\n')
    lines = content.split('\n')

if len(lines) != len(order):
    print('Plz check your system argv')

new_lines = []
for num in order:
    new_lines.append(lines[int(num)-1])

new_content = '\n'.join(new_lines).strip('\n')

with open(filename, 'w') as f:
    f.write(new_content)
