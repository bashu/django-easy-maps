# Repository Coverage

[Full report](https://htmlpreview.github.io/?https://github.com/bashu/django-easy-maps/blob/python-coverage-comment-action-data/htmlcov/index.html)

| Name                                        |    Stmts |     Miss |   Cover |   Missing |
|-------------------------------------------- | -------: | -------: | ------: | --------: |
| easy\_maps/\_\_init\_\_.py                  |        0 |        0 |    100% |           |
| easy\_maps/admin.py                         |       25 |       25 |      0% |      1-45 |
| easy\_maps/conf.py                          |       12 |        0 |    100% |           |
| easy\_maps/geocode.py                       |       16 |        4 |     75% |     23-27 |
| easy\_maps/models.py                        |       58 |        5 |     91% |6-7, 27, 57, 73 |
| easy\_maps/templatetags/\_\_init\_\_.py     |        0 |        0 |    100% |           |
| easy\_maps/templatetags/easy\_maps\_tags.py |       38 |        6 |     84% |18, 55-60, 63-68, 77 |
| easy\_maps/utils.py                         |       24 |        5 |     79% |     29-33 |
| easy\_maps/widgets.py                       |       12 |       12 |      0% |      1-21 |
| **TOTAL**                                   |  **185** |   **57** | **69%** |           |


## Setup coverage badge

Below are examples of the badges you can use in your main branch `README` file.

### Direct image

[![Coverage badge](https://raw.githubusercontent.com/bashu/django-easy-maps/python-coverage-comment-action-data/badge.svg)](https://htmlpreview.github.io/?https://github.com/bashu/django-easy-maps/blob/python-coverage-comment-action-data/htmlcov/index.html)

This is the one to use if your repository is private or if you don't want to customize anything.

### [Shields.io](https://shields.io) Json Endpoint

[![Coverage badge](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/bashu/django-easy-maps/python-coverage-comment-action-data/endpoint.json)](https://htmlpreview.github.io/?https://github.com/bashu/django-easy-maps/blob/python-coverage-comment-action-data/htmlcov/index.html)

Using this one will allow you to [customize](https://shields.io/endpoint) the look of your badge.
It won't work with private repositories. It won't be refreshed more than once per five minutes.

### [Shields.io](https://shields.io) Dynamic Badge

[![Coverage badge](https://img.shields.io/badge/dynamic/json?color=brightgreen&label=coverage&query=%24.message&url=https%3A%2F%2Fraw.githubusercontent.com%2Fbashu%2Fdjango-easy-maps%2Fpython-coverage-comment-action-data%2Fendpoint.json)](https://htmlpreview.github.io/?https://github.com/bashu/django-easy-maps/blob/python-coverage-comment-action-data/htmlcov/index.html)

This one will always be the same color. It won't work for private repos. I'm not even sure why we included it.

## What is that?

This branch is part of the
[python-coverage-comment-action](https://github.com/marketplace/actions/python-coverage-comment)
GitHub Action. All the files in this branch are automatically generated and may be
overwritten at any moment.