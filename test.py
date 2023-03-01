from okome import auth, Client, Account

account = Account("d1bd941ed84b766f487698ee1ab21000", "SHASH%3A475267dae23951155e338ab5dd051221")
client = Client(account)

mails = client.get_inbox()
for mail in mails:
    print("Sender: {}, To: {}".format(mail.sender, mail.to))