import datetime
import jwt


def generate_token(duration: int, payload: dict, key: str) -> str:
    """Takes care of generating a token.
    
    :param duration: indicates the duration of the token in seconds
    :param payload: dict that contains the claims
    :param key: the key to encrypt the token, default to the secret_key of the app
    :raises KeyError: if the payload does not contain the key "exp"
    :return: the JWT 
    """
    payload["exp"] += datetime.timedelta(seconds=duration) 
    token = jwt.encode(payload, key, algorithm="HS256")
    return token

def extract_token(data: dict) -> str:
    """Takes care of extracting a token from the data passed as a parameter.
    
    :param data: the data that contains the token
    :raises Exception: if the data passed as a parameter does not contain an 'x-access-token' or 'Authorization' key
    :return: the token in string format
    """
    if "x-access-token" in data:
        token = data["x-access-token"]
    elif "Authorization" in data:
        token = data["Authorization"]
        if token[:6] == "Bearer":
            token = token[7:]
    else:
        raise Exception("Error extracting token, data parameter should be a dict containing a key 'x-access-token' or 'Authorization'.")
    
    return token
