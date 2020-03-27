# > python -m ipykernel
# will give a PID you can use to connect below
# rather than create a new process with the 
# kernel = ... statement.

from jupyter_client import BlockingKernelClient
from jupyter_core import paths
from subprocess import Popen, PIPE
import sys, os
from time import sleep
import json
import contextlib
from io import StringIO

@contextlib.contextmanager
def capture():
    oldout,olderr = sys.stdout, sys.stderr
    try:
        out=[StringIO(), StringIO()]
        sys.stdout,sys.stderr = out
        yield out
    finally:
        sys.stdout,sys.stderr = oldout, olderr
        out[0] = out[0].getvalue()
        out[1] = out[1].getvalue()


client = None

def setup():
  global client

  kernel = Popen([sys.executable, '-m', 'ipykernel'], stdout=PIPE, stderr=PIPE)
  connection_file = os.path.join(
              paths.jupyter_runtime_dir(),
              'kernel-%i.json' % kernel.pid,
          )
  sleep(1)
  client = BlockingKernelClient(connection_file=connection_file)
  client.load_connection_file()
  client.start_channels()
  client.wait_for_ready()
  return connection_file

TIMEOUT = 500

def run(bcmd):
  cmd = bcmd.decode()
  with capture() as (out, err):
    msg = client.execute_interactive(cmd)
    out.seek(0), err.seek(0)
    msg['content']['stdout'] = out.read()
    msg['content']['stderr'] = err.read()
    out.flush(), err.flush()
    return msg['content']
