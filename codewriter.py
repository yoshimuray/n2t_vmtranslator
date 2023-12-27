import io
import vmcommandtype

class CodeWriter:

    _symbols = {
        'local': 'LCL',
        'argument': 'ARG',
        'this': 'THIS',
        'that': 'THAT'
    }
    _mapping = {
        'pointer': 3,
        'temp': 5
    }

    def __init__(self, f: io.TextIOWrapper) -> None:
        self.f = f
        self.labelcnt = 0
        self.callcnt = 0

    def writeInit(self) -> None:
        lines = [
            '@256\n',
            'D=A\n',
            '@SP\n',
            'M=D\n',
        ]
        self.f.writelines(lines)
        self.writeCall('Sys.init', 0)


    def setFileName(self, fileName: str) -> None:
        self.finame = fileName

    def writeArithmetic(self, command: str) -> None:
        lines = []
        match command:
            case 'add':
                lines = [
                    '@SP\n',
                    'AM=M-1\n',
                    'D=M\n',
                    '@SP\n',
                    'AM=M-1\n',
                    'M=D+M\n',
                    '@SP\n',
                    'M=M+1\n'
                ]
            case 'sub':
                lines = [
                    '@SP\n',
                    'AM=M-1\n',
                    'D=M\n',
                    '@SP\n',
                    'AM=M-1\n',
                    'M=M-D\n',
                    '@SP\n',
                    'M=M+1\n'
                ]
            case 'neg':
                lines = [
                    '@SP\n',
                    'AM=M-1\n',
                    'M=-M\n',
                    '@SP\n',
                    'M=M+1\n'
                ]
            case 'eq':
                lines = [
                    '@SP\n',
                    'AM=M-1\n',
                    'D=M\n',
                    '@SP\n'
                    'AM=M-1\n',
                    'D=M-D\n',
                    '@_ARITH' + str(self.labelcnt) + '\n',
                    'D;JEQ\n',
                    'D=0\n',
                    '@_ARITH' + str(self.labelcnt + 1) + '\n',
                    '0;JMP\n',
                    '(_ARITH' + str(self.labelcnt) + ')\n',
                    'D=-1\n',
                    '(_ARITH' + str(self.labelcnt + 1) + ')\n',
                    '@SP\n',
                    'A=M\n',
                    'M=D\n',
                    '@SP\n',
                    'M=M+1\n'
                ]
                self.labelcnt += 2
            case 'gt':
                lines = [
                    '@SP\n',
                    'AM=M-1\n',
                    'D=M\n',
                    '@SP\n'
                    'AM=M-1\n',
                    'D=M-D\n',
                    '@_ARITH' + str(self.labelcnt) + '\n',
                    'D;JGT\n',
                    'D=0\n',
                    '@_ARITH' + str(self.labelcnt + 1) + '\n',
                    '0;JMP\n',
                    '(_ARITH' + str(self.labelcnt) + ')\n',
                    'D=-1\n',
                    '(_ARITH' + str(self.labelcnt + 1) + ')\n',
                    '@SP\n',
                    'A=M\n',
                    'M=D\n',
                    '@SP\n',
                    'M=M+1\n'
                ]
                self.labelcnt += 2
            case 'lt':
                lines = [
                    '@SP\n',
                    'AM=M-1\n',
                    'D=M\n',
                    '@SP\n'
                    'AM=M-1\n',
                    'D=M-D\n',
                    '@_ARITH' + str(self.labelcnt) + '\n',
                    'D;JLT\n',
                    'D=0\n',
                    '@_ARITH' + str(self.labelcnt + 1) + '\n',
                    '0;JMP\n',
                    '(_ARITH' + str(self.labelcnt) + ')\n',
                    'D=-1\n',
                    '(_ARITH' + str(self.labelcnt + 1) + ')\n',
                    '@SP\n',
                    'A=M\n',
                    'M=D\n',
                    '@SP\n',
                    'M=M+1\n'
                ]
                self.labelcnt += 2
            case 'and':
                lines = [
                    '@SP\n',
                    'AM=M-1\n',
                    'D=M\n',
                    '@SP\n',
                    'AM=M-1\n',
                    'M=D&M\n',
                    '@SP\n',
                    'M=M+1\n'
                ]
            case 'or':
                lines = [
                    '@SP\n',
                    'AM=M-1\n',
                    'D=M\n',
                    '@SP\n',
                    'AM=M-1\n',
                    'M=D|M\n',
                    '@SP\n',
                    'M=M+1\n'
                ]
            case 'not':
                lines = [
                    '@SP\n',
                    'AM=M-1\n',
                    'M=!M\n',
                    '@SP\n',
                    'M=M+1\n'
                ]
        self.f.writelines(lines)

    def writePushPop(self, command: vmcommandtype.VMCommandType, segment: str, index: int) -> None:
        lines = []
        match command:
            case vmcommandtype.C_PUSH:
                match segment:
                    case 'constant':
                        lines = [
                            '@' + str(index) + '\n',
                            'D=A\n',
                            '@SP\n',
                            'A=M\n',
                            'M=D\n',
                            '@SP\n',
                            'M=M+1\n'
                        ]
                    case 'local' | 'argument' | 'this' | 'that':
                        symbol = self._symbols[segment]
                        lines = [
                            '@' + symbol + '\n',
                            'D=M\n',
                            '@' + str(index) + '\n',
                            'A=D+A\n',
                            'D=M\n',
                            '@SP\n',
                            'A=M\n',
                            'M=D\n',
                            '@SP\n',
                            'M=M+1\n'
                        ]
                    case 'pointer' | 'temp':
                        addr = str(self._mapping[segment] + index)
                        lines = [
                            '@' + addr + '\n',
                            'D=M\n',
                            '@SP\n',
                            'A=M\n',
                            'M=D\n',
                            '@SP\n',
                            'M=M+1\n'
                        ]
                    case 'static':
                        lines = [
                            '@' + self.finame + '.' + str(index) + '\n',
                            'D=M\n',
                            '@SP\n',
                            'A=M\n',
                            'M=D\n',
                            '@SP\n',
                            'M=M+1\n'
                        ]
            case vmcommandtype.C_POP:
                match segment:
                    case 'constant':
                        pass
                    case 'local' | 'argument' | 'this' | 'that':
                        symbol = self._symbols[segment]
                        lines = [
                            '@' + symbol + '\n',
                            'D=M\n',
                            '@' + str(index) + '\n',
                            'D=D+A\n',
                            '@R13\n',
                            'M=D\n',
                            '@SP\n',
                            'AM=M-1\n',
                            'D=M\n',
                            '@R13\n',
                            'A=M\n',
                            'M=D\n'
                        ]
                    case 'pointer' | 'temp':
                        addr = str(self._mapping[segment] + index)
                        lines = [
                            '@SP\n',
                            'AM=M-1\n',
                            'D=M\n',
                            '@' + addr + '\n',
                            'M=D\n'
                        ]
                    case 'static':
                        lines = [
                            '@SP\n',
                            'AM=M-1\n',
                            'D=M\n',
                            '@' + self.finame + '.' + str(index) + '\n',
                            'M=D\n'
                        ]
        self.f.writelines(lines)

    def writeLabel(self, label: str) -> None:
        lines = [
            '(' + self.funcname + '$' +  label + ')\n'
        ]
        self.f.writelines(lines)
    
    def writeGoto(self, label: str) -> None:
        lines = [
            '@' + self.funcname + '$' + label + '\n',
            '0;JMP\n'
        ]
        self.f.writelines(lines)

    def writeIf(self, label: str) -> None:
        lines = [
            '@SP\n',
            'AM=M-1\n',
            'D=M\n',
            '@' + self.funcname + '$' + label + '\n',
            'D;JNE\n'
        ]
        self.f.writelines(lines)

    def writeCall(self, functionName: str, numArgs: int) -> None:
        lines = [
            '@_CALL' + str(self.callcnt) + '\n',    # push return-address
            'D=A\n',
            '@SP\n',
            'A=M\n',
            'M=D\n',
            '@LCL\n',                           # push LCL
            'D=M\n', 
            '@SP\n',
            'AM=M+1\n',
            'M=D\n',
            '@ARG\n',                           # push ARG
            'D=M\n', 
            '@SP\n',
            'AM=M+1\n',
            'M=D\n',
            '@THIS\n',                          # push THIS
            'D=M\n', 
            '@SP\n',
            'AM=M+1\n',
            'M=D\n',
            '@THAT\n',                          # push THAT
            'D=M\n', 
            '@SP\n',
            'AM=M+1\n',
            'M=D\n',
            '@SP\n',
            'MD=M+1\n',
            '@LCL\n',
            'M=D\n',
            '@' + str(numArgs + 5) + '\n',
            'D=D-A\n',
            '@ARG\n',
            'M=D\n',
            '@' + functionName + '\n',          # goto f
            '0;JMP\n',
            '(_CALL' + str(self.callcnt) + ')\n'    # (return-address)
        ]
        self.f.writelines(lines)
        self.callcnt += 1

    def writeReturn(self) -> None:
        lines = [
            '@LCL\n',       # FRAME = LCL
            'D=M\n',
            '@R13\n',
            'M=D\n',
            '@5\n',         # RET = *(FRAME - 5)
            'A=D-A\n',
            'D=M\n',
            '@R14\n',
            'M=D\n',
            '@SP\n',        # *ARG = pop()
            'AM=M-1\n',
            'D=M\n',
            '@ARG\n',
            'A=M\n',
            'M=D\n',
            '@ARG\n',       # SP = ARG + 1
            'D=M+1\n',
            '@SP\n',
            'M=D\n',
            '@R13\n',       # THAT = *(FRAME - 1)
            'AM=M-1\n',
            'D=M\n',
            '@THAT\n',
            'M=D\n',
            '@R13\n',       # THIS = *(FRAME - 2)
            'AM=M-1\n',
            'D=M\n',
            '@THIS\n',
            'M=D\n',
            '@R13\n',       # ARG = *(FRAME - 3)
            'AM=M-1\n',
            'D=M\n',
            '@ARG\n',
            'M=D\n',
            '@R13\n',       # LCL = *(FRAME - 4)
            'AM=M-1\n',
            'D=M\n',
            '@LCL\n',
            'M=D\n',
            '@R14\n',
            'A=M\n',
            '0;JMP\n'
        ]
        self.f.writelines(lines)
    
    def writeFunction(self, functionName: str, numLocals: int) -> None:
        lines = [
            '(' + functionName + ')\n',
        ]
        if numLocals:
            lines += [
                '@SP\n'
                'A=M\n'
                'M=0\n'
            ] + [
                '@SP\n'
                'AM=M+1\n'
                'M=0\n'
            ] * (numLocals - 1) + [
                '@SP\n',
                'M=M+1\n'
            ]
        self.funcname = functionName
        self.f.writelines(lines)

    # def close(self):
    #     pass
