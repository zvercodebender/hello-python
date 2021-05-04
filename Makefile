REPO ?= danberg/hello-py
TAG ?= $(shell git rev-parse --short HEAD)
IMAGE := $(REPO):$(TAG)
LATEST_IMAGE := $(REPO):latest

all: docker-build docker-push timestamp

docker-build:
	docker build -t $(IMAGE) -f Dockerfile .
	docker tag $(IMAGE) $(LATEST_IMAGE)
docker-push:
	docker push $(IMAGE)
	docker push $(LATEST_IMAGE)
timestamp:
	date
