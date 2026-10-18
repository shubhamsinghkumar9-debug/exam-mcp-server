import hashlib
from contextvars import ContextVar
from typing import Optional

from starlette.datastructures import Headers
from starlette.types import ASGIApp, Receive, Scope, Send
from mcp.server.fastmcp import FastMCP

EMAIL = "24f2007269@ds.study.iitm.ac.in"
exam_challenge: ContextVar[Optional[str]] = ContextVar("exam_challenge", default=None)


class ExamHeaderMiddleware:
    """Capture the challenge header separately for each HTTP request."""
    def __init__(self, app: ASGIApp):
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        challenge = Headers(scope=scope).get("x-exam-challenge")
        token = exam_challenge.set(challenge)
        try:
            await self.app(scope, receive, send)
        finally:
            exam_challenge.reset(token)


mcp = FastMCP("Exam Challenge MCP", stateless_http=True, json_response=True)


@mcp.tool()
def solve_challenge() -> str:
    """Return the required hash derived from this HTTP call's challenge header."""
    challenge = exam_challenge.get()
    if challenge is None:
        raise ValueError("Missing X-Exam-Challenge HTTP header")
    digest = hashlib.sha256(f"{challenge}:{EMAIL}".encode("utf-8")).hexdigest()
    return digest[:16]


app = mcp.streamable_http_app()
app.add_middleware(ExamHeaderMiddleware)
