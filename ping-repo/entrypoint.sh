#!/bin/bash
set -e
set -o pipefail

if [[ -z "$GITHUB_TOKEN" ]]; then
	echo "Set the GITHUB_TOKEN env variable."
	exit 1
fi

if [[ -z "$GITHUB_REPOSITORY" ]]; then
	echo "Set the GITHUB_REPOSITORY env variable."
	exit 1
fi

URI=https://api.github.com
API_HEADER="Accept: application/vnd.github.everest-preview+json"
AUTH_HEADER="Authorization: token ${GITHUB_TOKEN}"

main() {
  echo 'in entrypoint.sh'
  echo 'Node version:' $(node -v)
  echo 'NPM version:' $(npm -v)
  echo 'Git version:' $(git --version)
  echo 'output of pwd:' && pwd
  echo 'output of ls:' && ls
  echo 'these are arguments set to the workflow' && echo ${*}

  curl -X POST -H "${AUTH_HEADER}" -H "${API_HEADER}" --data '{"event_type": "my_custom_webhook"}' "${URI}/repos/${GITHUB_REPOSITORY}/dispatches" || { echo "Error: cannot ping repo!";  exit 1; }
}

main
