defmodule SimplePythonNotebookWeb.RoomChannel do
  use SimplePythonNotebookWeb, :channel

  alias SimplePythonNotebookWeb.Endpoint

  def join(_room, _payload, socket) do
    state = SimplePythonNotebook.State.get()
    length = 8
    client_id = :crypto.strong_rand_bytes(length)
      |> Base.encode64
      |> binary_part(0, length)
    {:ok, %{state: state, client_id: client_id}, socket}
  end

  def handle_in("update", payload, socket) do
    SimplePythonNotebook.State.update(payload)
    Endpoint.broadcast("room:boom", "update", payload)
    {:noreply, socket}
  end
end

