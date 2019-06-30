def save_file(file_name, codes_table, cols = 8):
    file = open(file_name, "w+", encoding="utf-8")
    file.write("v2.0 raw\n")
    col = 0
    for code in codes_table:
        col += 1
        file.write("{:06x}".format(code))
        file.write(" ")
        if(col > cols - 1):
            col = 0
            file.write("\n")
    file.close()
