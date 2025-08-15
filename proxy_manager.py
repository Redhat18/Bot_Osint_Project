import os
import random

class ProxyManager:
    def __init__(self):
        self.proxies = os.getenv("PROXY_LIST", "").split(",")

    def next(self):
        proxy = random.choice(self.proxies) if self.proxies else None
        if proxy:
            return {"http": f"socks5://{proxy}", "https": f"socks5://{proxy}"}
        return None
