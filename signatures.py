from sha256 import SHA256

from cryptography.hazmat.primitives import serialization

private_key_path = "crypto_artifacts/keys/server.key"

message = b"give my friend 2 bitcoins for a pizza"

with open(private_key_path, "rb") as f:
    private_key = serialization.load_pem_private_key(
        f.read(),
        password=None,
    )
public_key = private_key.public_key()

hex_message = SHA256().hash(message)
bytes_message = bytes.fromhex(hex_message)

print("Message:", message.decode("utf-8"))
print("SHA-256:", hex_message)
