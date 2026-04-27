# TODO

- [ ] Test, dev
- [ ] live и ready на бд, помимо health в app

• Если смотреть жёстко, сейчас Armontex/base больше похож не на готовую base-платформу, а на черновой bootstrap-шаблон. Это не
плохо, но тогда его стоит довести либо до уровня template generator, либо до уровня реально запускаемого skeleton-репозитория.
Сейчас он посередине.

Что бы я исправил в первую очередь

- script.sh:3 надо делать безопасным и идемпотентным. Сейчас нет set -euo pipefail, нет trap, нет проверок существования файлов, а
  команды rm, mv, git branch -M, git commit и git checkout -b предполагают идеальное окружение. Повторный запуск легко ломает
  проект.
- script.sh:18, script.sh:23, script.sh:63 сейчас используют >>, поэтому AGENTS.md, TODO.md, pyproject.toml при повторном запуске
  будут дублироваться. Это критичный дефект для шаблона.
- script.sh:13, script.sh:28, script.sh:37 тянет артефакты с main и клонирует сам репозиторий как источник шаблона. Это делает
  bootstrap неповторяемым. Нужны pinned tag/SHA или релизные артефакты.
- Dockerfile:16 ожидает pyproject.toml и uv.lock, но в текущем дереве репозитория их нет. То есть сам репозиторий в таком виде не
  self-hosted и не воспроизводим как готовая база.
- docker-compose.yml:14 монтирует Postgres volume в /var/lib/postgresql, а для официального образа обычно нужен /var/lib/
  postgresql/data. Я бы это считал багом, а не улучшением.
- docker-compose.yml:5 требует .env, но script.sh:16 создаёт только .env.example. Для нового пользователя это лишний скрытый шаг.
- src/main.py:53 даёт только /health, причём без проверки БД. API может отвечать ok, когда база недоступна. Нужны минимум /live
  и /ready.
- Пустые файлы src/app/common/ports.py, src/app/common/dto.py, src/domain/validators.py, src/presentation/common/
  exception_handler.py показывают, что архитектурные слои намечены, но не реализованы. Либо заполнить их рабочими абстракциями,
  либо убрать до появления реального кода.

Жёсткие фичи и апдейты

- Превратить script.sh в нормальный scaffolder: режимы api, worker, full; имя сервиса; имя пакета; выбор postgres/redis; включение
  auth, alembic, celery, sentry, otel.
- Вместо shell-скрипта перейти на copier или собственный CLI. Для шаблона это намного надёжнее: переменные, версии, условные
  файлы, апгрейды шаблона.
- Сделать репозиторий self-contained: чтобы git clone && uv sync && docker compose up работало без генерации промежуточным
  скриптом.
- Добавить production-ready каркас backend-а: router versioning, global exception handlers, request-id middleware, structured
  error contract, unit-of-work, repositories, services/use-cases, pagination/sorting/filtering primitives.
- Добавить observability baseline: JSON-логи для prod, correlation id, Prometheus metrics, OpenTelemetry tracing, Sentry.
- Добавить security baseline: auth module, RBAC, refresh/access token flow, audit log, rate limit, CORS/TrustedHost, secrets
  policy.
- Добавить async/background контур: Redis + task queue, outbox pattern, scheduled jobs, retry policy.
- Добавить GitHub Actions: lint, typecheck, tests, docker build, migration smoke test, release/tag flow.
- Добавить devcontainer/Nix/Makefile/Justfile, чтобы локальная среда поднималась одной командой.

Средние улучшения

- src/infra/logging/setup.py:8 стоит разделить dev/prod logging. Сейчас всегда ConsoleRenderer, для прод-среды лучше JSON.
- src/infra/db/**init**.py:11 можно усилить pool-настройками, pool_pre_ping, pool_recycle, таймаутами и отдельными параметрами для
  тестов.
- env.py:44 и вся миграционная часть выглядят как bootstrap, но в репозитории нет полноценного migrations/versions. Я бы добавил
  реальную структуру миграций и smoke-тест на alembic upgrade head.
- docker-compose.yml:46 stop_grace_period: 1s слишком агрессивен; graceful shutdown легко обрежется.
- Имеет смысл добавить tests/unit, tests/integration, tests/e2e с базовыми фикстурами. Сейчас отсутствие тестов — главный стоп-
  фактор для эволюции шаблона.

Мелкие, но полезные вещи

- README с чётким позиционированием: это шаблон, генератор или базовый сервис.
- .env.example с полным набором переменных и командой быстрого старта.
- LICENSE, CONTRIBUTING.md, CODEOWNERS, release notes.
- GitHub metadata: description, topics, releases. На странице репозитория сейчас даже нет описания и релизов:
  https://github.com/Armontex/base
- Убрать или заменить TODO.md на roadmap/issues, иначе это просто шум.
- Добавить shellcheck и hadolint в pre-commit/CI, потому что у тебя есть и shell, и Docker.

Если кратко: самый сильный апдейт здесь не “добавить ещё пару модулей”, а выбрать стратегию. Либо это reproducible template repo,
который сам по себе запускается и тестируется. Либо это project generator, который параметризованно создаёт сервисы. Сейчас он
между этими состояниями, и из-за этого основные проблемы именно в воспроизводимости и DX, а не в бизнес-фичах.

Если хочешь, следующим сообщением я могу собрать тебе уже конкретный roadmap в порядке P0/P1/P2 с оценкой по сложности и пользе.
