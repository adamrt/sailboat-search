.PHONY: start
start:
	docker-compose up -d

.PHONY: logs
logs:
	docker-compose logs -f --tail=50

.PHONY: stop
stop:
	docker-compose down

.PHONY: clean
clean:
	docker-compose down -v

.PHONY: migrate
migrate:
	docker-compose run --rm app python manage.py migrate
