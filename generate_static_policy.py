#!/usr/bin/env python3
"""
Staticly includes public key in the OPA policy for simplicity
"""
from string import Template
import argparse
import os

if __name__ == "__main__":
    parser = argparse.ArgumentParser('Generate demo tokens')
    parser.add_argument("template_input", type=str)
    parser.add_argument("public_key", type=argparse.FileType('r'))
    parser.add_argument("--issuer", "-i", default="trustedIdP")
    args = parser.parse_args()

    public_key = args.public_key.read()
    with open(args.template_input, 'r') as template_file:
        template = Template(template_file.read())

        template_output = "".join(os.path.splitext(args.template_input)[:-1])
        substitutions = {"idp": args.issuer, "public_key": public_key}
        with open(template_output, 'w') as output_file:
            output_file.write(template.substitute(**substitutions))