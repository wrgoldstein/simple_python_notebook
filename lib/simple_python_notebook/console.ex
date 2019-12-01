defmodule SimplePythonNotebook.Console do
    use Agent
  
    def start_link(connection) do
      Agent.start_link(fn -> connect(connection) end, name: __MODULE__)
    end
  
    def run(command) do
      Agent.get(__MODULE__, fn pid ->
        :python.call(pid, :'python.repl', :run, [command]) 
      end)
    end
    
    def connect(nil) do
      {:error, "No connection set"}
    end
  
    def connect(connection) do
      {:ok, pid} = :python.start()
      pid
    end
  end