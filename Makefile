####################################################
# Makefile                                         #
# Contains make commands for common scripts        #
####################################################

# Starts container(s) in docker-compose.yaml
up:
	docker-compose -f docker-compose.yaml up -d

# Rebuild the docker image.
build:
	docker-compose -f docker-compose.yaml build && docker-compose -f docker-compose.yaml up -d

# Destroys container(s) in docker-compose.yaml and rebuilds them
upnew:
	docker-compose -f docker-compose.yaml build
	docker-compose -f docker-compose.yaml up -d

# Stops container(s) in docker-compose.yaml
down:
	docker-compose -f docker-compose.yaml down

# Execute migrations
migrate:
	docker exec -it task_manager_apiserver  flask db upgrade

# Runs unittests
test:
	docker exec -it task_manager_apiserver  coverage run -m pytest -v tests/

# Fetches logs for debugging
logs:
	docker-compose logs -f
