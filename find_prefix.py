import os
import time
from sha256 import SHA256
import hashlib

def find_prefix():
    sha = SHA256()
    message = b"give my friend 2 bitcoinsfor a pizza"
    target_prefix = "00000000" 
    
    print(f"Пошук префiкса для повiдомлення: '{message.decode()}'")    
    start_time = time.time()
    attempts = 0
    
    while True:
        prefix = os.urandom(20)
        
        current_hash = sha.hash(prefix + message)
        attempts += 1
        
        if current_hash.startswith(target_prefix):
            end_time = time.time()
            print(f"\nЗнайдено!")
            print(f"Префiкс (HEX): {prefix.hex()}")
            print(f"Результат хешу: {current_hash}")
            print(f"Кiлькiсть спроб: {attempts}")
            print(f"Час виконання: {end_time - start_time:.2f} секунд")
            return prefix, current_hash

def find_fast_prefix():
    message = b"give my friend 2 bitcoinsfor a pizza"
    
    target_prefix = "00000000"
    
    print(f"Пошук префiкса для: '{message.decode()}'")
    print(f"Цiль: хеш має починатися з {target_prefix}")
    print("-" * 50)

    start_time = time.time()
    attempts = 0
    last_print_time = start_time

    try:
        while True:
            prefix = os.urandom(20)
            h = hashlib.sha256()
            h.update(prefix)
            h.update(message)
            current_hash = h.hexdigest()
            
            attempts += 1

            if current_hash.startswith(target_prefix):
                end_time = time.time()
                total_time = end_time - start_time
                print(f"\n\nУСПIХ!")
                print(f"Префiкс (HEX): {prefix.hex()}")
                print(f"Хеш: {current_hash}")
                print(f"Всього спроб: {attempts}")
                print(f"Час: {total_time:.2f} сек.")
                print(f"Середня швидкiсть: {attempts / total_time:.0f} хеш/сек")
                break

            if attempts % 500000 == 0:
                now = time.time()
                elapsed = now - last_print_time
                speed = 500000 / elapsed if elapsed > 0 else 0
                print(f"Спроб: {attempts} | Швидкiсть: {speed:.0f} хеш/сек", end="\r")
                last_print_time = now

    except KeyboardInterrupt:
        print("\nПошук зупинено користувачем.")

if __name__ == "__main__":
    find_fast_prefix()