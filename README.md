# Okome Client

m.kuku.lu ラッパー無料完全

スペシャルサンクス: Natsuneko

# Usage

方法 1

```python
from okome import auth, Client

account = auth.create_account()
client = Client(account)

success, mail = client.create_mail()
print("Mail: " + mail)
```

方法 2

```python
from okome import Account, Client

account = Account("cookie_csrf_token", "cookie_session_hash")
client = Client(account)

success, mail = client.create_onetime_mail()
print("Mail: " + mail)
```

# 便利メソッド

Client

```
create_mail: アドレスを自動作成して作成
create_mail_manually: アドレスを指定して作成
create_onetime_mail: 期限付きのアドレスを作成

get_address_list: アドレスリストを取得
get_address_id: アドレスのIDを取得
delete_address: アドレスを消去
get_credentials: ログイン情報を取得

get_inbox: インボックを取得
get_mail_data: メールのコンテントを取得
```

# ライセンス

MIT
