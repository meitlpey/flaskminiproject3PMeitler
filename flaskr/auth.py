# auth.py

import hashlib
from werkzeug.security import generate_password_hash

def hash_password(password):
    return generate_password_hash(password, method='sha256')