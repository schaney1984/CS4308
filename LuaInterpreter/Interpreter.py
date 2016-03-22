from LuaInterpreter import Parser, Program, ParserException, LexicalException

__author__ = "Steven Chaney"


if __name__ == '__main__':
    try:
        p = Parser("test4.lua")
        prog = p.parse
        prog.execute()
    except ParserException:
        print(ParserException.getMessage())
    except LexicalException:
        print(LexicalException.getMessage())
    except ValueError:
        print(ValueError.args)
    except FileNotFoundError:
        print("source file is not found")
    except Exception:
        print("unknown error occurred -- terminating")
