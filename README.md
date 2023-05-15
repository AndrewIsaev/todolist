# Todolist
Simple todolist application(task tracker)
***
## Features
- Registration/Login via VK Auth
- Creating boards with goal
  - Creating/changing/deleting categories
  - Creating/changing/deleting goals
  - Creating/changing/deleting comments
  - Add another user to your boards with different roles
- Filter goals by category
- Search goals
- Choose goal priority
- Choose goal deadline
- Telegram bot
  - Get own goals using telegram bot
  - Create goal us
***
## Technology stack
- Python 3.10.6
- Django 4.1.7
- Django REST Framework 3.14.0
- Pydantic 1.10.7
- Poetry 1.4.1
- PostgreSQL
- VK OAuth 2.0
- Gunicorn
- Nginx
- Docker
- Docker-compose
- GitHub Actions
- pytest-django
- pre-commit
- black
- mypy
***
## Start app
1. Create .env file:
   ```
   SECRET_KEY=
   DEBUG=True
   DATABASE_URL=

   POSTGRES_USER=
   POSTGRES_PASSWORD=
   POSTGRES_DB=
   POSTGRES_HOST=

   VK_AUTH_KEY=
   VK_APP_SECRET_KEY=
   BOT_TOKEN=
2. Run docker container
   ```
    docker-compose up --build
***
## Project structure
- `bot/`: telegram bot application
- `core/`: login/register application
- `goals/`: goals application
- `tests/`: application`s tests
- `todolist/`: Django settings
- `.env`: environment variables
- `.pre-commit-config.yaml`: pre-commit settings
- `Dockerfile`: production docker file
- `Dockerfile.dev`: developer docker file
- `docker-compose.yaml`: docker compose file
- `entrypoint.sh`: bash script to run migrations
- `poetry.lock`: packages dependencies
- `pyproject.toml`: packages list
- `manage.py`: Django app management
