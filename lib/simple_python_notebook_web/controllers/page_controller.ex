defmodule SimplePythonNotebookWeb.PageController do
  use SimplePythonNotebookWeb, :controller

  def index(conn, _params) do
    render(conn, "index.html")
  end
  
  def python(conn, params) do
    command = params["command"]
    result = SimplePythonNotebook.Console.run(command)
    result = %{
      stdout: result['stdout'] |> to_string(),
      stderr: result['stderr'] |> to_string(),
    }
    json(conn, result)
  end
end
