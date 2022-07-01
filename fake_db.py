class FakeDB:
    _db = []

    def set(self, installation_dict):
        self._db.append(installation_dict)

    def get_all(self):
        return [installation_dict["bot_token"] for installation_dict in self._db]
