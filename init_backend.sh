uv python pin 3.13
uv init
uv venv

touch Dockerfile
touch docker-compose.yml
touch .env.example
touch AGENTS.md
touch TODO.md

uv add --dev pre-commit pyright commitizen
uv run pre-commit autoupdate
uv run pre-commit install --install-hooks --hook-type pre-commit --hook-type commit-msg
uv run pre-commit run --all-files
