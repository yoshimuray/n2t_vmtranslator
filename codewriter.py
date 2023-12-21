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
                    '@_AUTO' + str(self.labelcnt) + '\n',
                    'D;JEQ\n',
                    'D=0\n',
                    '@_AUTO' + str(self.labelcnt + 1) + '\n',
                    '0;JMP\n',
                    '(_AUTO' + str(self.labelcnt) + ')\n',
                    'D=-1\n',
                    '(_AUTO' + str(self.labelcnt + 1) + ')\n',
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
                    '@_AUTO' + str(self.labelcnt) + '\n',
                    'D;JGT\n',
                    'D=0\n',
                    '@_AUTO' + str(self.labelcnt + 1) + '\n',
                    '0;JMP\n',
                    '(_AUTO' + str(self.labelcnt) + ')\n',
                    'D=-1\n',
                    '(_AUTO' + str(self.labelcnt + 1) + ')\n',
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
                    '@_AUTO' + str(self.labelcnt) + '\n',
                    'D;JLT\n',
                    'D=0\n',
                    '@_AUTO' + str(self.labelcnt + 1) + '\n',
                    '0;JMP\n',
                    '(_AUTO' + str(self.labelcnt) + ')\n',
                    'D=-1\n',
                    '(_AUTO' + str(self.labelcnt + 1) + ')\n',
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

    # def close(self):
    #     pass
