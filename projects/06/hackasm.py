import sys
import os.path
import re
argv=sys.argv

class ASMParser(object):
    def __init__(self):
        self.symbolTable = {
                            'R0': '0',
                            'R1': '1',
                            'R2': '2',
                            'R3': '3',
                            'R4': '4',
                            'R5': '5',
                            'R6': '6',
                            'R7': '7',
                            'R8': '8',
                            'R9': '9',
                            'R10': '10',
                            'R11': '11',
                            'R12': '12',
                            'R13': '13',
                            'R14': '14',
                            'R15': '15'
                            }
    def parseLine(self, line):
        self.line = line.strip()
        if(self.line[0:2] != '//' and self.line != ''):
            if '//' in self.line:
                self.line = self.line[:self.line.find('//')].strip()
            if (self.line[0] == '('):
                self.key = self.line[1:self.line.find(')')]
                self.symbolTable[self.key] = 'null'
                return self.key + " " + self.symbolTable[self.key] + '\n'
            elif(self.line[0] == '@'):
                if(self.line[1].isdigit()):
                    return str(AInstruction(self.line[1:])) + '\n'
                else:
                    self.key = self.line[1:]
                    if self.key not in self.symbolTable:
                        self.symbolTable[self.key] = 'null'
                    elif self.symbolTable[self.key].isdigit():
                        return str(AInstruction(self.symbolTable[self.key])) + '\n'
                    return self.symbolTable[self.key] + '\n'
            else:
                self.op = 'null'
                self.dest = 'null'
                self.jump = 'null'
                
                if ';' in line and '=' in line:
                    self.op = re.split('[;=]',self.line)[1]
                else:
                    if ';' in line:
                        self.op, self.jump = self.line.rsplit(';',1)[-2:]
                    if '=' in line:
                        self.dest, self.op = self.line.split('=',1)[0:2]

                return str(CInstruction(self.op, self.dest, self.jump)) + '\n'
        else:
            return ''
            
class Instruction(object):
    def __str__(self):
        raise NotImplementedError
        
class AInstruction(Instruction):
    def __init__(self, address):
        self.address = address  
    def addressStr(self, decimalNum):
        return "{0:015b}".format(int(decimalNum))
    def __str__(self):
        return "0" + self.addressStr(self.address)
        
class CInstruction(Instruction):
    destTable = dict(
                null = "000",
                M = "001",
                D = "010",
                MD = "011",
                A = "100",
                AM = "101",
                AD = "110",
                AMD = "111"
                )
    jumpTable = dict(
                null = "000",
                JGT = "001",
                JEQ = "010",
                JGE = "011",
                JLT = "100",
                JNE = "101",
                JLE = "110",
                JMP = "111"
                )
    opTable =   {
                '0' : "0101010",
                '1' : "0111111",
                'D' : "0001100",
                'A' : "0110000",
                'M' : "1110000",
                '~D' : "0001101",
                '~A' : "0110001",
                '~M' : "1110001",
                '-D' : "0001111",
                '-A' : "0110011",
                '-M' : "1110011",
                'D+1' : "0011111",
                'A+1' : "0110111",
                'M+1' : "1110111",
                'D-1' : "0001110",
                'A-1' : "0110010",
                'M-1' : "1110010",
                'D+A' : "0000010",
                'D+M' : "1000010",
                'D-A' : "0010011",
                'D-M' : "1010011",
                'A-D' : "0000111",
                'M-D' : "1000111",
                'D&A' : "0000000",
                'D&M' : "1000000",
                'D|A' : "0010101",
                'D|M' : "1010101"
                }
                
    def __init__(self, operation, dest, jump):
        self.op = operation
        self.dest = dest
        self.jump = jump
    def opStr(self, op):
        if op in self.opTable.keys():
            return self.opTable[op]
        else:
            raise ValueError
    def destStr(self, dest):
        if dest in self.destTable.keys():
            return self.destTable[dest]
        else:
            raise ValueError
    def jumpStr(self, jump):
        if jump in self.jumpTable.keys():
            return self.jumpTable[jump]
        else:
            raise ValueError
    def __str__(self):
        return "111" + self.opStr(self.op) + \
                self.destStr(self.dest) + self.jumpStr(self.jump)
        
if __name__ == '__main__':
    if(len(argv) > 1):
        asmfile = argv[1]
        if('.asm' not in asmfile):
            asmfile += '.asm'
        print "Assembling {0}".format(asmfile)
        
        if os.path.exists(asmfile):
            parser = ASMParser()
            f = open(asmfile,'r')
            fout = open(asmfile.replace('.asm','.hack'),'w')
            for line in f:
                sys.stdout.write( parser.parseLine(line))
            
            fout.close()
            f.close()
        else:
            print "File doesn't exist"
    else:
        print "File not found"
        print "Usage: hackasm <file>"
        
