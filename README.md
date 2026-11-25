# MCP servers

A reference pack provided by the pytemplate-hub maintainer.

This pack creates a Python project that runs a [Model Context Protocol](https://modelcontextprotocol.io) server built on the official `mcp` SDK (2.x line). The server exposes your own typed Python functions as tools that AI clients can call. The generated tests call those tools through an in-process client session, so they run offline and do not start a process or open a port.

## What you get

The `tools` profile, with the project name `my-app`:

```text
my-app/
├── AGENTS.md
├── CLAUDE.md
├── README.md
├── pyproject.toml
├── my_app/
│   ├── __init__.py
│   ├── py.typed
│   ├── server.py
│   └── units.py
└── tests/
```

`server.py` holds the MCP server and two example tools, `word_count` and `convert_units`. `units.py` holds the plain conversion logic, with no MCP code. The `tools-http` profile has the same layout, plus `tests/test_http.py`, which runs the HTTP app in process.

## Profiles

| Profile | Kind | What it adds |
| --- | --- | --- |
| `tools` | service | An MCP server over stdio (`uv run <project>`). Tests list and call the tools through an in-process `mcp.Client`. |
| `tools-http` | service | The same tools over streamable HTTP at `/mcp`, on `127.0.0.1:8000` by default (`MCP_HOST`, `MCP_PORT`). A test runs the Starlette app from `streamable_http_app()` in process through an ASGI transport. |

Both profiles declare `mcp>=2.3,<3` and Python 3.11 or later.

## Create a project

```bash
uvx pytemplate-uv@latest create my-app -p tools -h yuxuzi/mcp-server@v1.1.0 -y
```

`-h` (`--hub`, pytemplate-uv 3.5 or later) reads the commit and digest that
[pytemplate-hub](https://yuxuzi.github.io/pytemplate-hub/) checked for this tag, and refuses the pack if
anything changed. For CI or offline use, copy the fully pinned command from the pack's listing there.

For HTTP, use `-p tools-http`. The hub's listing page adds `--template-commit` and `--template-digest` to pin the exact pack contents.

## What the generated checks run

Each generated project runs these, in order, and they must all pass:

- `uv sync`
- `uv run ruff check .` and `uv run ruff format --check .`
- `uv run mypy <package> tests` (strict)
- `uv run pytest` (offline)

## Security posture

- Tools run with the server's own permissions. The example tools read only their input.
- `tools` (stdio) has no authentication. The server trusts whichever client launches it.
- `tools-http` has no authentication either. It binds to `127.0.0.1` by default. Changing `MCP_HOST` exposes every tool to anyone who can reach the port, so put your own authentication and network controls in front of it first.
- The generated projects need no secrets, network access, or services. The checks do not review what your own tools do, and declared annotations such as `read_only_hint` are hints to clients, not a sandbox.

## Customizing

Fork this repository or edit the generated project. To add a tool, write a typed function with a docstring, decorate it with `@server.tool()`, and test it through the in-process client. Raise `ToolError` for failures you expect. The generated `AGENTS.md` describes the same steps for coding agents.

When you publish your own copy, tag it and give users the tag with `--template-ref`.

## Versions

The pack was built and checked against `mcp` 2.3.0. The SDK's high-level server API changed in the 2.x line (for example, `FastMCP` became `MCPServer`), so the pin excludes 3.x until it has been checked.

## License

MIT. See [LICENSE](LICENSE).
