import secrets

secret_key = secrets.token_urlsafe(32)  # 32 bytes
print(secret_key)