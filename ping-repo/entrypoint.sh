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
API_VERSION=v3
PREVIEW_VERSION=everest
API_HEADER="Accept: application/vnd.github.${API_VERSION}+json; application/vnd.github.${PREVIEW_VERSION}-preview+json"
AUTH_HEADER="Authorization: token ${GITHUB_TOKEN}"

main() {
	# Validate the GitHub token.
	curl -o /dev/null -sSL -H "${AUTH_HEADER}" -H "${API_HEADER}" "${URI}/repos/${GITHUB_REPOSITORY}" || { echo "Error: Invalid repo, token or network issue!";  exit 1; }

  # Ping repo
  curl -o /dev/null -sSL -X POST -H "${AUTH_HEADER}" -H "${API_HEADER}" "${URI}/repos/${GITHUB_REPOSITORY}/dispatches" || { echo "Error: cannot ping repo!";  exit 1; }

	# # Get the check run action.
	# action=$(jq --raw-output .action "$GITHUB_EVENT_PATH")

	# # If it's not synchronize or opened event return early.
	# if [[ "$action" != "synchronize" ]] && [[ "$action" != "opened" ]]; then
	# 	# Return early we only care about synchronize or opened.
	# 	echo "Check run has action: $action"
	# 	echo "Want: synchronize or opened"
	# 	exit 0
	# fi
}

main
