defmodule SimplePythonNotebook.Registry do
  use GenServer

  # Client API

  @doc """
  Starts the registry.
  """
  def start_link(opts) do
    GenServer.start_link(__MODULE__, :ok, opts)
  end

  @doc """
  Looks up the bucket pid for `kernel_id` stored in `server`.

  Returns `{:ok, pid}` if the bucket exists, `:error` otherwise.
  """
  def lookup(server, kernel_id) do
    GenServer.call(server, {:lookup, kernel_id})
  end

  @doc """
  Ensures there is a bucket associated with the given `kernel_id` in `server`.
  """
  def create(server, kernel_id) do
    GenServer.call(server, {:create, kernel_id})
  end

  def run(server, kernel_id, command) do
    GenServer.call(server, {:run, kernel_id, command})
  end

  # Server API

  @impl true
  def init(:ok) do
    kernels = %{}
    refs = %{}
    {:ok, {kernels, refs}}
  end

  @impl true
  def handle_call({:lookup, kernel_id}, _from, state) do
    {kernels, _} = state
    pid = Map.fetch(kernels, kernel_id)
    {:reply, pid, state}
  end

  @impl true
  def handle_call({:create, kernel_id}, _from, {kernels, refs}) do
    if Map.has_key?(kernels, kernel_id) do
      {:reply, Map.fetch(kernels, kernel_id), {kernels, refs}}
    else
      {:ok, pid} = SimplePythonNotebook.Kernel.start()
      ref = Process.monitor(pid)
      refs = Map.put(refs, ref, kernel_id)
      kernels = Map.put(kernels, kernel_id, pid)
      {:reply, pid, {kernels, refs}}
    end
  end

  @impl true
  def handle_info({:DOWN, ref, :process, _pid, _reason}, {names, refs}) do
    {name, refs} = Map.pop(refs, ref)
    names = Map.delete(names, name)
    {:noreply, {names, refs}}
  end

  @impl true
  def handle_info(_msg, state) do
    {:noreply, state}
  end
end
