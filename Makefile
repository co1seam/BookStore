IMAGE-NAME ?= pup-manager

CONTAINER-NAME ?= pup-manager-container

PORT ?= 8000

PROJECT-DIR ?= ?(PWD)

build:
	sudo docker build -t $(IMAGE-NAME) .

run:
	sudo docker run $(IMAGE-NAME)

stop:
	docker stop $(CONTAINER-NAME)

clean: stop
	sudo docker rm $(CONTAINER-NAME)
	sudo docker rmi $(IMAGE_NAME)