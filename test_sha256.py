from sha256 import SHA256

def run_tests():
    sha = SHA256()
    
    test_data = [
        (b"", "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"),
        (b"abc", "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"),
        (b"abcdbcdecdefdefgefghfghighijhijkijkljklmklmnlmnomnopnopq", 
         "248d6a61d20638b8e5c026930c3e6039a33ce45964ff2167f6ecedd419db06c1")
    ]

    print("--- Реалiзацiя SHA-256 (FIPS 180-4) ---\n")
    
    for i, (msg, expected) in enumerate(test_data, 1):
        result = sha.hash(msg)
        is_correct = result == expected
        status = "PASSED" if is_correct else "FAILED"
        
        print(f"Test {i}:")
        print(f"  Input:    {msg if len(msg) < 50 else msg[:47] + b'...'}")
        print(f"  Expected: {expected}")
        print(f"  Result:   {result}")
        print(f"  Status:   {status}\n")

if __name__ == "__main__":
    run_tests()