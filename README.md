# Cinescope Autotests

Автотесты для проекта Cinescope: API, UI и DB проверки в одном репозитории.

## Что внутри

- API-тесты: регистрация, аутентификация, пользователи, фильмы.
- UI-тесты: регистрация, логин, отзывы, demoqa-сценарии.
- DB-тесты: проверки данных через SQLAlchemy и PostgreSQL.
- Отчеты: Allure.
- Трассировки UI: Playwright trace (`files/playwright_trace`).

## Стек

- Python
- Pytest
- Requests
- Playwright
- Pydantic
- SQLAlchemy
- Psycopg2
- Faker
- Allure Pytest

## Структура проекта

- `clients` — API-клиенты.
- `custom_requester` — общий HTTP-слой для запросов.
- `models` / `entities` — модели данных.
- `tests/api` — API тесты.
- `tests/ui` — UI тесты.
- `tests/database` — DB тесты.
- `pages` — Page Object для UI.
- `db_requester` / `db_models` — работа с БД.
- `utils` — генераторы и утилиты.
- `resources` — переменные окружения (креды).

## Быстрый старт

### 1. Клонирование

```powershell
git clone https://github.com/sklit-dsk/cinescope-autotests.git
cd cinescope-autotests
```

### 2. Виртуальное окружение

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

Если PowerShell блокирует активацию:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
.\venv\Scripts\Activate.ps1
```

### 3. Установка зависимостей

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
python -m playwright install chromium
```

## Переменные окружения

Создай файл `.env` в корне проекта.

Минимально необходимые переменные:

```env
SUPER_ADMIN_USERNAME=your_login
SUPER_ADMIN_PASSWORD=your_password

DB_MOVIES_NAME=your_db_name
DB_MOVIES_USERNAME=your_db_user
DB_MOVIES_PASSWORD=your_db_password
DB_MOVIES_HOST=your_db_host
DB_MOVIES_PORT=5432
```

Использование:

- `SUPER_ADMIN_*` — авторизация супер-админа в API/UI фикстурах.
- `DB_MOVIES_*` — подключение к БД в DB-тестах.

## Запуск тестов

### Все тесты

```powershell
pytest
```

### По типам

```powershell
pytest -m api
pytest -m ui
pytest -m db
```

### По папкам

```powershell
pytest tests/api
pytest tests/ui
pytest tests/database
```

### Один тест/класс

```powershell
pytest tests/ui/test_reviews_cinescope.py::TestReviews::test_create_review -q
pytest tests/ui/test_login_cinescope.py::TestLogin::test_login -q
```

### Ретраи для нестабильных тестов

```powershell
pytest --reruns 2 --reruns-delay 2
```

## Allure отчет

### 1. Сгенерировать результаты

```powershell
pytest tests/ui --alluredir=allure-results
```

### 2. Быстро открыть отчет

```powershell
allure serve allure-results
```

### 3. Сгенерировать статический отчет

```powershell
allure generate allure-results -o allure-report --clean
allure open allure-report
```

Если `allure` не найден:

```powershell
allure --version
winget install Qameta.Allure
```

После установки перезапусти терминал.

## Полезные команды для отладки

```powershell
pytest -k "login" -q
pytest -k "reviews and ui" -q
pytest -s tests/ui/test_reviews_cinescope.py
pytest --collect-only
```

## Маркеры Pytest

Доступные маркеры из `pytest.ini`:

- `smoke`
- `regression`
- `slow`
- `api`
- `ui`
- `db`
- `skip_authenticated_user_cleanup`

Примеры:

```powershell
pytest -m "smoke and api"
pytest -m "ui and not slow"
```

## Частые проблемы

### 1. `pytest: command not found`

Запускай через интерпретатор venv:

```powershell
.\venv\Scripts\python.exe -m pytest
```

### 2. Timeout в Playwright

- Убедись, что открыт корректный URL и пользователь реально авторизован.
- Проверь актуальность `data-qa-id` локаторов.
- Добавляй явные ожидания (`expect(...).to_be_visible()`), а не `sleep`.

### 3. Не собирается Allure

- Проверь, что есть папка `allure-results`.
- Проверь установку CLI: `allure --version`.

### 4. Ошибки подключения к БД

- Проверь `DB_MOVIES_*` в `.env`.
- Проверь доступность хоста и порта БД.

## Рекомендации по запуску в CI

- API и DB тесты запускать отдельно от UI.
- Для UI хранить trace артефакты из `files/playwright_trace`.
- Публиковать `allure-report` как build artifact.

## Команда

Проект поддерживается QA-командой Cinescope.
