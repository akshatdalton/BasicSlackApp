class FakeDB:
    _db = {}

    def set(self, account_id, installation_dict):
        self._db[account_id] = installation_dict

    def get_all(self):
        return [
            dict(account_id=account_id, token=installation_dict["bot_token"])
            for account_id, installation_dict in self._db.items()
        ]
