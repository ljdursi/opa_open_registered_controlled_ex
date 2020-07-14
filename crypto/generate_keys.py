#!/usr/bin/env python3
"""
Generates public and private key for fake IdP
"""
from Crypto.PublicKey import RSA


def write_key_pair():
    """
    generate and output a key pair in PEM format
    """
    key = RSA.generate(2048)
    private_key = key.export_key()
    public_key = key.publickey().export_key()

    with open('private.pem', 'wb') as file_out:
        file_out.write(private_key)

    with open('public.pem', 'wb') as file_out:
        file_out.write(public_key)


if __name__ == "__main__":
    write_key_pair()
