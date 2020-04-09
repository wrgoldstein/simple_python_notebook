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

  def handle_in("execute", payload, socket) do
    pid = SimplePythonNotebook.Registry.create(socket.assigns.kernel_id)
    results = SimplePythonNotebook.Kernel.run(pid, payload["text"])
    cell = Map.put(payload, "outputs", results)
    SimplePythonNotebook.State.update(cell)
    Endpoint.broadcast("room:boom", "results", cell)
    {:noreply, socket}
  end

  def handle_in("dynamics", payload, socket) do
    i = payload["dyn_i"]
    value = payload["dyn_v"]
    pid = SimplePythonNotebook.Registry.create(socket.assigns.kernel_id)
    cmd = """
    spl.lock = False
    setattr(spl, "#{i}", #{value})
    spl.lock = True
    """
    IO.inspect(cmd)
    dynamic_update_result = SimplePythonNotebook.Kernel.run(pid, cmd)
    IO.puts("-------------------------")
    IO.inspect(dynamic_update_result)
    IO.puts("-------------------------")
    results = SimplePythonNotebook.Kernel.run(pid, payload["text"])
    IO.inspect(results)
    IO.puts("-------------------------")
    IO.puts("-------------------------")
    cell = Map.put(payload, "outputs", results)
    SimplePythonNotebook.State.update(cell)
    Endpoint.broadcast("room:boom", "results", cell)
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

  def handle_in("restart", _payload, socket) do
    Endpoint.broadcast("room:boom", "restarting", %{})
    SimplePythonNotebook.Registry.restart()
    {:noreply, socket}
  end
end
