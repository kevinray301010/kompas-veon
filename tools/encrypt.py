#!/usr/bin/env python3
"""Enkripsi halaman Kompas untuk PWA.

Pakai: python3 tools/encrypt.py INPUT.html KODE OUTPUT.json
AES-256-GCM, kunci dari PBKDF2-SHA256. Tanpa KODE, isinya tidak terbaca.
"""
import base64, json, os, sys
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes

ITER = 150000

def main():
    if len(sys.argv) != 4:
        sys.exit('pakai: encrypt.py INPUT.html KODE OUTPUT.json')
    src, code, out = sys.argv[1:]
    html = open(src, 'rb').read()
    if b'<html' not in html[:500].lower():
        sys.exit('ENKRIPSI GAGAL: input bukan halaman HTML')
    salt, iv = os.urandom(16), os.urandom(12)
    key = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=ITER).derive(code.encode())
    ct = AESGCM(key).encrypt(iv, html, None)
    e = lambda b: base64.b64encode(b).decode()
    json.dump({'v': 1, 'iter': ITER, 'salt': e(salt), 'iv': e(iv), 'ct': e(ct)}, open(out, 'w'))
    print('OK: %d byte terenkripsi' % len(ct))

if __name__ == '__main__':
    main()
