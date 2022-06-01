#!/usr/bin/env bash

export REPO="rbroker/hello-py"
TAG="$(date +%y.%m.%d-%H%M%S)"
if [ -z "${TAG}" ]
then
  echo "VERSION not set"
  exit -1
fi
echo "Version = ${TAG}"
IMAGE="${REPO}:${TAG}"

echo "docker build -t ${IMAGE} -f Dockerfile ."
docker build -t ${IMAGE} -f Dockerfile .
docker login --username $DOCKER_USER --password $DOCKER_PASSWORD docker.io
echo "docker push ${IMAGE}"
docker push ${IMAGE}
 
curl -k -X POST "${CB_FLOW}/rest/v1.0/releases?projectName=MyProject&releaseName=hello-app" \
     -u ${CB_USER}:${CB_PASSWD} \
     -H "accept: application/json" \
     -d "{\"pipelineParameter\":[{\"pipelineParameterName\":\"appVersion\",\"value\":\"${TAG}\"}]}"
