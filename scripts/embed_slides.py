"""index.html(앱)과 캡처 이미지를 발표.html 안에 그대로 넣는다.

Claude 앱의 내장 브라우저는 로컬 HTML을 파일 한 장짜리 사본으로 보여 줘서,
발표.html 옆의 index.html이나 캡처/ 이미지를 불러오지 못한다.
그래서 앱 전체를 gzip으로 줄여 발표.html 안의 <script type="text/plain" id="kj-app"> 블록에 base64로 넣고,
<img data-embed="캡처/파일.png"> 의 src 를 이미지 데이터로 채운다. 크롬에서 열어도 똑같이 동작한다.
바뀐 것이 없으면 파일을 건드리지 않는다.

사용: python3 scripts/embed_slides.py [--check]
  --check  쓰지 않고 다르면 종료 코드 1
"""
import base64
import gzip
import mimetypes
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
APP = ROOT / "index.html"
DECK = ROOT / "발표.html"

APP_BLOCK = re.compile(r'(<script type="text/plain" id="kj-app">)(.*?)(</script>)', re.S)
IMG = re.compile(r'(<img\b[^>]*?\bdata-embed=")([^"]+)("[^>]*?\bsrc=")([^"]*)(")')


def main() -> int:
    check = "--check" in sys.argv
    if not DECK.exists():
        print("발표.html 이 없습니다.", file=sys.stderr)
        return 2
    deck = DECK.read_text(encoding="utf-8")
    if not APP_BLOCK.search(deck):
        print('발표.html 에서 <script type="text/plain" id="kj-app"> 블록을 찾지 못했습니다.', file=sys.stderr)
        return 2

    # gzip 으로 줄여 넣는다. 내장 브라우저는 512KB 가 넘는 HTML 을 열지 못한다.
    app64 = base64.b64encode(gzip.compress(APP.read_bytes(), 9, mtime=0)).decode("ascii")
    out = APP_BLOCK.sub(lambda m: m.group(1) + app64 + m.group(3), deck, count=1)

    def img(m: re.Match) -> str:
        path = ROOT / m.group(2)
        if not path.exists():
            print(f"이미지가 없습니다: {m.group(2)}", file=sys.stderr)
            return m.group(0)
        mime = mimetypes.guess_type(path.name)[0] or "image/png"
        data = f"data:{mime};base64," + base64.b64encode(path.read_bytes()).decode("ascii")
        return m.group(1) + m.group(2) + m.group(3) + data + m.group(5)

    out = IMG.sub(img, out)

    if out == deck:
        print("발표.html 이 이미 index.html·캡처와 같습니다.")
        return 0
    if check:
        print("발표.html 에 넣은 앱이나 이미지가 최신이 아닙니다. python3 scripts/embed_slides.py 를 실행하세요.")
        return 1
    DECK.write_text(out, encoding="utf-8")
    print("발표.html 에 index.html 과 캡처 이미지를 다시 넣었습니다.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
