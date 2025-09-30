#!/bin/sh -l
# Build Image
if [ $(docker images local_action_runner:v1 | wc -l) -lt 2 ]
then
  echo "Building new image.."
  docker build -t local_action_runner:v1 -f .dev_docker/ActionDockerFile .github
else
  echo "Runner image exists. Skip the build..."
fi
docker run --rm --name local_actions  \
    -v $(pwd):/app --entrypoint "/bin/bash" \
    local_action_runner:v1 \
    -c "python .github/default/code_similarity/code_similarity.py src --th 80"
echo "Done"