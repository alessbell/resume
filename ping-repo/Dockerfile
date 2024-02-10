FROM alpine:latest

LABEL "com.github.actions.name"="Send a dispatch to Gatsby site"
LABEL "com.github.actions.description"="Trigger action in Gatsby site via GitHub API"
LABEL "com.github.actions.icon"="activity"
LABEL "com.github.actions.color"="yellow"

RUN apk --update add --no-cache \
  bash \
  curl

LABEL "repository"="http://github.com/obrien-k/resume"
LABEL "homepage"="http://github.com/actions"
LABEL "maintainer"="Kyle O'Brien <github@korin.codes>"

ADD entrypoint.sh /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
