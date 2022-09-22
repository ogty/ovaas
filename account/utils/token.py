import secrets


def generate_random_token() -> str:
    return secrets.token_hex().upper()
