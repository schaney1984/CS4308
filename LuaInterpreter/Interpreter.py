from LuaInterpreter import Parser, ParserException, LexicalException

__author__ = "Steven Chaney"


if __name__ == '__main__':
    try:
        p = Parser.Parser("test4.lua")
        prog = p.parse()
        prog.execute()
    except ParserException.ParserException:
        print(ParserException.ParserException.args)
    except LexicalException.LexicalException:
        print(LexicalException.LexicalException.args)
    except ValueError:
        print(ValueError.args)
    except FileNotFoundError:
        print("source file is not found")
    except Exception:
        print("unknown error occurred -- terminating")
