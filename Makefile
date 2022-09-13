lint:
	poetry run flake8

install:
	poetry install

test-coverage:
	poetry run coverage run --source='.' manage.py test
	poetry run coverage report
	poetry run coverage xml

run:
	poetry run python manage.py runserver

build:
	poetry build

test:
	poetry run python manage.py test
