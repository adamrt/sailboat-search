.PHONY: start
start:
	docker-compose up -d

.PHONY: logs
logs:
	docker-compose logs -f --tail=50

.PHONY: stop
stop:
	docker-compose down -v
