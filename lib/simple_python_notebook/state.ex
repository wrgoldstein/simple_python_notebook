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
    position = payload["i"]
    # Must increment "i" for all other cells..
  end

  def remove(payload) do
    Agent.update(__MODULE__, fn state -> 
      List.delete_at(state, payload["i"])
    end)
  end
end
