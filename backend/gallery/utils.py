import jwt
from django.conf import settings
from django.contrib.auth.models import User

def auth_header_to_user_id(access):
    access_token = access.split()[1]
    decoded_token = jwt.decode(access_token, settings.SECRET_KEY, algorithms=['HS256'])
    print(">>> auth_header_to_user_id.decoded_token:", decoded_token)
    user_id = decoded_token["user_id"]
    return decoded_token["user_id"]
