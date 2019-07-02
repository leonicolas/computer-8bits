#!python3

import save_rom
import sys

# Fetch steps. Used for all instructions.
fetch = [0x0104, 0x0068]

# Finalizes the instruction execution.
fin_inst = [0x0010]

# The instruction set.
# op_code = operation code.
# af = address flag. When 1 indicates that the instruction argument is an address, otherwise 0.
# cf = carry flag.
# zf = zero flag.
instruction_set = [
    {   'name': 'halt', 
        'op_code': 0x0, 'af': [0, 1], 'cf': [0, 1], 'zf': [0, 1],
        'flags': fetch + [ 0x8000 ] + fin_inst
    },
    {   'name': 'lda_num',
        'op_code': 0x1, 'af': 0, 'cf': [0, 1], 'zf': [0, 1],
        'flags': fetch + [ 0x010C, 0x4040 ] + fin_inst
    },
    {   'name': 'lda_addr',
        'op_code': 0x1, 'af': 1, 'cf': [0, 1], 'zf': [0, 1],
        'flags': fetch + [ 0x010C, 0x0140, 0x4040 ] + fin_inst
    },
    {   'name': 'sta_addr',
        'op_code': 0x2, 'af': [0, 1], 'cf': [0, 1], 'zf': [0, 1],
        'flags': fetch + [ 0x010C, 0x0140, 0x2080 ] + fin_inst
    },
    {   'name': 'ldb_num',
        'op_code': 0x3, 'af': 0, 'cf': [0, 1], 'zf': [0, 1],
        'flags': fetch + [ 0x010C, 0x0440 ] + fin_inst
    },
    {   'name': 'ldb_addr',
        'op_code': 0x3, 'af': 1, 'cf': [0, 1], 'zf': [0, 1],
        'flags': fetch + [ 0x010C, 0x0140, 0x0440 ] + fin_inst
    },
    {   'name': 'stb_addr',
        'op_code': 0x4, 'af': [0, 1], 'cf': [0, 1], 'zf': [0, 1],
        'flags': fetch + [ 0x010C, 0x0140, 0x0280 ] + fin_inst
    },
]

# Converts a value to an array if the value is not an array yet.
def cast_array(value):
    return value if isinstance(value, list) else [value]

# Print the microcode
def print_microcode(microcode):
    for instruction in microcode:
        op_code = instruction['address'] >> 6 
        af = (instruction['address'] & 0x20) >> 5
        cf = (instruction['address'] & 0x10) >> 4
        zf = (instruction['address'] & 0x08) >> 3
        step = instruction['address'] & 0x07
        print("{} - 0x{:04x} - {:04b} {:01b} {:01b} {:01b} {:03b} - {:04x}".format(
            instruction['name'].ljust(10),
            instruction['address'],
            op_code, af, cf, zf, step, 
            instruction['flag'])) 

# Transforms an array of arrays in an single array.
def flat_array(data):
    return [value for internal_data in data for value in internal_data]


def create_instruction_microcode(instruction, af, cf, zf):
    step = 0
    instruction_steps = list()
    # Loop over flags
    for flag in cast_array(instruction['flags']):
        instruction_microcode = {
            'name': instruction['name'],
            'address': instruction['op_code'] << 6 
                | af << 5 
                | cf << 4 
                | zf << 3 
                | step,
            'flag': flag 
        }
        instruction_steps.append(instruction_microcode)
        step += 1

    return instruction_steps

# Generates the processor microcode based on the given instruction set
def generate_microcode(fetch, instruction_set):
    microcode = list()

    # Loop over the instructions
    for instruction in instruction_set:
        instruction_steps = [ create_instruction_microcode(instruction, af, cf, zf)
            # Loop over the address flag
            for af in cast_array(instruction['af'])
            # Loop over the carry flag
            for cf in cast_array(instruction['cf'])
            # Loop over the zero flag
            for zf in cast_array(instruction['zf'])
        ]

        microcode += flat_array(instruction_steps)
    
    return microcode

# Fills the microcode missing addresses with NOP (no operation)
def fill_microcode_addresses(microcode):
    address = 0
    filled_microcode = list()

    # Loop over the microcode steps and complete the missing addresses.
    for instruction_step in microcode:
        while address < instruction_step['address']:
            filled_microcode.append({
                'name': 'nop',
                'address': address,
                'flag': 0
            })
            address += 1
        filled_microcode.append(instruction_step)
        address += 1

    return filled_microcode

# Validates the arguments.
arguments_num = len(sys.argv)
if(arguments_num <= 1 or arguments_num > 3):
    print(" Invalid arguments.\n Ex.: generate_cpu_microcode.py [-v] your_filename.rom")
    print("   -v   Verbose mode (optional)\n")
    exit(1)

# Gets the arguments values.
verbose = (arguments_num == 3 and sys.argv[1] == '-v')
file_name = sys.argv[2 if arguments_num == 3 else 1]

# Generates the codes table.
microcode = generate_microcode(fetch, instruction_set)
microcode = fill_microcode_addresses(microcode)
if verbose:
    print_microcode(microcode)

# Saves the code table in a ROM file.
instruction_size = 16 # bytes
save_rom.save_file(
    file_name, 
    [instruction_step["flag"] for instruction_step in microcode], 
    instruction_size)

