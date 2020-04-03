defmodule SimplePythonNotebook.Kernel do
  def start() do
    {:ok, erl_pid} = :python.start()
    py_pid = :python.call(erl_pid, :'python.repl', :setup, []) 
    {:ok, erl_pid, py_pid}
  end

  @doc """
  Runs python source against a specified kernel
  """
  def run(pid, command) do
    :python.call(pid, :'python.repl', :run, [command])
  end
end
