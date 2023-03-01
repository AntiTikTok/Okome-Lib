from okome import auth
from okome import Client

account = auth.create_account()
client = Client(account)

success, mail = client.create_onetime_mail()

print("Mail: " + mail)