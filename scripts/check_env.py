"""사전 환경 점검: 실행 후 '모두 정상' 화면을 캡처해 제출한다.

실행: python scripts/check_env.py   (가상환경을 활성화한 상태에서)
"""
import asyncio
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def step(ok, label, hint=""):
    print(("[OK]   " if ok else "[실패] ") + label)
    if not ok and hint:
        print("       -> " + hint)
    return ok


async def check_server():
    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client

    params = StdioServerParameters(command=sys.executable, args=[str(ROOT / "server.py")],
                                   env={"FOODLINK_NOW": "2026-11-21T09:00:00"})
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = [t.name for t in (await session.list_tools()).tools]
            pong = await session.call_tool("ping", {})
            return tools, pong.content[0].text


def main():
    results = [step(sys.version_info >= (3, 10), f"Python {sys.version.split()[0]} (3.10 이상 필요)",
                    "Python을 3.10 이상으로 설치하세요")]
    try:
        import mcp  # noqa: F401
        results.append(step(True, "mcp 패키지 설치됨"))
    except ImportError:
        results.append(step(False, "mcp 패키지 없음", "가상환경 활성화 후 pip install -r requirements.txt"))
        return print("\n점검 중단")
    results.append(step((ROOT / "data" / "orders.csv").exists(), "data/orders.csv 있음",
                        "python scripts/make_data.py 실행"))
    try:
        tools, pong = asyncio.run(check_server())
        results.append(step(pong == "pong", f"MCP 서버 연결 및 ping 응답 (도구 {len(tools)}개: {', '.join(tools)})"))
    except Exception as exc:  # 학생용 점검 스크립트라 모든 오류를 메시지로 보여준다
        results.append(step(False, f"MCP 서버 실행 실패: {exc!r}", "server.py가 단독으로 실행되는지 확인"))
    print("\n" + ("모두 정상입니다." if all(results) else "실패 항목을 해결한 뒤 다시 실행하세요."))


if __name__ == "__main__":
    main()
