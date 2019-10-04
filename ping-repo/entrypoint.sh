#!/bin/bash

main() {
  # echo 'in entrypoint.sh'
  # echo 'Node version:' $(node -v)
  # echo 'NPM version:' $(npm -v)
  # echo 'Git version:' $(git --version)
  # echo 'output of pwd:' && pwd
  # echo 'output of ls:' && ls
  # echo 'these are arguments set to the workflow' && echo ${*}
  echo 'token' ${GITHUB_TOKEN}
  echo 'github repo' ${GITHUB_REPOSITORY}
  echo 'repo' ${REPO}

  curl -XPOST -H "Accept: application/vnd.github.everest-preview+json" \
  -H "Content-Type: application/json" \
  -H "Authorization: token ${GITHUB_TOKEN}" \
  "https://api.github.com/repos/${REPO}/dispatches" \
  --data '{"event_type": "my_custom_webhook"}'
}

main
