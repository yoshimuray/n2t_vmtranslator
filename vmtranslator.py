import sys
from pathlib import Path
from vmparser import *
from codewriter import *

assert len(sys.argv) == 2
path = Path(sys.argv[1]).resolve()
if path.suffix == '.vm':
    fopath = path.with_suffix('.asm')
    vmlist = [path]
    path = path.parent
else:
    fopath = Path(path, path.stem).with_suffix('.asm')
    vmlist = list(path.glob('*.vm'))


with fopath.open(mode='w') as fo:
    writer = CodeWriter(fo)
    for fip in vmlist:
        writer.setFileName(str(fip.stem))
        with fip.open() as fi:
            parser = VMParser(fi)
            while parser.hasMoreCommands():
                match parser.commandType():
                    case vmcommandtype.C_ARITHMETIC:
                        writer.writeArithmetic(parser.arg1())                                
                    case vmcommandtype.C_PUSH | vmcommandtype.C_POP:
                        writer.writePushPop(parser.commandType(), parser.arg1(), parser.arg2())
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

