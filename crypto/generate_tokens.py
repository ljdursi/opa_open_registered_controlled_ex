#!/usr/bin/env python3
"""
Generates identity tokens for users Alice and Bob,
and a profyle_member claim token for Alice.
"""
from datetime import datetime, timedelta
import argparse
import cryptography
import jwt


def create_token(subject, private_key, issuer, issued, claims_dict=None):
    expires = issued + timedelta(hours=2)

    token = {
        'iat': issued,
        'nbf': issued,
        'exp': expires,
        'sub': subject,
        'iss': issuer
    }

    # add claims if provided
    if claims_dict:
        token = {**token, **claims_dict}

    return jwt.encode(token, private_key, algorithm='RS256')


def write_demo_tokens(private_key, issuer):
    now = datetime.utcnow()
    longago = datetime.utcnow() - timedelta(days=1)

    alice_identity = create_token('alice', private_key, issuer, now)
    bob_identity = create_token('bob', private_key, issuer, now)
    charlie_identity = create_token('charlie', private_key, issuer, now)
    alice_expired_identity = create_token('alice', private_key, issuer, longago)

    with open('alice_id.jwt', 'w') as f:
        f.write(alice_identity.decode('utf-8'))
    with open('bob_id.jwt', 'w') as f:
        f.write(bob_identity.decode('utf-8'))
    with open('charlie_id.jwt', 'w') as f:
        f.write(charlie_identity.decode('utf-8'))
    with open('alice_expired_id.jwt', 'w') as f:
        f.write(alice_expired_identity.decode('utf-8'))


if __name__ == "__main__":
    parser = argparse.ArgumentParser('Generate demo tokens')
    parser.add_argument("private_key", type=argparse.FileType('r'))
    parser.add_argument("--issuer", "-i", default="trustedIdP")
    args = parser.parse_args()

    private_key = "".join(args.private_key.readlines())
    write_demo_tokens(private_key, args.issuer)
