# Z-Hackathon

## Installation

1. Install ``poetry`` from [here](https://python-poetry.org/docs/)
2. Run the dependency management
```sh
$> poetry install
```

## Database seeding
1. Either in a ``poetry shell`` or in a simple bash, run:   
```sh
$> poetry run python manage.py makemigrations zhackahton
$> poetry run python manage.py migrate
$> poetry run python manage.py loaddata zhackathon/fixtures/festival.json
```

2. You may also want to create admin user:
```sh
$> poetry run python manage.py createsuperuser
```
   
## OpenAPI

1. To get the OpenAPI documentation, run:
```sh
$> poetry run python manage.py spectacular --file openapi.yml
```

## Start
1. To start the project, run:
```sh
$> poetry run python manage.py runserver
```