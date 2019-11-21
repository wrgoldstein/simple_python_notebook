# Ripped with minor tweaks from https://repl.it/@altendky/Capture-codeInteractiveConsole-output

import code
import io
import sys


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

c = Console()

def run(command):   
    command = command.decode()
    if not command.endswith("\n"):
        command += "\n"
    try:
        c.runcode(code.compile_command(command))
    except:
        pass
    
    return {
            "stdout": c.stdout.read(),
            "stderr": c.stderr.read()
        }

