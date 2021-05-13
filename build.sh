#!/usr/bin/env bash

export CLI_VERSION="10.0.0"
export REPO="rbroker/hello-py"
TAG="$(git rev-parse --short HEAD)"
#export VERSION="3.1.1"
if [ -z "${TAG}" ]
then
  echo "VERSION not set"
  exit -1
fi
echo "Version = ${TAG}"
IMAGE="${REPO}:${TAG}"

echo "docker build ${IMAGE} -f Dockerfile ."
docker build ${IMAGE} -f Dockerfile .
echo "docker push ${IMAGE}"
docker push ${IMAGE}
sed "s/{{image_tag}}/${TAG}/g" kubernetes/deployment.yaml > kubernetes/hello-python.yaml

if [ -z "${GET_LOCAL}" ]
then
  xl apply --file dai-deploy/hello-python-deploy.yaml --values version=$TAG
else
  curl -LO https://dist.xebialabs.com/public/xl-cli/$CLI_VERSION/linux-amd64/xl
  chmod +x xl
  ./xl apply --xl-deploy-url=$XLD_URL --xl-deploy-username=$XLD_USER --xl-deploy-password=$XLD_PASSWD --file dai-deploy/hello-python-deploy.yaml --values version=$VERSION
  rm xl
fi
#rm x.yaml
rm kubernetes/hello-python.yaml
