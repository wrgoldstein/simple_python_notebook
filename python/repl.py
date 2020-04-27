from jupyter_client import BlockingKernelClient
from jupyter_core import paths
from subprocess import Popen, PIPE
import sys, os
import re
from time import sleep
import json
import contextlib
from io import StringIO


load_splonky = """
import sys
sys.path.append('/Users/wgoldstein/wrgoldstein/simple_python_notebook/python')
import splonky
from splonky_sql import RS

# This must be in local scope
# so that global variables are passed!
def run_sql_and_keep_results(i, sql):
  name, data = RS.get(i, sql)
  globals()[name] = data
  return

"""


class CaptureIO:
  def __init__(self):
    self.io = []

  def capture(self, output):
    content = output['content']
    msg_type = output['msg_type']
    self.io.append(dict(content=content, msg_type=msg_type))
  
  def clear(self):
    self.io = []

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
  loaded = client.execute_interactive(load_splonky)
  if loaded['content']['status'] == 'error':
    raise Exception("Could not load core Splonky libraries")
  os_process_id = re.findall('.*\/kernel-(\d+)\.json$', connection_file)[0]
  return os_process_id

TIMEOUT = 500

def run_sql(i, bcmd):
  cmd = bcmd.decode()
  cmd = f'run_sql_and_keep_results({i}, """{cmd}""")'
  cap = CaptureIO()
  outputs = client.execute_interactive(cmd, output_hook=cap.capture)
  return encode(cap.io)

def run(bcmd):
  cmd = bcmd.decode()
  cap = CaptureIO()
  msg = client.execute_interactive(cmd, output_hook=cap.capture)
  cap.capture(msg)
  return encode(cap.io)

def encode(thing):
  """
  Makes sure all strings are encoded for passing
  back to elixir.
  """
  if type(thing) == str: return thing.encode()
  if type(thing) == list:
    return [encode(subthing) for subthing in thing]
  if type(thing) == dict:
    return dict(
      [(encode(k), encode(v)) for k,v in thing.items()]
    )
  else:
    return thing
