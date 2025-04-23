#!/usr/bin/python3
# -*- coding: utf-8 -*-

import argparse
import os


SEARCH_SIG = b"SecureBoot"
PATCH_SIG = b"SecureBoom"


def patch_grub2(input_file, output_file):
    if not os.path.isabs(input_file):
        input_file = os.path.abspath(input_file)

    if not os.path.isabs(output_file):
        output_file = os.path.abspath(output_file)

    if not os.path.exists(input_file):
        print(f"[-] {input_file} is not exists.")
        return

    if input_file == output_file:
        print("[-] Output file is the same as input file")
        return

    old_content: bytes = open(input_file, "rb").read()

    offset = old_content.find(SEARCH_SIG)
    if offset == -1:
        print(f"[-] signature '{SEARCH_SIG.decode()}' is not found in {input_file}")
        return
    print(f"[*] Found signature at offset {offset:x}")
    new_content = old_content.replace(SEARCH_SIG, PATCH_SIG)
    open(output_file, "wb").write(new_content)
    print(f"[*] Done")


def main():
    try:
        parser = argparse.ArgumentParser(description="GRUB shim lock patcher")
        parser.add_argument(
            "-i",
            "--input",
            type=str,
            required=True,
            help=f"Input file path",
        )
        parser.add_argument(
            "-o",
            "--output",
            type=str,
            required=True,
            help=f"Output file path",
        )
        args = parser.parse_args()
        patch_grub2(args.input, args.output)
    except Exception as e:
        pass


if __name__ == "__main__":
    main()