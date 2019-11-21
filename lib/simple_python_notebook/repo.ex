defmodule SimplePythonNotebook.Repo do
  use Ecto.Repo,
    otp_app: :simple_python_notebook,
    adapter: Ecto.Adapters.Postgres
end
