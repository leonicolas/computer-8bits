#!python3

from collections import OrderedDict 
import save_rom

fetch = [0x0104, 0x0068]

instruction_set = OrderedDict([
    ('halt', {
        'op_code': 0x0, 'af': [0, 1], 'cf': [0, 1], 'zf': [0, 1],
        'flags': [ 0x8000 ]
    }),
    ('lda_num', {
        'op_code': 0x1, 'af': 0, 'cf': [0, 1], 'zf': [0, 1],
        'flags': [ 0x401C ]
    })
])

def generate_microcode(fetch, instruction_set):
    microcode = list()

    for instruction_name in instruction_set:
        instruction_microcode = list(fetch);
        step = 0

        print(instruction_name)
        print(instruction_set[instruction_name])

microcode = generate_microcode(fetch, instruction_set)