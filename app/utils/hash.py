import bcrypt


def hash_password(passwd: str) -> str:
  return bcrypt.hashpw(passwd.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')


def check_password(passwd: str, stored_passwd: str) -> bool:
  return bcrypt.checkpw(passwd.encode('utf-8'), stored_passwd.encode('utf-8'))
