defmodule SimplePythonNotebook.Registry do
  use GenServer



  # Client API

  @doc """
  Starts the registry.
  """
  def start_link(opts) do
    GenServer.start_link(__MODULE__, :ok, name: __MODULE__)
  end

  @doc """
  Looks up the bucket pid for `kernel_id` stored in `server`.

  Returns `{:ok, pid}` if the bucket exists, `:error` otherwise.
  """
  def lookup(kernel_id) do
    GenServer.call(__MODULE__, {:lookup, kernel_id})
  end

  @doc """
  Ensures there is a bucket associated with the given `kernel_id` in `server`.
  """
  def create(kernel_id) do
    GenServer.call(__MODULE__, {:create, kernel_id})
  end

  def restart(kernel_id) do
    GenServer.call(__MODULE__, {:restart, kernel_id})
  end

  def run(kernel_id, command) do
    GenServer.call(__MODULE__, {:run, kernel_id, command})
  end

  defp start_and_monitor(kernel_id, {kernels, refs}) do
    {:ok, pid, ospid} = SimplePythonNotebook.Kernel.start()
    ref = Process.monitor(pid)
    refs = Map.put(refs, ref, {kernel_id, ospid})
    kernels = Map.put(kernels, kernel_id, {pid, ospid})
    {:reply, pid, {kernels, refs}}
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
    {pid, _} = Map.fetch(kernels, kernel_id)
    {:reply, pid, state}
  end

  @impl true
  def handle_call({:create, kernel_id}, _from, {kernels, refs}) do
    if Map.has_key?(kernels, kernel_id) do
      {:ok, {pid, _}} = Map.fetch(kernels, kernel_id)
      {:reply, pid, {kernels, refs}}
    else
      start_and_monitor(kernel_id, {kernels, refs})
    end
  end

  def handle_call({:restart, kernel_id}, _from, state) do
    {kernels, refs} = state
    if Map.has_key?(kernels, kernel_id) do
      {pid, ospid} = Map.fetch(kernels, kernel_id)
      Agent.stop(pid)
      start_and_monitor(kernel_id, state)
    else
      start_and_monitor(kernel_id, state)
    end
  end

  def handle_info({:DOWN, ref, :process, pid, reason}, {names, refs}) do
    {{name, ospid}, refs} = Map.pop(refs, ref)
    System.cmd("kill", ["#{ospid}"])
    names = Map.delete(names, name)
    {:noreply, {names, refs}}
  end

  @impl true
  def handle_info(_msg, state) do
    {:noreply, state}
  end
end
