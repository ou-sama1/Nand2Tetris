from enum import Enum
import sys

mapDestinationToBin = {
    'D': 0b010,
    'M': 0b001,
    'A': 0b100
}
mapComputationToBin = {
    '0': 0b101010,
    '1': 0b111111,
    '-1': 0b111010,
    'D': 0b001100,
    'X': 0b110000,
    '!D': 0b001101,
    '!X': 0b110001,
    '-D': 0b001111,
    '-X': 0b110011,
    'D+1': 0b011111,
    'X+1': 0b110111,
    'D-1': 0b001110,
    'X-1': 0b110010,
    'D+X': 0b000010,
    'D-X': 0b010011,
    'X-D': 0b000111,
    'D&X': 0b000000,
    'D|X': 0b010101
}
mapJumpToBin = {
    'JGT': 0b001,
    'JEQ': 0b010,
    'JGE': 0b011,
    'JLT': 0b100,
    'JNE': 0b101,
    'JLE': 0b110,
    'JMP': 0b111
}

predefinedAddresses = {
    **{f"R{i}": i for i in range(16)},
    "SP": 0,
    "LCL": 1,
    "ARG": 2,
    "THIS": 3,
    "THAT": 4,
    "SCREEN": 32640,
    "KBD": 32767
}

# Line type enum
class LineType(Enum):
    A_INSTRUCTION = 1
    C_INSTRUCTION = 2

# Token type enum
class TokenType(Enum):
    ADDRESS = 1
    DEST = 2
    COMP = 3
    JMP = 4

# Token binary length enum
class TokenBinLength(Enum):
    ADDRESS = 16
    DEST = 3
    COMP = 6
    JMP = 3

# Token max size enum
class TokenMaxSize(Enum):
    ADDRESS = 32767

# Convert decimal to binary
def convertDecimalToBin(decimalNumber, pad):
    return format(decimalNumber, f"0{pad.value}b")

# Convert decimal to hexadecimal
def convertDecimalToHex(decimalNumber, pad=4):
    return format(decimalNumber, f"0{pad}X")

# Strip whitespaces and commpents from a line
def cleanLine(line):
    line = line.split('//')[0]
    
    return "".join(line.split())

def code(token, tokenType):
    if tokenType == TokenType.ADDRESS:
        if int(token) < 0 or int(token) > TokenMaxSize.ADDRESS.value:
            raise Exception(f"Invalid address {token} !")
        
        return convertDecimalToBin(
                int(token),
                TokenBinLength.ADDRESS
            )

    if tokenType == TokenType.DEST:
        availableDestinations = list(mapDestinationToBin.keys())
        dest = 0b0
        
        for char in list(token):
            if char not in availableDestinations:
                raise Exception('Wrong destination format !')

            dest |= mapDestinationToBin.get(char)
            availableDestinations.remove(char)

        return convertDecimalToBin(
                int(dest),
                TokenBinLength.DEST
            )

    if tokenType == TokenType.COMP:
        a = '0'

        if 'M' in token:
            a = '1'
            
        token = token.replace('A', 'X').replace('M', 'X')
        
        if token not in mapComputationToBin.keys():
            raise Exception('Wrong computation format !')

        comp = mapComputationToBin.get(token)

        return a + convertDecimalToBin(comp, TokenBinLength.COMP)

    if tokenType == TokenType.JMP:
        if token and token not in mapJumpToBin.keys():
            raise Exception('Wrong jump format !')

        jmp = mapJumpToBin.get(token, 0)

        return convertDecimalToBin(
                int(jmp),
                TokenBinLength.JMP
            )
    
    raise Exception('Wrong token format !') 

# Parser
def parse(line):
    parsed = {
        'lineType': '',
        'address': '',
        'dest': '',
        'comp': '',
        'jmp': ''
    }

    if line.startswith('@'):
        parsed['lineType'] = LineType.A_INSTRUCTION
        parsed['address'] = line[1:]
    
        return parsed

    parsed['lineType'] = LineType.C_INSTRUCTION

    if '=' in line:
        parsed['dest'] = line.split('=')[0]
        parsed['comp'] = line.split('=')[1]
        line = line.split('=')[1]

    if ';' in line:
        parsed['comp'] = line.split(';')[0]
        line = line.split(';')[1]

        if line:
            parsed['jmp'] = line

    return parsed

# Store all labels in first pass
def firstPass(in_file):
    with open (in_file, "r", encoding="utf-8") as inFile:
        address = 0
        
        for line in inFile:
            line = cleanLine(line)

            if not line:
                continue

            if line.startswith('(') and line.endswith(')'):
                label = line[1:-1]
  
                if not label:
                    raise ValueError("Empty label () is invalid")
                
                if label in predefinedAddresses.keys():
                    raise ValueError(f"Label redefined: {label}")
                
                predefinedAddresses[label] = address
 
            else:
                address += 1
            
            
def secondPass(in_file, out_file):
    with open (in_file, "r", encoding="utf-8") as inFile, open (out_file, "w", encoding="utf-8") as outFile:
        # File header
        outFile.write("v2.0 raw" + '\n')
        
        next_var = 16

        for line in inFile:
            line = cleanLine(line)

            if not line or line.startswith('(') and line.endswith(')'):
                continue

            parsed = parse(line)
            instruction = 0b0
                
            # Parse A instruction
            if parsed['lineType'] == LineType.A_INSTRUCTION:
                address = parsed['address']
                    
                if not address.isdigit():
                    if address not in predefinedAddresses.keys():
                        predefinedAddresses[address] = next_var
                        next_var += 1
                            
                    address = predefinedAddresses[address]
                        
                instruction = code(address, TokenType.ADDRESS)

            # Parse C instruction
            elif parsed['lineType'] == LineType.C_INSTRUCTION:
                prefix = '111'
                comp = code(parsed['comp'], TokenType.COMP)
                dest = code(parsed['dest'], TokenType.DEST)
                jmp = code(parsed['jmp'], TokenType.JMP)
                instruction = prefix + comp + dest + jmp
            else:
                raise Exception('Unknown instruction type !')

            outFile.write(convertDecimalToHex(int(instruction, 2)) + ' ')


if __name__ == "__main__":
    if len(sys.argv) == 3:
        in_file = sys.argv[1]
        out_file = sys.argv[2]
    else:
        in_file = "symbols.asm"
        out_file = "code.bin"
        
    firstPass(in_file)
    secondPass(in_file, out_file)
    
    print(f"Assembled {in_file} -> {out_file}")
    




