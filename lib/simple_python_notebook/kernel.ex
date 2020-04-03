defmodule SimplePythonNotebook.Kernel do
  def start() do
    {:ok, pid} = :python.start()
    :python.call(pid, :'python.repl', :setup, []) 
    {:ok, pid}
  end

  @doc """
  Runs python source against a specified kernel
  """
  def run(pid, command) do
    :python.call(pid, :'python.repl', :run, [command])
  end
end
