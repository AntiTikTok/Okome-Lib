from requests.cookies import RequestsCookieJar
from okome import util
import requests
import re

class Account:
    def __init__(self, csrf_token: str, session_hash: str):
        self.csrf_token = csrf_token
        self.session_hash = session_hash
        self.subtoken = None
        # create a storage
        self.storage = RequestsCookieJar()
        self.storage.set("cookie_csrf_token", csrf_token, domain="m.kuku.lu", path="/")
        self.storage.set("cookie_sessionhash", session_hash, domain="m.kuku.lu", path="/")

    def set_subtoken(self, subtoken: str):
        self.subtoken = subtoken