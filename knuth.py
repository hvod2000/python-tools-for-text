from collections import namedtuple
from wcwidth import wcswidth as get_width
from mygraphemes import graphemes
from math import inf


def find_line_breaks_using_greedy_algo(blocks, line_lengths):
    print("greedy")
    lines = [[]]
    line_lengths = iter(line_lengths)
    cur_len = next(line_lengths)
    for block in blocks:
        if (
            sum(b.width for b in lines[-1]) + block.width > cur_len
            and lines[-1]
        ):
            lines.append([])
            cur_len = next(line_lengths)
        lines[-1].append(block)
    yield from lines


def where_to_put_line_breaks(blocks, line_lengths, limits=(0.95, 1.05)):
    low_limit, high_limit = limits

    def dp(blocks, line_lengths):
        if sum(b.width for b in blocks) < line_lengths[0]:
            return (0, [blocks])
        l = line_lengths[0] * low_limit
        h = line_lengths[0] * high_limit
        i = 0
        while sum(b.width for b in blocks[0:i]) < l:
            i += 1
        j = i
        while sum(b.width for b in blocks[0:j]) <= h and len(blocks) > j:
            j += 1
        options = [(sum(b.width for b in blocks[0:k]), k) for k in range(i, j)]
        if options:
            brk = [
                (
                    (
                        abs(sum(b.width for b in blocks[:k]) - line_lengths[0])
                        / k
                    )
                    ** 3,
                    dp(blocks[k:], line_lengths[1:]),
                    k,
                )
                for l, k in options
            ]
            return min(
                ((p1 + p2), [blocks[:k]] + tail) for p1, (p2, tail), k in brk
            )
        return (inf, [])

    penalty, lines = dp(blocks, line_lengths)
    if penalty < inf:
        yield from lines
    else:
        yield from find_line_breaks_using_greedy_algo(blocks, line_lengths)


Word = namedtuple("Word", "content width")


def break_text_for_console(text, line_length=72):
    words = [Word(w, get_width(w) + 1) for w in text.split()]
    line_lengths = [line_length] * len(words)
    return where_to_put_line_breaks(words, line_lengths)


def print_lines(lines, l=72):
    errors = []
    for line in lines:
        print(
            " ".join(w.content for w in line),
            abs(sum(w.width for w in line) - l) / len(line),
        )
        errors.append(abs((sum(w.width for w in line) - l) / len(line)))
    errors = errors[:-1]
    print("sum:", sum(errors))
    print("max:", max(errors))
    print("zrs:", sum(e == 0 for e in errors))
    print("gds:", sum(e <= 0.1 for e in errors))
