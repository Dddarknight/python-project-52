# Task Manager
Task Manager is an application, which provides the oppotunity for task management, including adding tasks with different pamameters referring to the users of the app, their tracking and filtering.

____

### Hexlet tests and linter status:
[![Actions Status](https://github.com/Dddarknight/python-project-52/workflows/hexlet-check/badge.svg)](https://github.com/Dddarknight/python-project-52/actions)

[![Python CI](https://github.com/Dddarknight/python-project-52/actions/workflows/pyci.yml/badge.svg)](https://github.com/Dddarknight/python-project-52/actions)


### CodeClimate:
<a href="https://codeclimate.com/github/Dddarknight/python-project-52/maintainability"><img src="https://api.codeclimate.com/v1/badges/bd5f746a84f1581c4360/maintainability" /></a>

<a href="https://codeclimate.com/github/Dddarknight/python-project-52/test_coverage"><img src="https://api.codeclimate.com/v1/badges/bd5f746a84f1581c4360/test_coverage" /></a>

## Links
This project was built using these tools:
| Tool | Description |
|----------|---------|
| [poetry](https://python-poetry.org/) |  "Python dependency management and packaging made easy" |
| [Py.Test](https://pytest.org) | "A mature full-featured Python testing tool" |

### Heroku link:

[![Heroku](https://heroku-badge.herokuapp.com/?app=heroku-badge)](https://dashboard.heroku.com/apps/fast-sea-58330)

## Installation for contributors
```
$ git clone git@github.com:Dddarknight/python-project-52.git
$ cd python-project-lvl3
$ pip install poetry
$ make install
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
