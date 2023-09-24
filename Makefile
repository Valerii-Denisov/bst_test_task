install:
	poetry install

lint:
	poetry run flake8 R4C

test:
	poetry run python manage.py test

test-coverage:
	poetry run coverage run manage.py test
	poetry run coverage xml
	poetry run coverage report

requir:
	poetry export --without-hashes --format=requirements.txt > requirements.txt

runserver:
	poetry run python manage.py runserver