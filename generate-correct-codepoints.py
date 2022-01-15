characters = []
for i in range(144_698):
    try:
        char = chr(i)
        print(i, char)
        characters.append(i)
    except Exception:
        pass

with open('correct_codepoints.py', 'wt') as f:
    f.write("codepoints=["+', '.join(repr(chr(c)) for c in characters)+']')
