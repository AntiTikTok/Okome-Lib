from requests.cookies import RequestsCookieJar
import requests
from okome import util
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

def create_account() -> Account:
    res = requests.get("https://m.kuku.lu/", headers=util.get_doc_headers())
    csrf_token = res.cookies.get("cookie_csrf_token") 
    session_hash = res.cookies.get("cookie_sessionhash")
        
    account = Account(csrf_token, session_hash)
    subtoken = get_subtoken(account)
    account.set_subtoken(subtoken)
    
    return account 

def get_subtoken(account: Account) -> str:
    res = requests.get("https://m.kuku.lu/", headers=util.get_doc_headers(), cookies=account.storage)
    id = re.search("csrf_subtoken_check=(\w+)", res.text)
    if id is None:
        return None
    return id.group(1)