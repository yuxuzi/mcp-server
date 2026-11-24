# Changelog

## 1.0.0

- Two profiles: `tools` (MCP server over stdio) and `tools-http` (the same server over streamable HTTP).
- Example tools `word_count` and `convert_units`, with tests that call them through an in-process client session.
- Built against `mcp` 2.3.0, pinned to `>=2.3,<3`.
