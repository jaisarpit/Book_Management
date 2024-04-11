import secrets

# Generate a secure random string of bytes
secret_key = secrets.token_hex(32)  # Generate a 256-bit (32-byte) hex-encoded token

print(secret_key)