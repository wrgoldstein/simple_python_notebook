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

  def handle_in("restart", _payload, socket) do
    pid = SimplePythonNotebook.Registry.restart(socket.assigns.kernel_id)
    Endpoint.broadcast("room:boom", "started", %{})
    {:noreply, socket}
  end

  def handle_in("execute", payload, socket) do
    pid = SimplePythonNotebook.Registry.create(socket.assigns.kernel_id)
    results = SimplePythonNotebook.Kernel.run(pid, payload["text"])
    cell = Map.put(payload, "outputs", results)
    SimplePythonNotebook.State.update(cell)
    Endpoint.broadcast("room:boom", "results", cell)
    {:noreply, socket}
  end

  def handle_in("dynamics", payload, socket) do
    id = payload["updated_id"]
    value = payload["updated_value"]
    IO.puts("The value is #{value}!")
    pid = SimplePythonNotebook.Registry.create(socket.assigns.kernel_id)
    cmd = "splonky.SplRegistry['#{id}'](#{value})"
    result = SimplePythonNotebook.Kernel.run(pid, cmd)
    Endpoint.broadcast("room:boom", "dynamic_outputs", %{id: id, result: result})
    {:noreply, socket}
  end

  def handle_in("save", payload, socket) do
    state = SimplePythonNotebook.State.get()
    Endpoint.broadcast("room:boom", "saved", payload)
    {:noreply, socket}
  end

  def handle_in("add", payload, socket) do
    SimplePythonNotebook.State.update(payload)
    Endpoint.broadcast("room:boom", "add", payload)
    {:noreply, socket}
  end

  def handle_in("remove", payload, socket) do
    SimplePythonNotebook.State.remove(payload)
    Endpoint.broadcast("room:boom", "remove", payload)
    {:noreply, socket}
  end

  def handle_in("results", payload, socket) do
    SimplePythonNotebook.State.update(payload)
    Endpoint.broadcast("room:boom", "results", payload)
    {:noreply, socket}
  end
end
