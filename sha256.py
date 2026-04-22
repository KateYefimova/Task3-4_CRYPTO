import struct

class SHA256:
    K = [
        0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
        0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
        0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
        0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
        0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
        0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
        0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
        0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208, 0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2
    ]

    @staticmethod
    def _rotr(x, n):
        return ((x >> n) | (x << (32 - n))) & 0xFFFFFFFF

    @staticmethod
    def _shr(x, n):
        return x >> n

    def _ch(self, x, y, z): return (x & y) ^ (~x & z)
    def _maj(self, x, y, z): return (x & y) ^ (x & z) ^ (y & z)
    def _sigma0(self, x): return self._rotr(x, 2) ^ self._rotr(x, 13) ^ self._rotr(x, 22)
    def _sigma1(self, x): return self._rotr(x, 6) ^ self._rotr(x, 11) ^ self._rotr(x, 25)
    def _s0(self, x): return self._rotr(x, 7) ^ self._rotr(x, 18) ^ self._shr(x, 3)
    def _s1(self, x): return self._rotr(x, 17) ^ self._rotr(x, 19) ^ self._shr(x, 10)

    def hash(self, message: bytes) -> str:
        orig_len_bits = len(message) * 8
        message += b'\x80'
        while (len(message) * 8) % 512 != 448:
            message += b'\x00'
        
        message += struct.pack('>Q', orig_len_bits)

        h0, h1, h2, h3, h4, h5, h6, h7 = (
            0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a,
            0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19
        )

        for i in range(0, len(message), 64):
            w = list(struct.unpack('>16L', message[i:i+64]))
            for t in range(16, 64):
                val = (self._s1(w[t-2]) + w[t-7] + self._s0(w[t-15]) + w[t-16]) & 0xFFFFFFFF
                w.append(val)

            a, b, c, d, e, f, g, h = h0, h1, h2, h3, h4, h5, h6, h7

            for t in range(64):
                t1 = (h + self._sigma1(e) + self._ch(e, f, g) + self.K[t] + w[t]) & 0xFFFFFFFF 
                t2 = (self._sigma0(a) + self._maj(a, b, c)) & 0xFFFFFFFF 
                h, g, f = g, f, e
                e = (d + t1) & 0xFFFFFFFF 
                d, c, b = c, b, a
                a = (t1 + t2) & 0xFFFFFFFF 

            h0 = (h0 + a) & 0xFFFFFFFF
            h1 = (h1 + b) & 0xFFFFFFFF
            h2 = (h2 + c) & 0xFFFFFFFF
            h3 = (h3 + d) & 0xFFFFFFFF
            h4 = (h4 + e) & 0xFFFFFFFF
            h5 = (h5 + f) & 0xFFFFFFFF
            h6 = (h6 + g) & 0xFFFFFFFF
            h7 = (h7 + h) & 0xFFFFFFFF

        return ''.join(f'{x:08x}' for x in (h0, h1, h2, h3, h4, h5, h6, h7))