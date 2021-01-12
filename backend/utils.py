import secrets
import security

ACTIVATION_TOKEN_LENGTH = 64


def generate_activation_token():
    return secrets.token_urlsafe(ACTIVATION_TOKEN_LENGTH)[:ACTIVATION_TOKEN_LENGTH]


def get_field(body, field):
    try:
        return body[field]
    except Exception as e:
        raise Exception(f'Field {str(e)} is missing.')


def get_user(request):
    try:
        token = request.headers.get('Authorization').split(" ")[1]
        return security.jwt_decode(token)
    except:
        raise Exception('Incorrect token.')
