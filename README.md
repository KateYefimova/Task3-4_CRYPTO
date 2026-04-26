# Task3-4_CRYPTO



## 1

## 2

## 3

## 4

After tasks 1-3 we will get three special files:

- server.key (Our private key, which we must keep as secret 🤫)
- server.crt (Our certificate)
- server.csr (Request for certificate, inside which our public key is hidden) $\leftarrow$ Exactly what we will send to the other team.

## 5

In subtask 5 we need to sing our message «give my friend 2 bitcoins for a pizza» using the SHA-256 hash and also with RSA-PSS signature scheme.

$$\begin{aligned}
 \text{message} & \\
 \downarrow \text{   }& \text{ SHA-256}\\
 \text{bytes_message} & \\
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

## 6

## 7

## 8

## Contribution

