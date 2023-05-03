# Extension for Python KiteConnect API from Zerodha

## Note: This repository is a clone of the original repository from GitLab(https://gitlab.com/algo2t/kiteext) and is now hosted on GitHub. All credits and copyrights belong to their respective owner.

## Installation

### Make sure that git is installed on your system

* `python -m pip install -U git+https://gitlab.com/algo2t/kiteext.git`


## Usage

```python

# Check config.py example

from config import username, password, secret, enctoken
from kiteext import KiteExt

kite = KiteExt()

kite.login_with_credentials(userid=username, password=password, secret=secret)

print(kite.profile())

# Store token to enctoken.txt

with open('enctoken.txt', 'w') as wr:
    wr.write(kite.enctoken)

```

## `config.py` example

```python

username='YourUsernameAB1234'
password='YourSecretPassword'
secret='YourSecretFromExtAuth32Chars'
enctoken=None

try:
    enctoken = open('enctoken.txt', 'r').read().rstrip()
except Exception as e:
    print('Exception occurred :: {}'.format(e))
    enctoken = None

```

## Usage existing `enctoken.txt`

```python
import config
from kiteext import KiteExt

# providing userid is must either in KiteExt or in set_headers method
kite = KiteExt(userid=config.username)
kite.set_headers(config.enctoken)

```

```python

# providing userid is must either in KiteExt or in set_headers method
kite = KiteExt()
kite.set_headers(config.enctoken, userid=config.username)

```

## Ticker

* Once `kite` object is created then creating ticker is very easy

```python

kws = kite.ticker()

```



## Alerts API

```python
z = KiteExt()

z.login_using_enctoken(userid= 'YOURUSEDID', public_token='PUBLICTOKEN', enctoken='ENCTOKEN' )

# OR LOGIN USING BELOW FUNCTION
# z.login_with_credentials(userid='YOURUSEDID',password='YOURPASSWORD',pin=int(input("Your Totp here: ")))

am = AlertManagement(kwc=z)

alert_response = am.create_alert_on_value(
                    name=  'API-Price-Below',
                    lhs_exchange='NSE',
                    lhs_tradingsymbol='MCX',
                    lhs_attribute=AlertAttributes.LAST_TRADED_PRICE,
                    operator=Operations.LESS_THAN,
                    rhs_constant=1440.85
                )
print(alert_response)


```

With the above change you'll get alert on your active login sessions i.e., be it Mobile, Browser or any device

But if you want capture the alert by your self and send it to your favorite messaging apps/bots you need have your own `on_message` callback defined

Example
```python
def  on_message(ws, payload, is_binary):
    # Parse text messages  
    if not is_binary:
        try:
            data = json.loads(payload)
            if data['type']  == 'message' and 'Triggered' in data['data']:
                print("Alert Message ===>")
                print(data)
        except ValueError:
            return
    
```
