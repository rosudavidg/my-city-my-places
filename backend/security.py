import hashlib
import binascii
import os
from get_docker_secret import get_docker_secret
import jwt


def hash_password(password):
    """Hash a password for storing."""
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'),
                                  salt, 100000)
    pwdhash = binascii.hexlify(pwdhash)
    return (salt + pwdhash).decode('ascii')


def verify_password(stored_password, provided_password):
    """Verify a stored password against one provided by user"""
    salt = stored_password[:64]
    stored_password = stored_password[64:]
    pwdhash = hashlib.pbkdf2_hmac('sha512',
                                  provided_password.encode('utf-8'),
                                  salt.encode('ascii'),
                                  100000)
    pwdhash = binascii.hexlify(pwdhash).decode('ascii')
    return pwdhash == stored_password


def jwt_encode(data):
    return jwt.encode(data, get_docker_secret(os.environ['AUTH_JWT_KEY']), algorithm="HS256")


def jwt_decode(token):
    return jwt.decode(token, get_docker_secret(os.environ['AUTH_JWT_KEY']), algorithms=["HS256"])
