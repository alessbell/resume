FROM alpine:latest

LABEL "com.github.actions.name"="Ping a different repository"
LABEL "com.github.actions.description"="Send a ping via GitHub API"
LABEL "com.github.actions.icon"="activity"
LABEL "com.github.actions.color"="yellow"

RUN apk add --no-cache \
  bash \
  ca-certificates \
  coreutils \
  curl \
  jq

LABEL "repository"="http://github.com/octocat/hello-world"
LABEL "homepage"="http://github.com/actions"
LABEL "maintainer"="Alessia Bellisario <github@bellisar.io>"

ADD entrypoint.sh /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
