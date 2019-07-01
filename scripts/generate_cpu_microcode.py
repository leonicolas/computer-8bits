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

def cast_array(value):
    return value if isinstance(value, list) else [value]

def create_instruction(instruction_metadata, af, cf, zf, initial_step):
    step = initial_step
    instruction_steps = list()
    # Loop over flags
    for flag in cast_array(instruction_metadata['flags']):
        instruction = {
            'address': instruction_metadata['op_code'] << 6 
                | af << 5 
                | cf << 4 
                | zf << 3 
                | step,
            'flag': flag 
        }
        instruction_steps.append(instruction)
        print("{:010b}".format(instruction['address']) + " - " + 
              "{:04x}".format(instruction['flag']))
        step += 1
    return instruction_steps

def generate_microcode(fetch, instruction_set):
    microcode = list()

    # Loop over the instructions
    for instruction_name in instruction_set:
        instruction_microcode = list(fetch)
        instruction_metadata = instruction_set[instruction_name]
        step = len(fetch) - 1

        instruction_steps = [ create_instruction(instruction_metadata, af, cf, zf, step)
            # Loop over the address flag
            for af in cast_array(instruction_metadata['af'])
            # Loop over the carry flag
            for cf in cast_array(instruction_metadata['cf'])
            # Loop over the zero flag
            for zf in cast_array(instruction_metadata['zf'])
        ]

        instruction_microcode.append(instruction_steps)
        step += 1

microcode = generate_microcode(fetch, instruction_set)