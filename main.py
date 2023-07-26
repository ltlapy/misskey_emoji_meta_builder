#!/usr/bin/env python3

import json
import os
import argparse
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

    return parser.parse_args()


def build_meta(files: List[str], category: Optional[str]) -> dict:
    # TODO: filename verification (/^[a-zA-Z0-9_]+?([a-zA-Z0-9\.]+)?$/)
    # TODO: emojiname verification (/^[a-zA-Z0-9_]+$/)
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
                    "localOnly": False
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

    meta = build_meta(files, args.category)
    if args.output:
        with open(args.output, "w") as f:
            json.dump(meta, f)
    else:
        print(json.dumps(meta))


if __name__ == "__main__":
    main()
