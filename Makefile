lint:
	poetry run flake8

install:
	poetry install

test-coverage:
	poetry run coverage run --source='.' manage.py test tests
	poetry run coverage report
	poetry run coverage xml

build:
	poetry build

test:
	./manage.py test tests
