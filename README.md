# Exam MCP Server

Minimal Streamable HTTP MCP server exposing exactly one tool: `solve_challenge`.

For every HTTP request, middleware reads `X-Exam-Challenge` from that request's headers.
The tool returns the first 16 lowercase hex characters of SHA-256 of:
`challenge:24f2007269@ds.study.iitm.ac.in`

The tool takes no arguments, so its input schema has no required properties.

## Deploy on Render

1. Upload `app.py`, `requirements.txt`, and `render.yaml` to a GitHub repository.
2. In Render, select **New + > Blueprint** and connect the repository, or create a Python Web Service manually.
3. For a manual service:
   - Build command: `pip install -r requirements.txt`
   - Start command: `uvicorn app:app --host 0.0.0.0 --port $PORT`
4. Wait for deployment to succeed.
5. Submit your public HTTPS service URL with `/mcp` appended, e.g. `https://YOUR-SERVICE.onrender.com/mcp`.

## Local run (optional)

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app:app --host 0.0.0.0 --port 8000
```

Local MCP endpoint: `http://localhost:8000/mcp`.

Do not add any other `@mcp.tool()` functions; the grader expects exactly one tool.
