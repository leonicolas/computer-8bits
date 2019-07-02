# Saves the codes table in a ROM file.
# file_name:   the ROM file name
# codes_table: the code table to be saved into the ROM file
# instruction_size: the instruction size in bytes
# cols: the number of columns
def save_file(file_name, codes_table, instruction_size, cols = 8):
    file = open(file_name, "w+", encoding="utf-8")
    file.write("v2.0 raw\n")
    col = 0
    instruction_size = int(instruction_size / 4)
    for code in codes_table:
        col += 1
        instruction = "{:0x}".format(code).rjust(instruction_size, "0")
        file.write("{} ".format(instruction))
        if(col > cols - 1):
            col = 0
            file.write("\n")
    file.close()
