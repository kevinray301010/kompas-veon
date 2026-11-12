#!/usr/bin/env python3
"""Enkripsi data JSON Ruang Strategi untuk PWA.

Pakai: python3 tools/encrypt_json.py STATE.json KODE strategi/data.enc.json
AES-256-GCM, kunci dari PBKDF2-SHA256 (format sama dengan encrypt.py).
"""
import base64, json, os, sys
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes

ITER = 150000

def main():
    if len(sys.argv) != 4:
        sys.exit('pakai: encrypt_json.py STATE.json KODE OUTPUT.json')
    src, code, out = sys.argv[1:]
    raw = open(src, 'rb').read()
    data = json.loads(raw)
    for k in ('question', 'thesis', 'chain', 'bets'):
        if k not in data:
            sys.exit('ENKRIPSI GAGAL: field %s tidak ada' % k)
    salt, iv = os.urandom(16), os.urandom(12)
    key = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=ITER).derive(code.encode())
    ct = AESGCM(key).encrypt(iv, json.dumps(data, ensure_ascii=False).encode(), None)
    e = lambda b: base64.b64encode(b).decode()
    json.dump({'v': 1, 'iter': ITER, 'salt': e(salt), 'iv': e(iv), 'ct': e(ct)}, open(out, 'w'))
    print('OK: %d byte terenkripsi' % len(ct))

if __name__ == '__main__':
    main()
