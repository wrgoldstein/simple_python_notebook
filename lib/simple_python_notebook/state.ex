defmodule SimplePythonNotebook.State do
  use Agent

  def start_link(_) do
    Agent.start_link(fn -> [] end, name: __MODULE__)
  end

  def get() do
    Agent.get(__MODULE__, fn state -> state end)
  end

  def update(payload) do
    # This will be more complex with multiple cells
    Agent.update(__MODULE__, fn state -> [payload] end)
  end
end
