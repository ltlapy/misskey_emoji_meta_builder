#!/usr/bin/env python3

import os
import json
import argparse
import re
from sys import stderr
from datetime import datetime
from typing import List, Optional


def argument_parse():
    parser = argparse.ArgumentParser(
        description="Build emoji metadata with given local path"
    )
    parser.add_argument("path", type=str, help="The path for build")
    parser.add_argument("-c", "--category", type=str, help="emoji category name")
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        help="output file path, default to standard output if omitted",
    )
    parser.add_argument("--local", action='store_true',
                        help="Make emojis local-only")

    return parser.parse_args()


def build_meta(files: List[str], category: Optional[str], localonly: bool = False) -> dict:
    return {
        "generatedAt": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "emojis": [
            {
                "fileName": filename,
                "downloaded": True,
                "emoji": {
                    "name": '_'.join(filename.split(".")[:-1]),
                    "category": category,
                    "aliases": [""],
                    "isSensitive": False,
                    "localOnly": localonly
                    # 'license': "",  # nullable
                },
            }
            for filename in files
            if filename != "meta.json"
        ]
    }


def main():
    args = argument_parse()

    # get files with given directory
    path = args.path
    try:
        files = [f for f in os.listdir(path) if f != "meta.json"]
    except FileNotFoundError:
        print("Error: The path not found -", path)
        return
    
    # validate emojiname
    filename_rule = re.compile(r'^[a-zA-Z0-9_]+?([a-zA-Z0-9\.]+)?$')
    
    filename_failed = [f for f in files if filename_rule.match(f) is None]
    
    if len(filename_failed) > 0:
        for filename in filename_failed:
            print("Error: Filename validation failed:", filename, file=stderr)
        print("Error: All filename should be in ascii alphabets, numbers or underscore.", file=stderr)
        return

    # build meta
    meta = build_meta(files, args.category, args.local)
    if args.output:
        with open(args.output, "w") as f:
            json.dump(meta, f)
    else:
        print(json.dumps(meta))


if __name__ == "__main__":
    main()
