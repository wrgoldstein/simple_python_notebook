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
  os_process_id = re.findall('.*\/kernel-(\d+)\.json$', connection_file)[0]
  client.execute_interactive(load_splonky)
  return os_process_id

TIMEOUT = 500

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
