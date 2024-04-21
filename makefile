run-app:
	docker rm -f backend \
	&& docker rm -f pg-db \
	&& docker compose up -d --build

check-db:
	docker exec -it pg-db psql -U box -d pg-db

logs-be:
	docker logs backend -f

prune:
	docker system prune -af --volumes