#!/usr/bin/env bash

export REPO="rbroker/hello-py"
#TAG="$(date +%y.%m.%d-%H%M%S)"
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
curl -k -X POST "${CB_FLOW}/rest/v1.0/projects/MyProject/releases?releaseName=%20Hello%20Python%20Release%20${TAG}&pipelineName=hello-python&pipelineProjectName=MyProject" \
    -u ${CB_USER}:${CB_PASSWD} \
    -H "accept: application/json" \
    -d "{\"actualParameter\":[{\"actualParameterName\":\"appVersion\",\"value\":\"${TAG}\"}]}"

curl -k -X POST "${CB_FLOW}/rest/v1.0/releases?projectName=MyProject&releaseName=%20Hello%20Python%20Release%20${TAG}" \
     -u ${CB_USER}:${CB_PASSWD} \
     -H "accept: application/json" \
     -d "{}"
