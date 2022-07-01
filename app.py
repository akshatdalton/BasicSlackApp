import os

import uvicorn
from fastapi import FastAPI, Request
from slack_bolt import App
from slack_bolt.adapter.fastapi import SlackRequestHandler
from slack_sdk.oauth.installation_store import Installation, InstallationStore

from fake_db import FakeDB

fake_db = FakeDB()


class MyInstallationStore(InstallationStore):
    def save(self, installation: Installation):
        fake_db.set(installation.to_dict())
        print("installation = ", installation.to_dict())


installation_store = MyInstallationStore()

app = App(
    name="BasicApp",
    raise_error_for_unhandled_request=True,
    signing_secret=os.environ["SLACK_SIGNING_SECRET"],
    installation_store=installation_store,
)
app_handler = SlackRequestHandler(app)


@app.error
def custom_error_handler(error, body, logger):
    logger.exception(f"Error: {error}")
    logger.info(f"Request body: {body}")


api = FastAPI()


@api.get("/slack/install")
async def install(req: Request):
    return await app_handler.handle(req)


@api.get("/slack/oauth_redirect")
async def oauth_redirect(req: Request):
    return await app_handler.handle(req)


@api.post("/messages")
async def send_messages(message: str):
    for token in fake_db.get_all():
        result = app.client.chat_postMessage(
            token=token, channel=os.environ["channel"], text=message
        )
        print("result = ", result)


if __name__ == "__main__":
    uvicorn.run("app:api", host="0.0.0.0", port=3000, reload=True)
