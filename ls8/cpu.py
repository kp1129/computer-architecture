"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        # 256 bytes of memory
        self.ram = [0] * 256
        # 8 general purpose registers
        self.reg = [0] * 8
        # instruction register
        # copy of the currently executing instruction
        self.ir = self.reg[3]
        # program counter
        # address of the currently executing instruction
        self.pc = self.reg[4]

        self.interrupt_mask = self.reg[5]
        self.interrupt_status = self.reg[6]
        self.stack_pointer = self.reg[7]

    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        program = [
            # From print8.ls8
            0b10000010, # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111, # PRN R0
            0b00000000,
            0b00000001, # HLT
        ]

        for instruction in program:
            self.ram[address] = instruction
            address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        # read the memory address in pc and store it in ir
        hlt = 0b00000001
        ldi = 0b10000010
        prn = 0b01000111
        self.ir = self.pc
        operand_a = self.ram_read(self.ram[self.pc + 1])
        operand_b = self.ram_read(self.ram[self.pc + 2])

        running = True
        while running:
            if self.ir == ldi:
                operand_a = operand_b
                self.pc += 3
            elif self.ir == prn:
                print(operand_a)
                self.pc += 2
            elif self.ir == hlt:
                running = False
                self.pc += 1    

    def ram_read(self, ix):
        return self.ram[ix]
    
    def ram_write(self, val, ix):
        self.ram[ix] = val
        return val


