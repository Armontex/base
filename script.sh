# bash script.sh

uv python pin 3.13
uv init
uv venv

# ----------------- FILES

rm main.py

rm .gitignore

curl -L -o .gitignore \
    https://raw.githubusercontent.com/Armontex/base/refs/heads/main/python.gitignore

touch .env.example

touch AGENTS.md
cat >> AGENTS.md <<'EOF'
# Instructions
EOF

touch TODO.md
cat >> TODO.md <<'EOF'
# TODO
EOF

curl -L -o Dockerfile \
    https://raw.githubusercontent.com/Armontex/base/refs/heads/main/Dockerfile

curl -L -o docker-compose.yml \
    https://raw.githubusercontent.com/Armontex/base/refs/heads/main/docker-compose.yml

curl -L -o .pre-commit-config.yaml \
    https://raw.githubusercontent.com/Armontex/base/refs/heads/main/.pre-commit-config.yaml

git clone --depth 1 --filter=blob:none --sparse https://github.com/Armontex/base.git temp-base
cd temp-base
git sparse-checkout set src
mv src ../
cd ..
rm -rf temp-base

# ----------------- MIGRATIONS

uv add alembic psycopg2-binary
uv run alembic init migrations

rm migrations/env.py
rm alembic.ini

curl -L -o migrations/env.py \
    https://raw.githubusercontent.com/Armontex/base/refs/heads/main/env.py

curl -L -o alembic.ini \
    https://raw.githubusercontent.com/Armontex/base/refs/heads/main/alembic.ini

echo >> migrations/README

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
ignore = ["RUF001"]
EOF

# ----------------- DEPENDENCIES

uv add fastapi uvicorn sqlalchemy asyncpg dependency-injector pydantic pydantic-settings structlog

# ----------------- DEV

# ----------------- PRE-COMMIT

uv add --dev pre-commit pyright commitizen
uv run pre-commit autoupdate
uv run pre-commit install --install-hooks --hook-type pre-commit --hook-type commit-msg
uv run pre-commit run --all-files

# ----------------- COMMIT

git add .
git commit -m "feat: init commit"
