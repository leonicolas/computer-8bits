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
    {   'name': 'nop',
        'op_code': 0x00, 'cf': [0, 1], 'zf': [0, 1],
        'flags': fetch + fin_inst
    },
    {   'name': 'halt',
        'op_code': 0x01, 'cf': [0, 1], 'zf': [0, 1],
        'flags': fetch + [ 0x8000 ] + fin_inst
    },
    {   'name': 'lda_num',
        'op_code': 0x02, 'cf': [0, 1], 'zf': [0, 1],
        'flags': fetch + [ 0x010C, 0x4040 ] + fin_inst
    },
    {   'name': 'lda_paddr',
        'op_code': 0x03, 'cf': [0, 1], 'zf': [0, 1],
        'flags': fetch + [ 0x010C, 0x0140, 0x4040 ] + fin_inst
    },
    {   'name': 'sta_paddr',
        'op_code': 0x04, 'cf': [0, 1], 'zf': [0, 1],
        'flags': fetch + [ 0x010C, 0x0140, 0x2080 ] + fin_inst
    },
    {   'name': 'ldb_num',
        'op_code': 0x05, 'cf': [0, 1], 'zf': [0, 1],
        'flags': fetch + [ 0x010C, 0x0440 ] + fin_inst
    },
    {   'name': 'ldb_paddr',
        'op_code': 0x06, 'cf': [0, 1], 'zf': [0, 1],
        'flags': fetch + [ 0x010C, 0x0140, 0x0440 ] + fin_inst
    },
    {   'name': 'stb_paddr',
        'op_code': 0x07, 'cf': [0, 1], 'zf': [0, 1],
        'flags': fetch + [ 0x010C, 0x0140, 0x0280 ] + fin_inst
    },
    {   'name': 'add_num',
        'op_code': 0x08, 'cf': [0, 1], 'zf': [0, 1],
        'flags': fetch + [ 0x010C, 0x0440, 0x5000 ] + fin_inst
    },
    {   'name': 'add_paddr',
        'op_code': 0x09, 'cf': [0, 1], 'zf': [0, 1],
        'flags': fetch + [ 0x010C, 0x0140, 0x0440, 0x5000 ] + fin_inst
    },
    {   'name': 'sub_num',
        'op_code': 0x0A, 'cf': [0, 1], 'zf': [0, 1],
        'flags': fetch + [ 0x010C, 0x0C40, 0x5800 ] + fin_inst
    },
    {   'name': 'sub_paddr',
        'op_code': 0x0B, 'cf': [0, 1], 'zf': [0, 1],
        'flags': fetch + [ 0x010C, 0x0140, 0x0C40, 0x5800 ] + fin_inst
    },
    {   'name': 'outa',
        'op_code': 0x0C, 'cf': [0, 1], 'zf': [0, 1],
        'flags': fetch + [ 0x2001 ] + fin_inst
    },
    {   'name': 'outb',
        'op_code': 0x0D, 'cf': [0, 1], 'zf': [0, 1],
        'flags': fetch + [ 0x0201 ] + fin_inst
    },
    {   'name': 'out_num',
        'op_code': 0x0E, 'cf': [0, 1], 'zf': [0, 1],
        'flags': fetch + [ 0x010C, 0x0041 ] + fin_inst
    },
    {   'name': 'out_paddr',
        'op_code': 0x0F, 'cf': [0, 1], 'zf': [0, 1],
        'flags': fetch + [ 0x010C, 0x0140, 0x0041 ] + fin_inst
    },
    {   'name': 'jp_addr',
        'op_code': 0x10, 'cf': [0, 1], 'zf': [0, 1],
        'flags': fetch + [ 0x010C, 0x0042 ] + fin_inst
    },
    {   'name': 'jp_paddr',
        'op_code': 0x11, 'cf': [0, 1], 'zf': [0, 1],
        'flags': fetch + [ 0x010C, 0x0140, 0x0042 ] + fin_inst
    },
    {   'name': 'jpz_addr',
        'op_code': 0x12, 'cf': [0, 1], 'zf': 1,
        'flags': fetch + [ 0x010C, 0x0042 ] + fin_inst
    },
    {   'name': 'jpz_paddr',
        'op_code': 0x13, 'cf': [0, 1], 'zf': 1,
        'flags': fetch + [ 0x010C, 0x0140, 0x0042 ] + fin_inst
    },
    {   'name': 'jpc_addr',
        'op_code': 0x14, 'cf': 1, 'zf': [0, 1],
        'flags': fetch + [ 0x010C, 0x0042 ] + fin_inst
    },
    {   'name': 'jpc_paddr',
        'op_code': 0x15, 'cf': 1, 'zf': [0, 1],
        'flags': fetch + [ 0x010C, 0x0140, 0x0042 ] + fin_inst
    },
]

# Converts a value to an array if the value is not an array yet.
def cast_array(value):
    return value if isinstance(value, list) else [value]

# Print the microcode
def print_microcode(microcode):
    for instruction in microcode:
        op_code = instruction['address'] >> 5
        cf = (instruction['address'] & 0x10) >> 4
        zf = (instruction['address'] & 0x08) >> 3
        step = instruction['address'] & 0x07
        print("{} - 0x{:04x} - {:05b} {:01b} {:01b} {:03b} - {:04x}".format(
            instruction['name'].ljust(10),
            instruction['address'],
            op_code, cf, zf, step,
            instruction['flag']))

# Transforms an array of arrays in an single array.
def flat_array(data):
    return [value for internal_data in data for value in internal_data]


def create_instruction_microcode(instruction, cf, zf):
    step = 0
    instruction_steps = list()
    # Loop over flags
    for flag in cast_array(instruction['flags']):
        instruction_microcode = {
            'name': instruction['name'],
            'address': instruction['op_code'] << 5
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
        instruction_steps = [ create_instruction_microcode(instruction, cf, zf)
            # Loop over the carry flag
            for cf in cast_array(instruction['cf'])
            # Loop over the zero flag
            for zf in cast_array(instruction['zf'])
        ]

        microcode += flat_array(instruction_steps)

    return microcode

# Fills the microcode missing addresses with NOP (no operation)
def fill_microcode_paddresses(microcode):
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
microcode = fill_microcode_paddresses(microcode)
if verbose:
    print_microcode(microcode)

# Saves the code table in a ROM file.
instruction_size = 16 # bytes
save_rom.save_file(
    file_name,
    [instruction_step["flag"] for instruction_step in microcode],
    instruction_size)

