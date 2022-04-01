from datetime import datetime, timedelta, timezone
from ..config import jwtExpireMinutes, jwtSecretKey, jwtAlgorithm
import jwt


def generate_jwt(data: dict,
                 expire_delta: int = jwtExpireMinutes,
                 algorithm: str = jwtAlgorithm):
    """
    generate a jwt token
    :param data: payload data
    :param expire_delta: expiration in minutes
    :param algorithm: algorithm for JWT
    :return: a JWT
    """

    data['exp'] = datetime.now(tz=timezone.utc) + timedelta(minutes=expire_delta)
    return jwt.encode(data, key=jwtSecretKey, algorithm=algorithm)


def verify_jwt(token: str):
    """
    verify a jwt token
    :param token:
    :return: T / F,  data / err msg
    """
    try:
        decoded_data = jwt.decode(token, key=jwtSecretKey, algorithms=jwtAlgorithm)
        return True, decoded_data
    except jwt.ExpiredSignatureError:
        return False, "Token expired"
    except jwt.InvalidTokenError:
        return False, "Token Invalid"


if __name__ == "__main__":
    # token = generate_jwt({"name": "cli"})
    # print(token)
    # token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJuYW1lIjoiY2xpIiwiZXhwIjoxNjQ4NjgxOTQ5fQ.arhf_Q8vGGBAJwYewuR3ICkybCdj4L5WpYKMMqxPlwU"
    # print(verify_jwt(token))
    pass