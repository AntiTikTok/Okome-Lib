from okome import auth
from okome import Client

account = auth.create_account()
client = Client(account)

id, password = client.get_credentials()
print("Id: {}, Password: {}".format(id, password))