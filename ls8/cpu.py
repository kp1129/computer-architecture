"""CPU functionality."""

# import sys

# # grab file name from sys.argv
# file_name = sys.argv[1]
# print(file_name)

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        # 256 bytes of memory
        self.ram = [0] * 256
        # 8 general purpose registers
        self.reg = [0] * 8
        # program counter
        # address of the currently executing instruction
        # starts with 0
        self.pc = 0
        # reserved registers
        self.interrupt_mask = self.reg[5]
        self.interrupt_status = self.reg[6]
        # stack pointer
        self.reg[7] = 0xF4
        # self.stack_pointer = self.reg[7]

    def load(self, file_name):
        """Load a program into memory."""

        address = 0

        with open(file_name) as file:
            for line in file:
                clean_line = line.split("#")[0].strip()

                if clean_line == "":
                    continue
                else:
                    command = int(clean_line, 2)
                    self.ram_write(command, address)
                    # print('saved command ', self.ram[address], 'at ', address)
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
        HLT = 0b00000001
        LDI = 0b10000010
        PRN = 0b01000111
        MUL = 0b10100010
        PSH = 0b01000101 #push
        POP = 0b01000110 
        CLL = 0b01010000 #call
        RET = 0b00010001 #return
        ADD = 0b10100000

        running = True
        while running:
            # ir, operand_a, and operand_b have to reset on each iteration
            # read the memory address in pc and store it in ir
            ir = self.ram[self.pc]
            # arguments a and b
            operand_a = self.ram[self.pc + 1]
            operand_b = self.ram[self.pc + 2]

            if ir == LDI:
                self.reg[operand_a] = operand_b
 
            elif ir == PRN:
                print(self.reg[operand_a])
   
            elif ir == HLT:
                running = False

            elif ir == MUL:
                a = self.reg[operand_a]
                b = self.reg[operand_b]
                self.reg[operand_a] = a * b

            elif ir == PSH:
                self.reg[7] -= 1
                val = self.reg[operand_a]
                ix = self.reg[7]
                self.ram[ix] = val   

            elif ir == POP:
                sp = self.reg[7]
                value = self.ram[sp]
                self.reg[operand_a] = value
                self.reg[7] += 1

            elif ir == CLL:
                # print('memory rn: ', self.ram)
                # print('what is in register 1? ', self.reg[1])
                reg = operand_a
                address = self.reg[reg]
                return_address = self.pc + 2
                # decrement stack pointer
                self.reg[7] -= 1
                sp = self.reg[7]
                # put return address on the stack
                self.ram[sp] = return_address

                # go to the function
                self.pc = address

            elif ir == RET:
                # pop the return address off the stack
                sp = self.reg[7]
                return_address = self.ram[sp]
                self.reg[7] += 1
                # go to return address
                self.pc = return_address

            elif ir == ADD:
                a = self.reg[operand_a]
                b = self.reg[operand_b]
                self.reg[operand_a] = a + b


            if ir != RET and ir != CLL: 
                # increment the program counter based on
                # how many arguments this command includes:
                # take the command, right-shift 6 places, 
                # and add the resulting 0, 1, or 2 to the 
                # one-point increment
                self.pc += 1 + (ir >> 6)    

    def ram_read(self, ix):
        return self.ram[ix]
    
    def ram_write(self, val, ix):
        self.ram[ix] = val

