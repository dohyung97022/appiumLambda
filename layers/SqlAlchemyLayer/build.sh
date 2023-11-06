echo Make sure to put the package names in requirements.txt

LAYER_NAME=Tweety

remove_library() {
  rm -r python/lib
}

deploy_version() {
  docker run -v "$PWD":/var/task "public.ecr.aws/sam/build-python$1" /bin/sh -c "pip install -r requirements.txt -t python/lib/python$1/site-packages/; exit"
  zip -r python.zip python
}

publish_aws() {
  echo publishing to aws
  aws lambda publish-layer-version --layer-name "$2" --description "" --zip-file fileb://./python.zip --compatible-runtimes $1
}

remove_library
deploy_version 3.7
deploy_version 3.8
deploy_version 3.9
publish_aws "python3.7 python3.8 python3.9" ${LAYER_NAME}