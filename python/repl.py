# Ripped with minor tweaks from https://repl.it/@altendky/Capture-codeInteractiveConsole-output

import code
import io
import sys

# Thanks https://stackoverflow.com/questions/33409207/how-to-return-value-from-exec-in-function
import ast
import copy

class Stream:
    @classmethod
    def flush(cls):
        pass

    def __init__(self):
        self.stream = io.StringIO()

    def flush(self):
        self.stream.flush()

    def read(self, *args, **kwargs):
        result = self.stream.read(*args, **kwargs)
        self.stream = io.StringIO(self.stream.read())

        return result
    
    def write(self, *args, **kwargs):
        p = self.stream.tell()
        self.stream.seek(0, io.SEEK_END)
        result = self.stream.write(*args, **kwargs)
        self.stream.seek(p)
        
        return result

class Console:
    def __init__(self):
        self.console = code.InteractiveConsole()    
        self.console.runcode("""
import matplotlib                                                                                                                                                                                   
matplotlib.use('module://python.my_backend')
print("Initialized matplotlib")
        """)
        self.stdout = Stream()
        self.stderr = Stream()
        
    def runcode(self, *args, **kwargs):
        stdout = sys.stdout
        sys.stdout = self.stdout
        
        stderr = sys.stderr
        sys.stderr = self.stderr

        result = None
        try:
            result = self.console.runcode(*args, **kwargs)
        except SyntaxError:
            self.console.showsyntaxerror()
        except:
            self.console.showtraceback()

        sys.stdout = stdout
        
        sys.stderr = stderr
        
        return result

def convertExpr2Expression(Expr):
        Expr.lineno = 0
        Expr.col_offset = 0
        result = ast.Expression(Expr.value, lineno=0, col_offset = 0)

        return result

def runcode(self, code):
    try:
        code_ast = ast.parse(code)
        init_ast = copy.deepcopy(code_ast)
        init_ast.body = code_ast.body[:-1]

        last_ast = copy.deepcopy(code_ast)
        last_ast.body = code_ast.body[-1:]
        exec(code, self.console.locals)
        if type(last_ast.body[0]) == ast.Expr:
            out = eval(compile(convertExpr2Expression(last_ast.body[0]), "<ast>", "eval"), self.console.locals)
            if out is not None and type(out) not in [str, int, float, bool]:
                return str(out)
            else:
                return out
        else:
            exec(compile(last_ast, "<ast>", "exec"), self.console.locals)
    except SystemExit:
        raise
    except:
        self.console.showtraceback()

c = Console()
c.console.runcode = runcode.__get__(c, code.InteractiveConsole)

def run(command):
    result = None
    command = command.decode()
    if not command.endswith("\n"):
        command += "\n"
    try:
        result = c.runcode(command)
    except:
        pass
    
    return {
            "result": result,
            "stdout": c.stdout.read(),
            "stderr": c.stderr.read()
        }
