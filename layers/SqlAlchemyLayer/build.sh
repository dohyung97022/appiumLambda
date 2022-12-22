echo Make sure to put the package names in requirements.txt
echo Do you want to build python version 3.7? [y/n]
read install3_7
echo Do you want to build python version 3.8? [y/n]
read install3_8

layer_name=SqlAlchemyLayer

if [ "$install3_7" == "y" ]; then
  echo installing 3.7
  docker run -v "$PWD":/var/task "public.ecr.aws/sam/build-python3.7" /bin/sh -c "pip install -r requirements.txt -t python/lib/python3.7/site-packages/; exit"
fi

if [ "$install3_8" == "y" ]; then
  echo installing 3.8
  docker run -v "$PWD":/var/task "public.ecr.aws/sam/build-python3.8" /bin/sh -c "pip install -r requirements.txt -t python/lib/python3.8/site-packages/; exit"
fi

zip -r python.zip python

echo publishing to aws

if [ "$install3_7" == "y" ] && [ "$install3_8" == "y" ]; then
  aws lambda publish-layer-version --layer-name "$layer_name" --description "" --zip-file fileb://./python.zip --compatible-runtimes python3.7 python3.8
elif [ "$install3_8" == "y" ]; then
  aws lambda publish-layer-version --layer-name "$layer_name" --description "" --zip-file fileb://./python.zip --compatible-runtimes python3.8
elif [ "$install3_7" == "y" ]; then
  aws lambda publish-layer-version --layer-name "$layer_name" --description "" --zip-file fileb://./python.zip --compatible-runtimes python3.7
fi
