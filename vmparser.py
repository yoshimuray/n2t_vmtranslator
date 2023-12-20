import io
import re
import vmcommandtype

class VMParser:
    def __init__(self, f: io.TextIOWrapper) -> None:
        self.f = f
        self.isEOF = False
        while not self.isEOF:
            s = self.f.readline()
            self.isEOF = (len(s) == 0)
            self.cmd = re.sub('//.*', '', s).strip().split()
            if self.cmd:
                break

    def hasMoreCommands(self) -> bool:
        return not self.isEOF

    def advance(self) -> None:
        assert self.hasMoreCommands()
        while not self.isEOF:
            s = self.f.readline()
            self.isEOF = (len(s) == 0)
            self.cmd = re.sub('//.*', '', s).strip()
            if self.cmd:
                break

    def commandType(self) -> vmcommandtype.VMCommandType:
        match self.cmd[0]:
            case 'add' | 'sub' | 'neg' | 'eq' | 'gt' | 'lt' | 'and' | 'or' | 'not':
                return vmcommandtype.C_ARITHMETIC
            case 'push':
                return vmcommandtype.C_PUSH
            case 'pop':
                return vmcommandtype.C_POP
            case 'label':
                return vmcommandtype.C_LABEL
            case 'goto':
                return vmcommandtype.C_GOTO
            case 'if-goto':
                return vmcommandtype.C_IF
            case 'function':
                return vmcommandtype.C_FUNCTION
            case 'return':
                return vmcommandtype.C_RETURN
            case 'call':
                return vmcommandtype.C_CALL

    def arg1(self) -> str:
        assert(self.commandType() != vmcommandtype.C_RETURN)
        match self.commandType():
            case vmcommandtype.C_ARITHMETIC:
                return self.cmd[0]
            case _:
                return self.cmd[1]
    
    def arg2(self) -> int:
        assert(self.commandType() in [vmcommandtype.C_PUSH, vmcommandtype.C_POP, vmcommandtype.C_FUNCTION, vmcommandtype.C_CALL])
        return int(self.cmd[2])
            
