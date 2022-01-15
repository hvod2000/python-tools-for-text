from wcwidth import wcswidth as get_width

def graphemes(text):
    grapheme = ""
    for code in text:
        if get_width(code) != 0:
            if grapheme:
                yield grapheme
            grapheme = ""
        grapheme += code
    if grapheme:
        yield grapheme
