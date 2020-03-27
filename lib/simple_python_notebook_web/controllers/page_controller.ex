defmodule SimplePythonNotebookWeb.PageController do
  use SimplePythonNotebookWeb, :controller

  def index(conn, _params) do
    render(conn, "index.html")
  end

  def charlist_to_string(charlist) when is_list(charlist) do
    to_string(charlist)
  end

  def charlist_to_string(other) do
    other
  end
  
  def python(conn, params) do
    command = params["command"]
    result = SimplePythonNotebook.Console.run(command)
    IO.inspect(result)
    # There will be more payload parsing todo
    result = %{
      status: result['status'] |> charlist_to_string(),
      stdout: result['stdout'] |> charlist_to_string(),
      stderr: result['stderr'] |> charlist_to_string(),
      payload: result['payload']
        |> Enum.map(fn x -> x['data']['text/plain'] |> charlist_to_string() end)
    }
    json(conn, result)
  end
end
