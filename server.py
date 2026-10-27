"""새벽장터 푸드링크(가상) 배송 안내 MCP 서버.

주의: stdio 방식 MCP 서버는 표준출력(print)으로 통신한다.
디버깅 출력은 print() 대신 표준에러(sys.stderr)나 로그 파일을 쓸 것.
"""
from mcp.server.fastmcp import FastMCP

import logic

mcp = FastMCP("foodlink-delivery")


@mcp.tool()
def ping() -> str:
    """서버 연결 확인용. 'pong'을 반환한다."""
    return "pong"


# TODO (6차시) logic.py에서 구현한 함수를 도구로 노출한다.
# 도구의 docstring은 에이전트가 읽는 '사용 설명서'다. 언제 쓰는지, 무엇을 반환하는지 분명히 쓸 것.


if __name__ == "__main__":
    mcp.run()
