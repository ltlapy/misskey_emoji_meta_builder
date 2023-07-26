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
        description="주어진 경로로 이모지 생성을 위한 메타데이터를 작성합니다."
    )
    parser.add_argument("path", type=str, help="이모지 파일 디렉토리")
    parser.add_argument("-c", "--category", type=str, help="이모지 카테고리명 (선택)")
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        help="json 출력 경로, 지정하지 않으면 화면 또는 표준 출력으로 내보냅니다",
    )
    parser.add_argument("--local", action='store_true',
                        help="이모지를 로컬 전용으로 지정합니다.")

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
        print("오류: 경로를 찾을 수 없습니다 -", path)
        return
    
    # validate emojiname
    filename_rule = re.compile(r'^[a-zA-Z0-9_]+?([a-zA-Z0-9\.]+)?$')
    
    filename_failed = [f for f in files if filename_rule.match(f) is None]
    
    if len(filename_failed) > 0:
        for filename in filename_failed:
            print("오류: 파일명 검증 실패:", filename, file=stderr)
        print("오류: 파일명은 영문자 대소문자, 숫자, 언더바(_)로 이루어져 있어야 합니다.", file=stderr)
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
