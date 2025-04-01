from argon2 import PasswordHasher
ph = PasswordHasher()

def hash_password(ptxt: str) -> str:
    return str(ph.hash(ptxt))