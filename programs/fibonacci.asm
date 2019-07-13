INIT:                   # 0x00
0x00  LDA 0             # Initializes the number 1 loading it in register A.
0x02  STA [NUM1]        # Stores register A in the number 1 memory address.
0x04  OUT [NUM1]        # Output the number 1.

0x06  LDA 1             # Initializes the number 2 loading it in register A.
0x08  STA [NUM2]        # Stores register A in the number 2 memory address.

START:                  # 0x0A
0x0A  OUT [NUM2]        # Output the number 2.
0x0C  LDA [NUM1]        # Loads the number 1 in register A.
0x0E  ADD [NUM2]        # Adds the number 2.
0x10  STB [NUM1]        # Stores number 2 in number 1.
0x12  STA [NUM2]        # Stores the sum of number 1 and 2 in number 2.

0x14  JPC [INIT]        # Jump on carry (restart).
0x16  JP  [START]       # Jumps to start.

# VARIABLES:
# 0x18  NUM1
# 0x19  NUM2
