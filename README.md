# 푸드링크 배송 안내 에이전트: 실습 스타터

Track 2 (Copilot Coding · Vibe Coding) 학생용 실습 뼈대입니다. 도구 구현은 비어 있고, 연결 확인용 `ping` 도구만 동작합니다. 수업 중에 차시별로 채워 나갑니다.

새벽장터 푸드링크는 **가상의 기업**입니다. 데이터는 모두 가상이며 실제 기업, 거래처, 가격과 무관합니다.

## 시작하기

1. 이 폴더를 VS Code로 엽니다. (파일, 폴더 열기)
2. VS Code 아래쪽 터미널을 열고 한 줄씩 실행합니다.

Mac:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python scripts/check_env.py
```

Windows (PowerShell):

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python scripts\check_env.py
```

마지막 줄에서 "모두 정상입니다."가 나오면 준비가 끝났습니다. 화면을 캡처해 제출하세요.

3. `.vscode/mcp.json`을 열고 `foodlink` 위의 시작(Start)을 누르면 Copilot Agent 모드의 도구 목록에 `foodlink`가 나타납니다. Windows는 `.vscode/mcp.windows.json`의 내용을 `mcp.json`에 복사한 뒤 시작합니다.

자세한 설치 방법과 오류 해결은 학생용 사이트의 설치 가이드와 트러블슈팅 카드를 보세요. 사이트 주소는 강사가 알려 줍니다.

## 폴더 구성

| 경로 | 설명 |
|---|---|
| `logic.py` | 핵심 로직. `TODO`가 붙은 함수를 차시마다 채웁니다 |
| `server.py` | MCP 서버. 현재는 `ping`만 있고 3차시 이후에 도구를 추가합니다 |
| `data/orders.csv` | 가상 주문 120행 |
| `data/handoffs.json` | 담당자 이관 기록. 처음에는 `[]` |
| `tests/` | 단위 테스트 (`python -m pytest -q`) |
| `scripts/check_env.py` | 사전 환경 점검 |
| `scripts/make_data.py` | 가상 데이터를 다시 만듭니다. 이관 기록도 비워집니다 |
| `.vscode/` | MCP 서버 설정 |

## 주의

- `mcp` 패키지를 따로 업그레이드하지 않습니다. 2.x 버전에서는 예제 코드가 동작하지 않습니다. 반드시 `requirements.txt`대로 설치합니다.
- 서버 코드에 `print()`를 넣지 않습니다. 서버가 표준출력으로 통신하므로 연결이 끊어집니다.
- 실제 개인정보, API 키, 비밀번호를 코드나 채팅에 넣지 않습니다.
- 출처를 모르는 MCP 서버는 설치하지 않습니다.
