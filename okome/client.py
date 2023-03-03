from requests.cookies import RequestsCookieJar
from okome.auth import Account
from okome import util
import urllib.parse
import requests
import json
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
        """Create an mail address automatically

        Returns:
            typing.Tuple[bool, str]: Successed, Mail address
        """
        
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
       
    def create_mail_manually(
            self, 
            username: typing.Optional[str] = None, 
            domain: typing.Optional[str] = None
            ) -> typing.Tuple[bool, str]:
        """Create an mail address manually

        Args:
            username (str): (Optional)
            domain (str): (Optional)

        Returns:
            typing.Tuple[bool, str]: Successed, Mail address
        """
        
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
        """Create an mail address with expiration date

        Returns:
            typing.Tuple[bool, str]: Successed, Mail Address
        """
        
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
        """Gets a list of addresses

        Returns:
            list[Address]: List of addresses
        """
        
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
        """Delete an address by id

        Args:
            id (str): Address ID
        """

        params = {
            "action": "delAddrList",
            "nopost": 1,
            "num_list": id + ","
        }
        
        requests.get("https://m.kuku.lu/index._addrlist.php", headers=util.get_headers(), params=params
                                , cookies=self._get_cookies())

    def get_credentials(self) -> typing.Tuple[str, str]:
        """Gets the account's credentials

        Returns:
            typing.Tuple[str, str]: Account's id and password
        """
        res = requests.get("https://m.kuku.lu/",headers=util.get_headers(),cookies=self._get_cookies())
        id = re.search('<div id="area_numberview" style="white-space:wrap;word-break:break-all;">(\w*)<\/div>', res.text)
        password = re.search('<span id="area_passwordview_copy">(\w*)<\/span>',res.text)
                
        if (id is None) or (password is None):
            return None
        return id.group(1), password.group(1)

    def get_address_id(self, target: str) -> str:
        """Gets the address id

        Args:
            target (str): Mail Address

        Returns:
            str: ID of the address
        """
        addresses = self.get_address_list()
        for address in addresses:
            if address.address.lower() == target.lower():
                return address.id
        return None  
    
    def get_inbox(self, page: typing.Optional[int] | None, filter: typing.Optional[str] | None) -> list[Mail]:
        """Gets the inbox mails

        Args:
            page (typing.Optional[int] | None): (Optinal)
            filter (typing.Optional[int] | None): Mail Address (Optinal)

        Returns:
            list[Mail]: List of mails. You can get content by get_mail_data()
        """
        params = {
            "nopost": 1,
            "csrf_token_check": self._get_csrf_token(),
            "csrf_subtoken_check": self._get_subtoken()
        } 
        
        cookies = self._get_cookies()
        
        if page is not None:
            params["page"] = page
        
        if filter is not None:
            data = json.dumps({
                "filter_mailaddr": filter,
            })
            cookies: RequestsCookieJar = self._get_cookies().copy()
            cookies.set("cookie_filter_recv2", data)

        res = requests.get(f"https://m.kuku.lu/recv._ajax.php", headers=util.get_headers(), cookies=cookies
                           , params=params)
        
        results = []
        mails = re.findall("openMailData\('(\d+)',\s*'(\w+)',\s*'([\w=%\.;\-]+)'", res.text)
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
    
    def get_mail_data(self, num: str, key: str) -> str:
        """Gets the mail data 

        Args:
            num (str): use get_inbox
            key (str): use get_inbox

        Returns:
            _type_: Html content
        """
        params = {
            "num": num,
            "key": key,
            "noscroll": 1
        }
        
        response = requests.post("https://m.kuku.lu/smphone.app.recv.view.php", headers=util.get_doc_headers()
                                 , cookies=self._get_cookies(), params=params)
        return response.text

    def send_mail(self, send_from: str, send_to: str) -> bool:
        """Sends an empty mail
        
        Returns:
            bool: Successed
        """
        sendtemp, filehash = self._get_hashes()
        
        params = {
            "action": "sendMail",
            "ajax": "1",
            "csrf_token_check": self._get_csrf_token(),
            "sendmail_replymode": "",
            "sendmail_replynum": "",
            "sendtemp_hash": sendtemp,
            "sendmail_from": send_from,
            "sendmail_from_radio": send_from,
            "sendmail_to": send_to,
            "sendmail_subject": "",
            "sendmail_content": "",
            "sendmail_content_add": "",
            "file_hash": filehash
        }
        
        response = requests.post("https://m.kuku.lu/new.php", headers=util.get_headers(), 
                      cookies=self._get_cookies(), params=params)
        return response.json()["result"] == "OK"
    
    def _get_hashes(self) -> typing.Tuple[str, str]:
        response = requests.get("https://m.kuku.lu/new.php", cookies=self._get_cookies(), 
                     headers=util.get_doc_headers())
        
        sendtemp = re.search('sendtemp_hash=([\w]+)', response.text).group(1)
        filehash = re.search('file_hash=([\w]+)', response.text).group(1)
        
        return (sendtemp, filehash)
    
    def _get_cookies(self):
        return self.account.storage
    
    def _get_csrf_token(self):
        return self.account.csrf_token
    
    def _get_subtoken(self):
        return self.account.subtoken