
docker build --target libra-reminder -t libra-reminder:latest  -f Docker/Dockerfile .
mkdir -p ${HOME}/tmp/lambda

docker run  -v ${HOME}/tmp/lambda:/tmp libra-reminder:latest



