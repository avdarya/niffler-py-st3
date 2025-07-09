class Server:

    def __init__(self, env: str):
        self.base_api_url = {
            "dev": "http://gateway.niffler.dc:8090",
            "rc": "http://gateway.niffler.dc:8090"
        }[env]