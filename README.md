# Task Manager
Task Manager is an application, which provides the oppotunity for task management, including adding tasks with different pamameters referring to the users of the app, their tracking and filtering.

____

### Hexlet tests, linter status and CodeClimate:
[![Actions Status](https://github.com/Dddarknight/python-project-52/workflows/hexlet-check/badge.svg)](https://github.com/Dddarknight/python-project-52/actions) [![Python CI](https://github.com/Dddarknight/python-project-52/actions/workflows/pyci.yml/badge.svg)](https://github.com/Dddarknight/python-project-52/actions) <a href="https://codeclimate.com/github/Dddarknight/python-project-52/maintainability"><img src="https://api.codeclimate.com/v1/badges/bd5f746a84f1581c4360/maintainability" /></a> <a href="https://codeclimate.com/github/Dddarknight/python-project-52/test_coverage"><img src="https://api.codeclimate.com/v1/badges/bd5f746a84f1581c4360/test_coverage" /></a>

## Links
This project was built using these tools:
| Tool | Description |
|----------|---------|
| [Django ](https://www.djangoproject.com/) |  "A high-level Python web framework" |
| [poetry](https://python-poetry.org/) |  "Python dependency management and packaging made easy" |
| [Py.Test](https://pytest.org) | "A mature full-featured Python testing tool" |
| [django-filter](https://django-filter.readthedocs.io/en/stable/) | "Allows to filter down a queryset based on a model’s fields" |
| [Selenium](https://selenium-python.readthedocs.io/index.html) | "For automating web applications for testing purposes" |


### Heroku link:

[![Heroku](https://pyheroku-badge.herokuapp.com/?app=fast-sea-58330)](https://fast-sea-58330.herokuapp.com/)

## Installation for contributors
```
$ git clone git@github.com:Dddarknight/python-project-52.git
$ cd python-project-52
$ pip install poetry
$ make install
$ touch .env

You have to write into .env file SECRET_KEY for Django app and token for Rollbar. See .env.example.
To get SECRET_KEY for Django app:
$ python manage.py shell
>>> from django.core.management.utils import get_random_secret_key
>>> get_random_secret_key()

Then add new SECRET_KEY to .env file

$ make migrate
$ make run
```

## Description and usage
Here are some hints for using the app.
| Steps | Description |
|----------|---------|
| Registration |  First you need to register in the app using the provided form of registration. |
| Log in | Then you have to log in using the information you've filled in the registration form. |
| User | You can see all users on the relevant page. You can change the information only about yourself. If the user is an author or an executor of the task he cannot be deleted.|
| Statuses | You can add, update, delete statuses of the tasks, if you are logged in. The statuses which correspond with any tasks cannot be deleted.|
| Labels | You can add, update, delete labels of the tasks, if you are logged in. The label which correspond with any tasks cannot be deleted.|
| Tasks | You can add, update, delete tasks, if you are logged in. You can also filter tasks on the relevant page with given statuses, exetutors and labels.|

## License
[GNU GPLv3](https://choosealicense.com/licenses/gpl-3.0/)
