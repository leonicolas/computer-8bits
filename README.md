# Basic 8-bits computer simulation

A basic 8-bits computer created with [LogiSim](http://www.cburch.com/logisim/pt/index.html) digital circuit simulator.

- [Basic 8-bits computer simulation](#basic-8-bits-computer-simulation)
  - [Project goal](#project-goal)
  - [Acknowledgments](#acknowledgments)
  - [The current processor version](#the-current-processor-version)
  - [The BUS](#the-bus)
  - [The full adder](#the-full-adder)
  - [The 8-bits Arithmetic and Logic Unit (ALU)](#the-8-bits-arithmetic-and-logic-unit-alu)
  - [The 4-bits address decoder](#the-4-bits-address-decoder)
  - [The 8-bits registers](#the-8-bits-registers)
  - [The RAM](#the-ram)
    - [The DRAM and SRAM](#the-dram-and-sram)
    - [The 16 bytes SRAM](#the-16-bytes-sram)
    - [The 256 bytes SRAM](#the-256-bytes-sram)
  - [The program counter (PC)](#the-program-counter-pc)
 
## Project goal

This project goal is to build a basic 8-bits computer with a functional 8-bits processor using a digital circuit simulator (LogiSim).

For future versions I will expand the circuits modules and functionalities creating a more complex processor, but for now, I'm trying to keep the circuits as simple as possible.

## Acknowledgments

`Ben Eater` and his [YouTube channel](https://www.youtube.com/user/eaterbc) with great videos explaining about a processor architecture.

## The current processor version

This is the current processor circuit version. It's not complete yet, but it's quite cool, isn't?.

![The processor](images/processor.png)

Is there anything missing? Yes, I know, the ~~program counter (PC)~~, instructions decoder, the ~~RAM memory~~, etc. I'll put these modules into the processor in the next versions.

## The BUS

The BUS is used to connect all processor modules allowing the components to communicate with each other.

Normally there is more than 1 bus in a processor, like the data BUS, address BUS, control BUS, etc. For the first processor version I'm using only 2 BUS, one for data and one for control.

The data bus:

![The data bus](images/data_bus.png)

## The full adder

This is the circuit responsible for sum two numbers. It's a important ALU piece.

![The full adder](images/full_adder.png)

## The 8-bits Arithmetic and Logic Unit (ALU)

The ALU executes the arithmetic (sum, subtract, multiplication, division) and logic (and, or, xor, not, comparison) operations inside the processor. In my processor, the ALU is directly connected to the registers A and B to use them as source to perform the operations.

For this first processor version, I will only implement the sum and subtraction operations, reserving the other operations for a future version.

![The ALU](images/alu_8-bits.png)

## The 4-bits address decoder

The address decoder is responsable for decode one binary address to a binary signal (1-bit). For each address the circuit will activated one different ouput.

This circuit decodes each of the 4-bits address to a different output signal in a total of 16 ouputs. 

![The 4-bits addres decoder](images/address_decoder_4-bits.png)

## The 8-bits registers

A register is a processor piece that is responsible for storing information. In our case, the 8-bits register will store an 8-bits number.

The register works using a D flip-flop for store a bit. Each 8-bits register uses 8 D flip-flop for store a byte (8-bits).

This processor will use 5 registers: 

1) Program counter register (PC)
2) Register A connected to the ALU
3) Register B connected to the ALU
4) Instruction register
5) Memory address register

The RAM memory used in this computer also uses the 8-bits registry.

This is the internal 8-bits register circuit:

![The 8-bits register circuit](images/register_8-bits.png)

## The RAM

The RAM (Random Access Memory) is responsable for store values with 8-bits each (word size). This values will include the program binary and the program variables.

### The DRAM and SRAM

There are different types of RAM. Dynamic RAM (DRAM) and Static RAM (SRAM) are usually found in our computers. 

DRAM is a memory based on capacitors, with less components compared with the SRAM memory, but with the necessity to refresh the capacitors many times per second for avoid data loss. 

SRAM is based on D flip-flop registers generating a more complex circuit to store a bit, but with no refresh circuits.

This project is using SRAM memory type for the RAM circuit.


### The 16 bytes SRAM

The 16 bytes SRAM uses 16 registers to store 1 byte each and a 4-bits length address to access the memory data.

![The 16 bytes SRAM](images/SRAM_16-bytes.png)

### The 256 bytes SRAM

This computer uses a 256 bytes SRAM memory composed by 16 SRAM modules with 16 bytes each (16 x 16 bytes = 256 bytes).

The image bellow is the 256 bytes SRAM memory circuit. For only 256 bytes we have this crazy complexity, remembering that each one of the 16 SRAM shown in the circuit is a [16 bytes SRAM](#the-16-bytes-sram), imagine a 16GB RAM memory! Wow! :flushed:

![The 256 bytes SRAM](images/SRAM_256-bytes.png)

## The program counter (PC)
 