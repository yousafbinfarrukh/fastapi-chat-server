from cryptography.fernet import Fernet

# Generate a key
key = Fernet.generate_key()
print(f"ENCRYPTION_KEY={key.decode()}")
