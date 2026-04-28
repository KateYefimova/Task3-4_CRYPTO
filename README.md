# Task3-4_CRYPTO



## 1

SHA-256 - криптографічна хеш-функція стандарту FIPS 180-4, що належить до сімейства SHA-2. Вона перетворює вхідне повідомлення довільної довжини на 256-бітне (32-байтне) хеш-значення. Алгоритм базується на конструкції Меркла–Дамгора і використовує 64 раунди стиснення з константами, що виведені з кубічних коренів простих чисел.

Перевірка коректності реалізації проводилася на офіційних тестових векторах NIST. Усі три тести пройдено успішно

<img width="716" height="386" alt="image" src="https://github.com/user-attachments/assets/192da4df-35b3-4d10-a130-2d48bc657a65" />

Третій тестовий вектор є особливо важливим, оскільки повідомлення завдовжки 448 біт охоплює граничний випадок padding-у (повідомлення точно заповнює поле до довжини). Всі результати збігаються з еталонними значеннями NIST, що підтверджує коректність реалізації.

## 2

Необхідно підібрати випадковий 20-байтний бінарний префікс P до повідомлення M = "give my friend 2 bitcoinsfor a pizza" такий, щоб:

                                                        SHA-256(P || M) = "00000000" + ...
де "00000000" — 8 шістнадцяткових нулів, що відповідають 32 нульовим бітам на початку хешу. Ця задача є демонстрацією принципу Proof-of-Work, покладеного в основу протоколів Bitcoin.

Ймовірність того, що випадковий хеш починається з 32 нульових бітів, становить 1/2^32 ≈ 2.3 × 10^-10. Отже, в середньому потрібно ~4.3 мільярди спроб. При швидкості ~3 мільйони хешів/секунду Python-реалізацією - це приблизно 1400 секунд.

Скрипт містить дві функції: find_prefix() — з власною реалізацією SHA-256, та find_fast_prefix() — з використанням стандартної бібліотеки hashlib для максимальної швидкості. Обидві демонструють один і той самий підхід:

Після завершення пошуку програма виводить знайдений префікс та відповідний хеш:

<img width="722" height="272" alt="image" src="https://github.com/user-attachments/assets/65898124-1554-4339-b1ff-5f386d6772bc" />


## 3
Пара ключів згенерована командою:
```
openssl genpkey -algorithm RSA -out server.key -pkeyopt rsa_keygen_bits:8192
```
Розмір ключа 8192 біт обраний для забезпечення максимальної криптографічної стійкості. Файл server.key містить приватний ключ у форматі PKCS#8 (PEM), а також усю інформацію для відновлення відповідного публічного ключа.

Certificate Signing Request (CSR) сформовано командою:
```
openssl req -new -key server.key -out server.csr \
  -subj "/C=UA/L=Kyiv/O=KSE/CN=www.crypto.kse.ua/emailAddress=user@kse.org.ua"
  -nodes
```
CSR містить публічний ключ та метаінформацію про власника. Перевірка вмісту:
```
openssl req -text -noout -in server.csr
```
Результат перевірки CSR:
```
Certificate Request:
    Data:
        Version: 1 (0x0)
        Subject: C=UA, L=Kyiv, O=KSE, CN=www.crypto.kse.ua
                 emailAddress=user@kse.org.ua
        Subject Public Key Info:
            Public Key Algorithm: rsaEncryption
                Public-Key: (8192 bit)
        Attributes:
            (none)
    Signature Algorithm: sha256WithRSAEncryption
```

Самопідписаний сертифікат сформовано командою:
```
openssl x509 -req -sha256 -in server.csr -signkey server.key -out server.crt
```
Дослідження вмісту сертифіката:
```
openssl x509 -text -noout -in server.crt
```
Сертифікат є самопідписаним: поля Issuer та Subject збігаються, тобто він підписаний тим самим ключем, який засвідчує. Це типова практика для локального тестування та розробки. 

## 4

After tasks 1-3 we will get three special files:

- server.key (Our private key, which we must keep as secret)
- server.crt (Our certificate)
- server.csr (Request for certificate)

We send the request to the other team, and as a result, we have the signed certificate

## 5

In subtask 5 we need to sing our message «give my friend 2 bitcoins for a pizza» using the SHA-256 hash and also with RSA-PSS signature scheme.

$$\begin{aligned}
 \text{message} & \\
 \downarrow \text{   }& \text{ SHA-256}\\
 \text{bytes-message} & \\
 \downarrow \text{   }& \text{ RSA-PSS} \\
 \text{signature} & \\
\end{aligned}$$

First of all we substitute our message into `SHA256().hash` function and get hash in hex format so we transform it into bytes.
From our private key `server.key` we extract all private RSA params. Then we pull on public digits from private.
```commandline
n = public_numbers.n  # RSA modulus
e = public_numbers.e  # public exponent
d = private_numbers.d # private exponent
```
After that we use formula: `m^d mod n` where m is our bytes_message which was transformed into int.
For verification, we will use `s` (the resulting signature) public exponent `e` and `n`: `m' = s^e mod n` 
And If m and m' are not equals so somthing went wrong.

### Textbook RSA

Plain "textbook" RSA is not CPA-secure because it is deterministic: encrypting the same plaintext always yields the same ciphertext.
Also, textbook RSA it's a public-key encryption system. So it means that the attacker can know our public-key.
So attacker can easily attack textbook RSA.

1. Choose two distinct plaintext messages (say, A and B) and submit them to the challenger.
2. Receive an encrypted ciphertext c from the challenger.
3. Using the public key, encrypt A and B to obtain $c_A = E_{k_{pub}}(A) \text{ and } c_B = E_{k_{pub}}(B)$
4. Check which of $c_A$ and $c_B$ is equal to c. Since the encryption scheme is deterministic, one of them should be.

To make RSA secure against such attacks, we need to add padding with random bits before encryption. 
So after padding attacker will not get the same result again.

We see that **PKCS#v1.5** has many weaknesses such as:

$\star$ It is deterministic. \
$\star$ The hashed value can be extracted from the signature. \
$\star$ It has no formal security proof.

**RSA-PSS** can beat all these weaknesses. 

$\star$ It uses randomized signatures for the same message. (So it's rather probabilistic than deterministic) \
$\star$ We also can't anymore extract hash, because random salt  was added. \
$\star$ And it has a formal security proof of its security.


## 6

In subtask 6 we have the same message = «give my friend 2 bitcoins for a pizza». 

`key_data` hear is same text which place in `key.pub`, we use `serialization.load_pem_public_key` 
to translate ordinary text into the desired Python format that can be used for encryption.

```commandline
key_data = key_path.read_bytes()
public_key = serialization.load_pem_public_key(key_data)
```

After that we used special function `.encrypt()` and we pass on our message, and algorithm (hashes.SHA256()).

## 7

In subtask 7 we will use `crt.sh` service. We will look only in columns where Common Name = kse.ua.

![Знімок екрана 2026-04-27 о 11.45.15 пп.png](Images/kse_in_crt.png)

But this service has to mach data. So we will use this command:

```bush
curl -s 'https://crt.sh/?Identity=kse.ua&output=json' \
| jq '
[
  .[]
  | select((.common_name // "" | ascii_downcase) == "kse.ua")
]
| sort_by(.not_before)
| .[0]
'
```

We use `jq` to read all information from the website, and add `&output=json` in the end of the link.
Then we search for columns Common Name = kse.ua, and sort them $\downarrow$ (.not_before) and took only 1 certificate.

$\star$ "not_before": "2021-06-19T00:00:00", \
$\star$ "not_after": "2021-09-17T23:59:59",

For period, we need not_before ~~--~~ not_after. It's 90 days 23 hours 59 minutes and 59 seconds.

**In summary:**

$\star$ Fist certificate was issued: 2021-06-19 00:00:00. \
$\star$ It was valid until: 2021-09-17 23:59:59. \
$\star$ Period: approx 91 days.

## 8

In subtask 8 we гіу `openssl` to pull out certificate. 

```bush
openssl s_client -connect kse.ua:443 -servername kse.ua </dev/null 2>/dev/null \
  | openssl x509 -out crypto_artifacts/kse_current.crt  
```

**Then the entire eighth task we can reduce to xxx steps:**

$\star$ Read certificate and transform it onto required format \
$\star$ Calculate SHA-256 from certificate \
$\star$ Add ":" and compare results \
$\star$ (Additional) compare results without ":"

## Contribution

Halka Hanna

1. Working with tasks 5-8
2. Description in report of tasks 5-8

Kate Yefimova

1. Working with tasks 1-4
2. Description in report of tasks 1-4

## Reference

1. <https://medium.com/@keithacrawfordjr/rsaprivatekey-encryption-in-python-7c78ec254ceb>
2. <https://crypto.stackexchange.com/questions/47512/why-plain-rsa-encryption-does-not-achieve-cpa-security>
3. <https://billatnapier.medium.com/provable-secure-signatures-with-rsa-8c1ca7d68433>
4. <https://cryptography.io/en/latest/hazmat/primitives/asymmetric/rsa/>
5. <https://stackoverflow.com/questions/54318942/python-how-do-i-extract-public-key-from-a-cert-file>

## Interaction with AI

1. [Correction of bash formula in task 8](https://chatgpt.com/share/69effdda-fdf8-83eb-b766-e233e1eec1b0)
