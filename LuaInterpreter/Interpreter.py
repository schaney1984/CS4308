from LuaInterpreter import Parser, ParserException, LexicalException
import traceback

__author__ = "Steven Chaney"


if __name__ == '__main__':
    try:
        p = Parser.Parser("test3.lua")
        prog = p.parse()
        prog.execute()
    except ParserException.ParserException as p:
        print(p)
        # print("ParserException")
        traceback.print_exc()
    except LexicalException.LexicalException as l:
        print(l)
        # print("LexicalException")
        traceback.print_exc()
    except ValueError as v:
        print(v)
        # print("ValueError")
        traceback.print_exc()
    except FileNotFoundError:
        print("source file is not found")
        traceback.print_exc()
    except Exception as e:
        print(e)
        traceback.print_exc()
