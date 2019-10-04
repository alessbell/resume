#!/bin/bash

main() {
  curl -XPOST -H "Accept: application/vnd.github.everest-preview+json" \
  -H "Content-Type: application/json" \
  -H "Authorization: token ${GITHUB_TOKEN}" \
  "https://api.github.com/repos/${REPO}/dispatches" \
  --data '{"event_type": "update_resume"}'
}

main
