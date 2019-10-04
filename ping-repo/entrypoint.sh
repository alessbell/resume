#!/bin/sh -l

sh -c "curl -XPOST -H \"Accept: \
application/vnd.github.everest-preview+json\"  \
-H \"Content-Type: application/json\" \
-H \"Authorization: token ${GITHUB_TOKEN}\" \
\"https://api.github.com/repos/${GITHUB_REPOSITORY}/dispatches\" \
--data '{\"event_type\": \"my_custom_webhook\"}'"
