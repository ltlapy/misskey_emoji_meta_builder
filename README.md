# Misskey emoji packer
디렉토리에 있는 이미지 파일을 토대로 misskey에 업로드할 수 있는 형태의 meta.json을 생성합니다.
Python의 내부 라이브러리만 사용하며, 외부 라이브러리를 필요로 하지 않습니다.

## How to use
```plaintext
usage: main.py [-h] [-c CATEGORY] [-o OUTPUT] [--local] path

Build emoji metadata with given local path

positional arguments:
  path                  The path for build

options:
  -h, --help            show this help message and exit
  -c, --category CATEGORY
                        emoji category name
  -o, --output OUTPUT   output file path, default to standard output if omitted
  --local               Make emojis local-only
```

### 예시
> [사용 환경 설정](#사용-환경-설정)을 모두 실행한 상태라고 가정합니다
> 
> Pro tip: 작업 중인 폴더 경로를 쉽고 간편하게 입력하는 방법
>   1. 상위 폴더로 이동
>   2. 작업 중이던 파일을 cmd 창으로 끌고 오기
>   3. Profit!

- 같은 폴더의 `emojis` 폴더에 저장된 이모지 파일을 토대로 meta.json 생성
  - `py main.py -o meta.json emojis`
  - 생성된 `meta.json` 파일을 `emojis` 폴더로 옮긴 뒤, 상위 폴더 없이 그대로 압축해서 사용
- `D:\blobcat` 폴더에 저장된 이모지 파일을 토대로, 카테고리 명을 `blobcat`으로 지정하여 meta.json 생성
  - `py main.py -c "blobcat" -o meta.json "D:\blobcat"`
  - 생성된 `meta.json` 파일을 `emojis` 폴더로 옮긴 뒤, 상위 폴더 없이 그대로 압축해서 사용