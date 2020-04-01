defmodule SimplePythonNotebook.State do
  use Agent

  def start_link(_) do
    Agent.start_link(fn -> [] end, name: __MODULE__)
  end

  def get() do
    Agent.get(__MODULE__, fn state -> state end)
  end

  def update(payload) do
    position = payload["i"]
    new = Map.take(payload, ["text", "uuid", "outputs"])
    Agent.update(__MODULE__, fn state -> 
      current = Enum.at(state, position)
      if current && current["uuid"] == payload["uuid"] do
        List.replace_at(state, position, payload)
      else
        List.insert_at(state, position, payload)
      end
    end)
  end

  def add_cell(payload) do
  end

  def remove(payload) do
    Agent.update(__MODULE__, fn state -> 
      List.delete_at(state, payload["i"])
    end)
  end
end
