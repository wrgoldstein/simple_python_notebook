defmodule SimplePythonNotebookWeb.Router do
  use SimplePythonNotebookWeb, :router

  pipeline :browser do
    plug :accepts, ["html", "json"]
    plug :fetch_session
    plug :fetch_flash
    plug :protect_from_forgery
    plug :put_secure_browser_headers
  end

  pipeline :api do
    plug :accepts, ["json"]
  end

  scope "/", SimplePythonNotebookWeb do
    pipe_through :browser

    get "/", PageController, :index
    post "/python", PageController, :python
  end

  # Other scopes may use custom stacks.
  # scope "/api", SimplePythonNotebookWeb do
  #   pipe_through :api
  # end
end
