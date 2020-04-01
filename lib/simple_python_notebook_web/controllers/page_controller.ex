defmodule SimplePythonNotebookWeb.PageController do
  use SimplePythonNotebookWeb, :controller

  def index(conn, _params) do
    render(conn, "index.html")
  end
end
