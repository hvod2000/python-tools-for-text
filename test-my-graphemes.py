codepoints = list("abowcrawqrfuwicrheantjrhewrai-")
from correct_codepoints import codepoints
from random import choice
from grapheme import graphemes as g1
from mygraphemes import graphemes as g2, get_width

def random_string(length):
    return ''.join(choice(codepoints) for _ in range(length))

errors = 0
N = 2**10
for i in range(N):
    s = random_string(3)
    y1 = list(g1(s))
    y2 = list(g2(s))
    if y1 != y2:
        errors += 1
        print('error')
        print(y1)
        print(y2)
        print(list(map(get_width,y1)))
        print(list(map(get_width,y2)))
print(f'error rate: {errors/N}')
