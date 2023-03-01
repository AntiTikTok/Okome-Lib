from okome.auth import Account
from okome import util
import urllib.parse
import requests
import typing
import re

class Address:
    def __init__(self, address: str, id: str):
        self.address = address
        self.id = id

class Mail:
    def __init__(self, num: str, key: str, sender: str, to: str, subject: str):
        self.num = num
        self.key = key
        self.sender = sender
        self.to = to
        self.subject = subject

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
    
    def get_address_list(self) -> list[Address]:
        params = {
            "nopost": 1
        }
        
        response = requests.get("https://m.kuku.lu/index._addrlist.php", headers=util.get_headers(), params=params
                                , cookies=self._get_cookies())
        
        results = []
        founds = re.findall("<span id=\"area_mailaddr_(\w+)\">([\w@\.]+)", response.text)
        for found in founds:
            id = found[0]
            address = found[1]
            results.append(Address(address, id))

        return results

    def delete_address(self, id: str):
        params = {
            "action": "delAddrList",
            "nopost": 1,
            "num_list": id + ","
        }
        
        requests.get("https://m.kuku.lu/index._addrlist.php", headers=util.get_headers(), params=params
                                , cookies=self._get_cookies())

    def get_credentials(self) -> typing.Tuple[str, str]:
        res = requests.get("https://m.kuku.lu/",headers=util.get_headers(),cookies=self._get_cookies())
        id = re.search('<div id="area_numberview" style="white-space:wrap;word-break:break-all;">(\w*)<\/div>', res.text)
        password = re.search('<span id="area_passwordview_copy">(\w*)<\/span>',res.text)
                
        if (id is None) or (password is None):
            return None
        return id.group(1), password.group(1)

    def get_inbox(self) -> list[Mail]:
        params = {
            "nopost": 1,
            "csrf_token_check": self._get_csrf_token(),
            "csrf_subtoken_check": self._get_subtoken()
        } 

        res = requests.get(f"https://m.kuku.lu/recv._ajax.php", headers=util.get_headers(), cookies=self._get_cookies()
                           , params=params)
        
        results = []

        mails = re.findall("openMailData\('(\d+)',\s*'(\w+)',\s*'([\w=;%\.]+)'", res.text)
        subjects = re.findall('<span style=\"overflow-wrap: break-word;word-break: break-all;\">(.*)<\/span>|<span class=\"font_gray\" style=\"\">(.+)</span>'
                              , res.text)
        for i in range(len(mails)):
            mail = mails[i]
            num = mail[0]
            key = mail[1]
            a = urllib.parse.unquote(mail[2]).split(";")
            sender = a[0].split("=")[1]
            to = a[2].split("=")[1]
            subject = subjects[i][0]
            
            results.append(Mail(num, key, sender, to, subject))
        
        return results
        
    def _get_cookies(self):
        return self.account.storage
    
    def _get_csrf_token(self):
        return self.account.csrf_token
    
    def _get_subtoken(self):
        return self.account.subtoken