from pathlib import Path
from cryptography import x509
from cryptography.hazmat.primitives import serialization
from sha256 import SHA256

cert_path = Path("crypto_artifacts/certificate_kse.crt")
target_hash = (
    "36:A7:60:17:49:FB:AD:99:5A:97:79:E2:C8:A2:B6:89:"
    "1D:03:98:70:FF:40:E3:4B:E2:0D:A3:A4:BF:CC:EB:E0"
)

pem_data = cert_path.read_bytes()

cert = x509.load_pem_x509_certificate(pem_data)
der_data = cert.public_bytes(serialization.Encoding.DER)

computed_hex = SHA256().hash(der_data)

computed_hex_with_colons = ":".join(
    computed_hex[i:i + 2].upper()
    for i in range(0, len(computed_hex), 2)
)

print("Results: ")
print(f"Target:   {target_hash}\nComputed: {computed_hex_with_colons}")

normalized_computed = computed_hex_with_colons.replace(":", "").lower()
normalized_target = target_hash.replace(":", "").lower()

print("\nNormalized: ")
print(f"Target:   {normalized_target}\nComputed: {normalized_computed}")
