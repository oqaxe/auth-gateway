# utils.py

import os
import logging
import jwt
from functools import wraps

# Set up logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set up JWT secret key
secret_key = os.environ.get('JWT_SECRET_KEY')

def authenticate_token(func):
    """Decorator to authenticate incoming JWT tokens"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            token = kwargs.get('token')
            if not token:
                raise ValueError('Missing token')
            payload = jwt.decode(token, secret_key, algorithms=['HS256'])
            kwargs['user_id'] = payload['user_id']
            return func(*args, **kwargs)
        except jwt.ExpiredSignatureError:
            logger.error('Token has expired')
            raise ValueError('Token has expired')
        except jwt.InvalidTokenError:
            logger.error('Invalid token')
            raise ValueError('Invalid token')
    return wrapper

def validate_password(password: str) -> bool:
    """Validate password strength"""
    if len(password) < 8:
        return False
    if not any(char.isdigit() for char in password):
        return False
    if not any(char.isalpha() for char in password):
        return False
    if not any(char in '!@#$%^&*()' for char in password):
        return False
    return True