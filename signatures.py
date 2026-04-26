from sha256 import SHA256

from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding, utils

private_key_path = "crypto_artifacts/server.key"
message = b"give my friend 2 bitcoins for a pizza"

with open(private_key_path, "rb") as f:
    private_key = serialization.load_pem_private_key(
        f.read(),
        password=None,
    )
public_key = private_key.public_key()

""" SHA-256 """

hex_message = SHA256().hash(message)
bytes_message = bytes.fromhex(hex_message)

print("Message: ", message.decode("utf-8"))
print("SHA-256: ", hex_message)

""" Textbook RSA """

private_numbers = private_key.private_numbers()
public_numbers = private_numbers.public_numbers

n = public_numbers.n
e = public_numbers.e
d = private_numbers.d

m = int.from_bytes(bytes_message, byteorder="big")
signature_int = pow(m, d, n) # same as m^d mod n

key_size_bytes = (private_key.key_size + 7) // 8
signature_textbook = signature_int.to_bytes(key_size_bytes, byteorder="big")

recovered_int = pow(signature_int, e, n)  # same as signature^e mod n
if recovered_int == m:
    print("\nTextbook RSA signature verified successfully!\n")
else:
    raise ValueError("Textbook RSA signature verification failed!")

print("Textbook RSA signature: ", signature_textbook)

""" RSA-PSS """

signature_pss = private_key.sign(
    bytes_message,
    padding.PSS(
        mgf=padding.MGF1(hashes.SHA256()),
        salt_length=padding.PSS.MAX_LENGTH,
    ),
    utils.Prehashed(hashes.SHA256()),
)

print("RSA-PSS after SHA-256 hash: ", signature_pss)
