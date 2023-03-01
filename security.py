import bcrypt


def encrypt_password(password: str, salt: bytes) -> bytes:
    return bcrypt.hashpw(password.encode("utf-8"), salt)


def check_password(password: str, salt: bytes, hashed_password: bytes) -> bool:
    return encrypt_password(password, salt) == hashed_password


def get_salt():
    return bcrypt.gensalt()
