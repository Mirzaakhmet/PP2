import re

with open(r"C:\Users\Asus\Documents\Little\PP2\lab5\row.txt", 'r', encoding='utf-8') as f:
    row = f.read()

print(row)

# Task 1
res = re.findall(r'a[b]*', row)
print(res)

# Task 2
res = re.findall(r'ab{2,3}', row)
print(res)

# Task 3
res = re.findall(r'[a-z]+(?:_[a-z]+)+', row)
print(res)

# Task 4
res = re.findall(r'[A-Z][a-z]+', row)
print(res)

# Task 5
res = re.findall(r'a.*b$', row, re.MULTILINE)  
print(res)

# Task 6
res = re.sub(r'[\s,.]+', ':', row)
print(res)

# Task 7
words = row.split('_')
camel_str = words[0] + ''.join(word.capitalize() for word in words[1:])
print(camel_str)

# Task 8
result = re.split(r'(?=[A-Z])', row)
result = [part for part in result if part] 
print(result)

# Task 9
res = re.sub(r'(?<=[a-z])(?=[A-Z])', ' ', row)
print(res)

# Task 10
snake_str = re.sub(r'([a-z])([A-Z])', r'\1_\2', row).lower()
print(snake_str)
