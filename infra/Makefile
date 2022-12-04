project=api

up:
	docker-compose -f docker-compose.yml -p  $(project) up -d

down:
	docker-compose -f docker-compose.yml -p  $(project) down --remove-orphans

logs:
	docker-compose -f docker-compose.yml logs -f  


infra:
	python3 maneger_infra.py