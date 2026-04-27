uv python pin 3.13
uv init
uv venv

# ----------------- FILES

rm main.py

rm .gitignore

curl -L -o .gitignore \
    https://raw.githubusercontent.com/Armontex/base/refs/heads/main/python.gitignore

touch docker-compose.yml
touch .env.example
touch AGENTS.md
touch TODO.md

curl -L -o Dockerfile \
    https://raw.githubusercontent.com/Armontex/base/refs/heads/main/Dockerfile

curl -L -o .pre-commit-config.yaml \
    https://raw.githubusercontent.com/Armontex/base/refs/heads/main/.pre-commit-config.yaml

# ----------------- MIGRATIONS

uv add alembic psycopg2-binary
alembic init migrations

# ----------------- CONFIG


cat >> pyproject.toml <<'EOF'

[tool.pyright]
venvPath = "."
venv = ".venv"
pythonVersion = "3.13"

[tool.pytest.ini_options]
asyncio_mode = "auto"
asyncio_default_fixture_loop_scope = "session"
asyncio_default_test_loop_scope = "session"
testpaths = ["tests"]

[tool.ruff]
line-length = 88
target-version = "py313"

[tool.ruff.lint]
select = ["E", "F", "I", "B", "UP", "RUF"]
EOF

# ----------------- PRE-COMMIT

uv add --dev pre-commit pyright commitizen
uv run pre-commit autoupdate
uv run pre-commit install --install-hooks --hook-type pre-commit --hook-type commit-msg
uv run pre-commit run --all-files

# ----------------- ARCHITECTURE



# ----------------- DEPENDENCIES

uv add fastapi uvicorn sqlalchemy asyncpg dependency-injector pydantic pydantic-settings structlog

# ----------------- DEV

uv add --dev hypothesis polyfactory pytest pytest-asyncio pytest-mock pytest-randomly testcontainers


# ----------------- COMMIT

git add .
git commit -m "init commit"