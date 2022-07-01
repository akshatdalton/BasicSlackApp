# BasicSlackApp
A basic Slack app setup with FastAPI

# Setup
`pip install -r requirements.txt`

```.bash
# -- OAuth flow -- #
export SLACK_SIGNING_SECRET=***
export SLACK_CLIENT_ID=111.111
export SLACK_CLIENT_SECRET=***
export SLACK_SCOPES=chat:write
```

# Resources:
- https://github.com/slackapi/bolt-python/tree/main/examples/fastapi
- https://slack.dev/python-slack-sdk/oauth/
- https://www.youtube.com/watch?v=aycTE75-2Gc
- https://api.slack.com/methods/chat.postMessage
- https://slack.dev/bolt-python/concepts#authenticating-oauth
- https://github.com/Idadelveloper/OAuth2-Slack-App/blob/main/app.py
- https://slack.dev/python-slack-sdk/oauth/
- https://slack.dev/python-slack-sdk/oauth/index.html#app-installation-flow
- https://slack.dev/bolt-python/concepts#authorization
- https://github.com/slackapi/bolt-python/issues/590
