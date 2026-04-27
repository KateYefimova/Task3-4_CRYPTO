import base64
from pathlib import Path

from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding

key_path = Path("crypto_artifacts/key.pub")
message = b"give my friend 2 bitcoins for a pizza"

key_data = key_path.read_bytes()
public_key = serialization.load_pem_public_key(key_data)

encrypted_message = public_key.encrypt(
    message,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None,
    ),
)

print(f"Key data: {key_data}\n\n")
print("Message:", message.decode("utf-8"))
print("Encrypted message: ", encrypted_message)
print("Encrypted message Base64: ", base64.b64encode(encrypted_message).decode("ascii"))
