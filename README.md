# SEA-web-app

## GO LIVE CHECKLIST

- Switch from `psycopg2-binary` to `psycopg2` for Production
- run `docker-compose exec web python manage.py collectstatic --noinput` before deploying or restarting your app so the latest static assets are gathered.

## How to test with pytest

1. Ensure `pytest` and `pytest-django` are in `requirements.txt`
2. Install them inside docker. Run `docker-compose build` in the terminal
3. Create a `pytest.ini` file in your root directory
    - It must contain:
        ```
        [pytest]
        DJANGO_SETTINGS_MODULE = mysite.settings
        python_files = tests.py test_*.py *_tests.py
        ```
4. Run tests with `docker-compose exec web pytest` in the terminal
5. This will run the tests in `main/tests.py`

### Running tests with coverage

1. Add `pytest-cov` to your `requirements.txt`
2. Run tests with coverage: `docker-compose exec web pytest --cov=main --cov-report=term-missing`
    - `--cov=main` tells it to measure coverage for your `main` app.
    - `--cov-report=term-missing` shows lines that were not covered.
3. Generate an HTML report: `docker-compose exec web pytest --cov=main --cov-report=html`

## If you add or update CSS, images, or JS...

- Rerun `docker-compose exec web python manage.py collectstatic --noinput`

## Makefile Commands

To simplify common Docker and Django tasks, this project includes a `Makefile` with handy commands. Run these commands from the root of the project (where the `Makefile` is located).

### Usage

```bash
make <command>
```

## Always make sure you're executing commands inside the docker container

- `docker-compose exec web python manage.py makemigrations`
- `docker-compose exec web python manage.py migrate`
- `docker-compose exec web python manage.py createsuperuser`
- `docker-compose exec web pytest`