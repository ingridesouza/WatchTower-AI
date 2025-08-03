up: ; docker compose up -d --build
down: ; docker compose down
logs: ; docker compose logs -f --tail=200
migrate: ; docker compose exec web python manage.py migrate
createsuperuser: ; docker compose exec web python manage.py createsuperuser
collectstatic: ; docker compose exec web python manage.py collectstatic --noinput
