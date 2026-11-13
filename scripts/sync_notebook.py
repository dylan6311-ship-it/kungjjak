"""index.html 내용을 쿵짝_프로토타입.ipynb 에 그대로 반영한다.

원본은 index.html 이다. 노트북은 Colab 공유용 사본으로,
- 코드 셀의 page = r'''...''' 안에 HTML 전체가 들어 있고
- 실행하지 않아도 화면이 보이도록 출력(iframe srcdoc)도 미리 저장돼 있다.
이 스크립트는 둘 다 index.html 기준으로 다시 쓴다. 바뀐 것이 없으면 파일을 건드리지 않는다.

사용: python3 scripts/sync_notebook.py [--check]
  --check  쓰지 않고 다르면 종료 코드 1
"""
import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "index.html"
NB = ROOT / "쿵짝_프로토타입.ipynb"
IFRAME_STYLE = "width:100%;height:900px;border:0"


def lines(text: str) -> list[str]:
    return text.splitlines(keepends=True)


def main() -> int:
    check = "--check" in sys.argv
    page = SRC.read_text(encoding="utf-8")
    if "'''" in page:
        print("index.html 에 ''' 가 있어 노트북 문자열에 넣을 수 없습니다.", file=sys.stderr)
        return 2

    nb = json.loads(NB.read_text(encoding="utf-8"))
    cell = next(
        (c for c in nb["cells"] if c["cell_type"] == "code" and "page = r'''" in "".join(c["source"])),
        None,
    )
    if cell is None:
        print("노트북에서 page = r''' 셀을 찾지 못했습니다.", file=sys.stderr)
        return 2

    src = "".join(cell["source"])
    new_src = re.sub(r"page = r'''.*?'''", lambda _: f"page = r'''{page.rstrip(chr(10))}\n'''", src, count=1, flags=re.S)
    new_out = f'<iframe srcdoc="{html.escape(page.rstrip(chr(10)) + chr(10))}" style="{IFRAME_STYLE}"></iframe>'

    old_out = ""
    for o in cell.get("outputs", []):
        if "text/html" in o.get("data", {}):
            v = o["data"]["text/html"]
            old_out = "".join(v) if isinstance(v, list) else v

    if new_src == src and new_out == old_out:
        print("노트북이 이미 index.html 과 같습니다.")
        return 0
    if check:
        print("노트북이 index.html 과 다릅니다. python3 scripts/sync_notebook.py 를 실행하세요.")
        return 1

    cell["source"] = lines(new_src)
    cell["outputs"] = [{
        "output_type": "execute_result",
        "execution_count": cell.get("execution_count") or 1,
        "metadata": {},
        "data": {"text/html": lines(new_out), "text/plain": ["<IPython.core.display.HTML object>"]},
    }]
    NB.write_text(json.dumps(nb, ensure_ascii=False, indent=1), encoding="utf-8")
    print("노트북을 index.html 기준으로 갱신했습니다. Colab 공유본은 따로 반영해야 합니다.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
