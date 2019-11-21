use Mix.Config

# Configure your database
config :simple_python_notebook, SimplePythonNotebook.Repo,
  username: "postgres",
  password: "postgres",
  database: "simple_python_notebook_test",
  hostname: "localhost",
  pool: Ecto.Adapters.SQL.Sandbox

# We don't run a server during test. If one is required,
# you can enable the server option below.
config :simple_python_notebook, SimplePythonNotebookWeb.Endpoint,
  http: [port: 4002],
  server: false

# Print only warnings and errors during test
config :logger, level: :warn
