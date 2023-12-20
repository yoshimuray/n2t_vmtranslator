import sys
from pathlib import Path
from vmparser import *
from codewriter import *

assert len(sys.argv) == 2
di = name = sys.argv[1]
if name[-3:] == '.vm':
    di = '.'
    name = name[:-3]

with open(name + '.asm', mode='w') as fo:
    writer = CodeWriter(fo)
    for fip in Path(di).glob('*.vm'):
        with fip.open() as fi:
            parser = VMParser(fi)
            while parser.hasMoreCommands():
                match parser.commandType():
                    case vmcommandtype.C_ARITHMETIC:
                        writer.writeArithmetic(parser.arg1())                                
                    case vmcommandtype.C_PUSH | vmcommandtype.C_POP:
                        writer.writePushPop(parser.arg1(), parser.arg2())
                    case vmcommandtype.C_LABEL:
                        pass
                    case vmcommandtype.C_GOTO:
                        pass
                    case vmcommandtype.C_IF:
                        pass
                    case vmcommandtype.C_FUNCTION:
                        pass
                    case vmcommandtype.C_RETURN:
                        pass
                    case vmcommandtype.C_CALL:
                        pass
                parser.advance()

