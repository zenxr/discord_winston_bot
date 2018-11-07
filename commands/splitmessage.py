# function to split strings into lists of single words
def splitmessage(s):
    words = []
    inword = 0
    for c in s:
        if c in " \r\n\t": #whitepsace
            inword = 0
        elif not inword:
            words = words + [c]
            inword = 1
        else:
            words[-1] = words[-1] + c
    return words