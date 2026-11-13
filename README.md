# 쿵짝

지방에도 무대는 있다. 보이지 않을 뿐.
동네 공연·전시·북토크를 발견하고, 다시 찾고, 직접 여는 앱 **쿵짝**의 시연용 프로토타입입니다.
「지역문제 해결 AI 바이브코딩 아이디어 경진대회」 결선(2026-11-27) 출품작입니다.

## 👀 프로토타입 보기

**[Colab에서 앱 화면 보기](https://colab.research.google.com/github/dylan6311-ship-it/kungjjak/blob/main/%EC%BF%B5%EC%A7%9D_%ED%94%84%EB%A1%9C%ED%86%A0%ED%83%80%EC%9E%85.ipynb)**

- 로그인이나 실행 없이 바로 휴대폰 화면이 보여요.
- 이 저장소의 `main`에 올라온 최신 버전이 그대로 보여요.
- 게시글과 팀·공간 이름은 모두 가상이고, 실제 결제는 일어나지 않아요.

## ✏️ 고치는 방법

앱은 **`index.html` 한 파일**이에요. 이 파일만 고치면 돼요.

> ⚠️ **Colab에서 고쳐서 "GitHub에 저장"하지 마세요.** 노트북은 `index.html`로 자동으로 만드는 사본이라, 노트북을 직접 고치면 다음 동기화 때 지워져요.

### 매번 이 순서로

| 순서 | 명령 | 왜 |
|---|---|---|
| 1. 받기 | `git pull` | 다른 사람 수정을 먼저 받아야 부딪치지 않아요 |
| 2. 고치기 | `index.html` 수정 | 고친 뒤 브라우저로 열어 직접 눌러 보세요 |
| 3. 올리기 | `git add -A && git commit -m "무엇을 바꿨는지" && git push` | 끝나면 바로 올려요. 오래 쥐고 있을수록 부딪쳐요 |

- Claude Code를 쓰면 "최신본 받고 작업해 줘", "커밋하고 푸시해 줘"라고 말하면 돼요. 작업 규칙은 [`CLAUDE.md`](CLAUDE.md)에 있고 Claude가 알아서 읽어요.
- 작은 문구 수정은 GitHub 웹에서 `index.html`을 열고 연필(✏️) 아이콘으로 고쳐도 돼요.
- 올리고 1~2분 뒤 Colab 링크를 새로고침하면 반영돼 있어요.
- 같은 시간에 둘이 같은 화면을 고치면 부딪치기 쉬워요. **"지금 ○○ 화면 고치는 중"이라고 단톡방에 한 줄** 남겨 주세요.

### 처음 한 번만

```bash
git clone https://github.com/dylan6311-ship-it/kungjjak.git
cd kungjjak
```

푸시하려면 GitHub 로그인이 필요해요. 비밀번호로는 안 되니 GitHub CLI로 로그인하세요.

```bash
brew install gh          # Windows는 https://cli.github.com 에서 설치
gh auth login --hostname github.com --git-protocol https --web
gh auth setup-git
```

## 🆘 푸시가 안 될 때

| 메시지에 이런 말이 있으면 | 해결 |
|---|---|
| `rejected … (fetch first)` | 다른 사람이 먼저 올렸어요. `git pull --rebase` 후 다시 `git push` |
| `CONFLICT` | 같은 줄을 둘이 고쳤어요. 혼자 풀기 어려우면 Claude에게 "충돌 해결해 줘"라고 하거나 단톡방에 물어보세요 |
| `Password authentication is not supported` | 위 "처음 한 번만"의 `gh auth login` |
| `Permission … denied to 다른아이디` | 다른 계정으로 로그인돼 있어요. `gh auth login`으로 다시 로그인 |
| `Repository not found` | `gh auth status`로 로그인한 아이디 확인. 저장소 초대를 수락했는지도 확인 |
| 웹용 Claude Code에서 "읽기만 된다" | 저장소 주인에게 Claude GitHub 앱 접근 확인을 요청 |

## 📁 파일

| 파일 | 내용 |
|---|---|
| `index.html` | 앱 원본 (이것만 고치기) |
| `쿵짝_프로토타입.ipynb` | Colab용 사본 (자동 생성, 직접 고치지 않기) |
| `scripts/sync_notebook.py` | `index.html` → 노트북 변환 |
| `.github/workflows/sync-notebook.yml` | `index.html`이 올라오면 GitHub가 노트북을 자동으로 맞춤 |
| `CLAUDE.md` | AI 작업 규칙과 디자인 원칙 |
| `*.pdf`, `*.hwpx` | 기획 자료 |
| `캡처/` | 화면 캡처 |
