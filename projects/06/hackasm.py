import sys
argv=sys.argv

class Instruction(object):
    def __str__(self):
        raise NotImplementedError
        
class AInstruction(Instruction):
    def __init__(self, address):
        self.address = address  
    def addressStr(self, decimalNum):
        return "{0:015b}".format(decimalNum)
    def __str__(self):
        return "0" + self.addressStr(self.address)
        
class CInstruction(Instruction):
    def __init__(self, operation, dest, jump):
        self.op = operation
        self.dest = dest
        self.jump = jump
    def __str__(self):
        return "111" + self.opStr(self.op) + \
                self.destStr(self.dest) + self.jumpStr(self.jump)
        
if __name__ == '__main__':
    if(len(argv) > 1):
        asmfile = argv[1]
        if('.asm' not in asmfile):
            asmfile += '.asm'
        print "Assembling {0}".format(asmfile)
    else:
        print "File not found"
        print "Usage: hackasm <file>"
        