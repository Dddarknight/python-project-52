lint:
	poetry run flake8

install:
	poetry install

test-coverage:
	poetry run coverage run --source='.' manage.py test tests
	poetry run coverage report

build:
	poetry build

test:
	poetry run pytest
