defmodule SimplePythonNotebook.IpykernelTest do
  use ExUnit.Case, async: true

  alias SimplePythonNotebook.Kernel
  alias SimplePythonNotebook.Registry

  setup do
    registry = start_supervised!(Registry)
    %{registry: registry}
  end

  test "spawns kernels", %{registry: registry} do
    assert Registry.lookup(registry, "shopping") == :error

    Registry.create(registry, "shopping")
    assert {:ok, pid} = Registry.lookup(registry, "shopping")
    result = Kernel.run(pid, "print('hello world')")
    output = Enum.find(result, fn x -> x["msg_type"] == "stream" end)
      |> Map.get("content")
      |> Map.get("text")

    assert output == "hello world\n"
  end

  test "removes kernels on exit", %{registry: registry} do
    Registry.create(registry, "shopping")
    {:ok, pid} = Registry.lookup(registry, "shopping")
    Agent.stop(pid)
    assert Registry.lookup(registry, "shopping") == :error
  end
end
