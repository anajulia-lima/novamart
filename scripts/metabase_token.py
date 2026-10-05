# You'll need to install PyJWT via pip 'pip install PyJWT' or your project packages file

import jwt
import time


METABASE_SECRET_KEY = "df9da5fb03ee930730b7a363a2f71df67e28393518f3db9063b4c19465001eb5"

payload = {
  "resource": {"dashboard": 2},
  "params": {
    
  },
  "exp": round(time.time()) + (6000000 * 10) # 10 minute expiration
}
token = jwt.encode(payload, METABASE_SECRET_KEY, algorithm="HS256")

print(token)