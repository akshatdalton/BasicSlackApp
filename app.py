import os
from urllib.parse import urljoin

import uvicorn
from fastapi import FastAPI, Request
from slack_bolt import App
from slack_bolt.adapter.fastapi import SlackRequestHandler
from slack_bolt.oauth.oauth_settings import OAuthSettings
from slack_sdk.oauth.installation_store import Installation, InstallationStore
from starlette.datastructures import URL

from fake_db import FakeDB

fake_db = FakeDB()


class MyInstallationStore(InstallationStore):
    def __init__(self) -> None:
        self._account_id = None
        super().__init__()

    def set_account_id(self, account_id) -> None:
        self._account_id = account_id

    def _reset_account_id(self) -> None:
        self._account_id = None

    def save(self, installation: Installation):
        if self._account_id is None:
            raise ValueError("Expected account_id")

        fake_db.set(self._account_id, installation.to_dict())
        print("account_id = ", self._account_id)
        print("installation = ", installation.to_dict())
        self._reset_account_id()


installation_store = MyInstallationStore()

app = App(
    name="BasicApp",
    raise_error_for_unhandled_request=True,
    signing_secret=os.environ["SLACK_SIGNING_SECRET"],
    installation_store=installation_store,
    # Following `install_page_rendering_enabled` ensures that
    # user doesn't have to click on `Add to Slack` button twice.
    # They will be directly redirected to `https://slack.com/oauth/v2/authorize` page.
    oauth_settings=OAuthSettings(install_page_rendering_enabled=False),
)
app_handler = SlackRequestHandler(app)


@app.error
def custom_error_handler(error, body, logger):
    logger.exception(f"Error: {error}")
    logger.info(f"Request body: {body}")


api = FastAPI()


############## BAD #############################################

# @api.get("/slack/install")
# async def install(req: Request):
#     return await app_handler.handle(req)


# @api.get("/start_auth_flow/{account_id}")
# async def start_auth_flow(account_id: str):
#     # Check if this `account_id` is valid or not.
#     installation_store.set_account_id(account_id=account_id)
#     RedirectResponse("/slack/install")


########### GOOD ##############################################


@api.get("/start_auth_flow/{account_id}")
async def start_auth_flow(account_id: str, request: Request):
    # Check if this `account_id` is valid or not.
    installation_store.set_account_id(account_id=account_id)
    # HACK: We don't want to expose `/slack/install` api since another user can
    # directly hit it and save their installation data with different user `account_id`
    # if this user started `App to Slack` flow but never completed it.
    request._url = URL(urljoin(str(request.base_url), app.oauth_flow.install_path))
    return await app_handler.handle(request)


@api.get("/slack/oauth_redirect")
async def oauth_redirect(req: Request):
    return await app_handler.handle(req)


@api.post("/messages")
async def send_messages(message: str):
    for data in fake_db.get_all():
        print("account_id = ", data["account_id"])
        result = app.client.chat_postMessage(
            token=data["token"], channel=os.environ["channel"], text=message
        )
        print("result = ", result)


if __name__ == "__main__":
    uvicorn.run("app:api", host="0.0.0.0", port=3000, reload=True)
