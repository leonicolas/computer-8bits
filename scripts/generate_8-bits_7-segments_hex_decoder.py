#!python3
# This script generates the hex table used to decode 
# an 8-bits number to show it in a 7-segment display
# in base 10 (0 to 255).
# The hex table is write into a ROM chip in our 
# decoder circuit.

import save_rom
import sys

def generate_codes():
    # Codes for 0 to 9 decode - segments bits order g, f, e, d, c, b, a.
    decimal_codes = [0x3f, 0x06, 0x5b, 0x4f, 0x66, 0x6d, 0x7d, 0x07, 0x7f, 0x6f]

    # Ones (0 to 9)
    codes_table = list(decimal_codes)

    # Tens (10 to 99)
    tens_table = list()
    for num in range(0, 10):
        tens = decimal_codes[num]

        for code in decimal_codes:
            tens_code = (tens << 7) | code
            tens_table.append(tens_code)
            if(num > 0):
                codes_table.append(tens_code)

    # Hundreds (100 to 255)
    for num in range(1, 3):
        hundreds = decimal_codes[num]
        tens_num = 0

        for tens_code in tens_table:
            codes_table.append((hundreds << 14) | tens_code)
            if(num == 2 and tens_num >= 55):
                break
            tens_num += 1

    return codes_table

# Validates the filename parameter.
if(len(sys.argv) <= 1):
    print "Invalid file name."
    exit 1

# Gets the file name.
file_name = sys.argv[1]

# Generates the codes table.
codes_table = generate_codes()

# Saves the code table in a ROM file.
instruction_size = 24 # bytes
save_rom.save_file(file_name, codes_table, instruction_size)
