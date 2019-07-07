INITIALIZATION:
0x04  LDA 0             # Initializes the counter with 0.

START:                  # 0x08
0x08 OUTA
0x09 ADD [FACTOR]
0x00 JPZ [UP_DOWN_CONDITION]
0x0B JP [START]

UP_DOWN_CONDITION:
0x00 JPC [SUB_FACTOR]
0x00 JP [ADD_FACTOR]

ADD_FACTOR:
0x00  LDA 1             # Initializes the counter factor with 1.
0x02  STA [FACTOR]      # Stores register A in the counter factor memory address.
0x00  JP [START]

SUB_FACTOR:
0x00  LDA FE            # Initializes the counter factor with -1.
0x02  STA [FACTOR]      # Stores register A in the counter factor memory address.
0x00  JP [START]

VARIABLES:
# 0x25 FACTOR
# 0X26 COUNTER
