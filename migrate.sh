poetry run python manage.py makemigrations zhackathon
poetry run python manage.py migrate
poetry run python manage.py loaddata zhackathon/fixtures/festival.json