from okome.auth import Account
from okome import util
import requests
import re
import typing

class Mail:
    def __init__(self, address: str, id: str):
        self.address = address
        self.id = id

class Client():
    def __init__(self, account: Account):
        self.account = account
       
    def create_mail(self) -> typing.Tuple[bool, str]:
        params = {
            'action': 'addMailAddrByAuto',
            'nopost': '1',
            'by_system': '1',
            'csrf_token_check': self._get_csrf_token(),
            'csrf_subtoken_check': self._get_subtoken(),
            'recaptcha_token': '',
        }
        
        response = requests.get('https://m.kuku.lu/index.php', params=params, cookies=self._get_cookies()
                                , headers=util.get_headers())
        result = response.text.split(":")
        if result[0] == "OK":
            return (True, result[1])
        else:
            return (False, None)           
       
    def create_mail_manually(self, username: str, domain: str) -> typing.Tuple[bool, str]:
        params = {
            'action': 'addMailAddrByManual',
            'nopost': '1',
            'by_system': '1',
            'csrf_token_check': self._get_csrf_token(),
            'newdomain': '',
            'newuser': '',
        }
        
        if username is not None:
            params['newuser'] = username
        if domain is not None:
            params['newdomain'] = domain
        
        response = requests.get('https://m.kuku.lu/index.php', params=params, cookies=self._get_cookies()
                                , headers=util.get_headers())
        result = response.text.split(":")
        if result[0] == "OK":
            return (True, result[1])
        else:
            return (False, None)
    
    def create_onetime_mail(self) -> typing.Tuple[bool, str]:
        params = {
            'action': 'addMailAddrByOnetime',
            'nopost': '1',
            'by_system': '1',
            'csrf_token_check': self._get_csrf_token(),
            'csrf_subtoken_check': self._get_subtoken(),
            'recaptcha_token': '',
        }
        
        response = requests.get('https://m.kuku.lu/index.php', params=params, cookies=self._get_cookies()
                                , headers=util.get_headers())
        result = response.text.split(":")
        if result[0] == "OK":
            mail = result[1].split(",")[0]
            return (True, mail)
        else:
            return (False, None)
    
    def get_address_list(self) -> typing.Tuple[bool, str]:
        params = {
            "nopost": 1
        }
        
        response = requests.get("https://m.kuku.lu/index._addrlist.php", headers=util.get_headers(), params=params
                                , cookies=self._get_cookies())
        
        results = []
        founds = re.findall(response.text, "<span id=\"area_mailaddr_(\w+)\">([\w@\.]+)")
        for found in founds:
            id = found[0]
            address = found[1]
            results.append(Mail(address, id))

        return results

    def get_account_info(self) -> list[typing.Tuple(str, str)]:
        res = requests.get("https://m.kuku.lu/",headers=util.get_headers(),cookies=self._get_cookies())
        pass
        
    def _get_cookies(self):
        return self.account.storage
    
    def _get_csrf_token(self):
        return self.account.csrf_token
    
    def _get_subtoken(self):
        return self.account.subtoken