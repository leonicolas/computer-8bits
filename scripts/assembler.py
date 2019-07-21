#!python
import sys

if len(sys.argv) != 2:
    print('usage: a.py <input>')
    exit(-1)

def lex(content):
    i = 0; size = len(content)

    while i < size:
        token = content[i]
        i += 1; type = 'BLK'
        # Spaces
        if token.isspace():
            while i < size and content[i].isspace():
                token += content[i]; i += 1
        # Commentaries
        elif token == '#' or token == ';':
            type = 'COM'
            while i < size and content[i] != '\n':
                token += content[i]; i += 1
        # Strings
        elif token.isalpha():
            type = 'STR'
            while i < size and content[i].isalnum():
                token += content[i]; i += 1
        # Directives
        elif token == '.':
            type = 'DIR'
            while i < size and content[i].isalnum():
                token += content[i]; i += 1
        # Numbers
        elif token.isnumeric():
            type = 'NUM'
            while i < size and content[i].isnumeric():
                token += content[i]; i += 1
        # Symbols
        else:
            type = 'SYM'

        yield (token, type)

zops = {
    'NOP':  0x00,
    'HALT': 0x01,
    'OUTA': 0x0C,
    'OUTB': 0x0D
}

ops = {
    'LDA':  { 1: 0x02, 2: 0x03 },
    'STA':  { 2: 0x04 },
    'LDB':  { 1: 0x05, 2: 0x06 },
    'STB':  { 2: 0x07 },
    'ADD':  { 1: 0x08, 2: 0x09 },
    'SUB':  { 1: 0x0A, 2: 0x0B },

    'OUT':  { 1: 0x0E, 2: 0x0F },

    'JP':   { 2: 0x10 },
    'JPZ':  { 2: 0x11 },
    'JPC':  { 2: 0x12 }
}

def parse(content):
    fn = lambda t: t[1] != 'BLK' and t[1] != 'COM'
    lexer = filter(fn, lex(content))

    mem = []; labels = {}; fwd = []

    while True:
        (token, type) = next(lexer, (0,0))
        if (type == 0):
            break

        if type == 'STR':
            if token in zops:
                mem.append(zops[token])
            elif token in ops:
                ins = token

                (token, type) = next(lexer)

                is_addr = (token == '[')

                if is_addr:
                    if not (2 in ops[ins]):
                        exit(-1)
                    (token, type) = next(lexer)
                    mem.append(ops[ins][2])
                else:
                    mem.append(ops[ins][1])

                if type == 'NUM':
                    mem.append(int(token))
                elif type == 'STR':
                    if token in labels:
                        mem.append(labels[token])
                    else:
                        fwd.append((token, len(mem)))
                        mem.append(0)
                else:
                    exit(-1)

                if (is_addr and next(lexer)[0] != ']'):
                    exit(-1)
            else: # label
                if token in labels: # already defined
                    exit(-1)
                else:
                    labels[token] = len(mem)
                if next(lexer)[0] != ':':
                    exit(-1)
        elif type == 'DIR': # directive
            if token == '.BYTE':
                (token, type) = next(lexer)
                if type != 'NUM':
                    exit(-1)
                mem.append(int(token))
            else:
                exit(-1)

    for f in fwd:
        if f[0] in labels:
            mem[f[1]] = labels[f[0]]
        else:
            exit(-1)

    print('v2.0 raw')
    for m in mem:
        print(format(m, '02X') + ' ', end='')

parse(open(sys.argv[1], 'r').read())

