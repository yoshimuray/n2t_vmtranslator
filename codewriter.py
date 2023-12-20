import io
import vmcommandtype

class CodeWriter:
    def __init__(self, f: io.TextIOWrapper) -> None:
        self.f = f
        self.labelcnt = 0

    # def setFileName(self, fileName: str) -> None:
    #     pass

    def writeArithmetic(self, command: str) -> None:
        lines = []
        match command:
            case 'add':
                lines = [
                    '@SP\n',
                    'A=A-1\n',
                    'D=M\n',
                    'A=A-1\n',
                    'M=D+M\n',
                    'A=A+1\n'
                ]
            case 'sub':
                lines = [
                    '@SP\n',
                    'A=A-1\n',
                    'D=M\n',
                    'A=A-1\n',
                    'M=M-D\n',
                    'A=A+1\n'
                ]
            case 'neg':
                lines = [
                    '@SP\n',
                    'A=A-1\n',
                    'M=-M\n',
                    'A=A+1\n'
                ]
            case 'eq':
                lines = [
                    '@SP\n',
                    'A=A-1\n',
                    'D=M\n',
                    'A=A-1\n',
                    'D=M-D\n',
                    '@_AUTO' + str(self.labelcnt) + '\n',
                    'D;JEQ\n',
                    'D=1\n',
                    '@_AUTO' + str(self.labelcnt + 1) + '\n',
                    '0;JMP\n',
                    '(_AUTO' + str(self.labelcnt) + ')\n',
                    'D=0\n',
                    '(_AUTO' + str(self.labelcnt + 1) + ')\n',
                    '@SP\n',
                    'M=D\n',
                    'A=A+1\n'
                ]
                self.labelcnt += 2
            case 'gt':
                lines = [
                    '@SP\n',
                    'A=A-1\n',
                    'D=M\n',
                    'A=A-1\n',
                    'D=M-D\n',
                    '@_AUTO' + str(self.labelcnt) + '\n',
                    'D;JGT\n',
                    'D=1\n',
                    '@_AUTO' + str(self.labelcnt + 1) + '\n',
                    '0;JMP\n',
                    '(_AUTO' + str(self.labelcnt) + ')\n',
                    'D=0\n',
                    '(_AUTO' + str(self.labelcnt + 1) + ')\n',
                    '@SP\n',
                    'M=D\n',
                    'A=A+1\n'
                ]
                self.labelcnt += 2
            case 'lt':
                lines = [
                    '@SP\n',
                    'A=A-1\n',
                    'D=M\n',
                    'A=A-1\n',
                    'D=M-D\n',
                    '@_AUTO' + str(self.labelcnt) + '\n',
                    'D;JLT\n',
                    'D=1\n',
                    '@_AUTO' + str(self.labelcnt + 1) + '\n',
                    '0;JMP\n',
                    '(_AUTO' + str(self.labelcnt) + ')\n',
                    'D=0\n',
                    '(_AUTO' + str(self.labelcnt + 1) + ')\n',
                    '@SP\n',
                    'M=D\n',
                    'A=A+1\n'
                ]
                self.labelcnt += 2
            case 'and':
                lines = [
                    '@SP\n',
                    'A=A-1\n',
                    'D=M\n',
                    'A=A-1\n',
                    'M=D&M\n',
                    'A=A+1\n'
                ]
            case 'or':
                lines = [
                    '@SP\n',
                    'A=A-1\n',
                    'D=M\n',
                    'A=A-1\n',
                    'M=D|M\n',
                    'A=A+1\n'
                ]
            case 'not':
                lines = [
                    '@SP\n',
                    'A=A-1\n',
                    'M=!M\n',
                    'A=A+1\n'
                ]
        self.f.writelines(lines)

    def writePushPop(self, command: vmcommandtype.VMCommandType, segment: str, index: int) -> None:
        lines = []
        match command:
            case vmcommandtype.C_PUSH:
                lines = [
                    '@' + str(index) + '\n',
                    'D=A',
                    '@SP',
                    'M=D',
                    'A=A+1'
                ]
            case vmcommandtype.C_POP:
                pass
        self.f.writelines(lines)

    # def close(self):
    #     pass
