<!-- mcp-name: ai.backskills/backskills -->
# backskills-mcp

Back skills, because skills change and your agents should know.

A thin, stdlib-only MCP (stdio) client for [backskills.ai](https://backskills.ai): watch the skills and MCP servers your agent depends on, get version history and diffs, and ask what to chain next. Ranking is merit-only and never paid.

## Use the hosted server (no install)
Streamable HTTP endpoint: `https://backskills.ai/mcp`

## Or run locally
```bash
pipx run backskills-mcp     # or: uvx backskills-mcp
```
Client config:
```json
{"mcpServers":{"backskills":{"command":"uvx","args":["backskills-mcp"],"env":{"BACKSKILLS_KEY":"bsk_..."}}}}
```
Env vars:
- `BACKSKILLS_URL` (default `https://backskills.ai`)
- `BACKSKILLS_KEY` optional; if unset, a free key is registered on first tool call.

## Tools
register, search, watch, list_watches, changes, versions, weave_ask, weave_reference, usage.

This package only calls the public backskills.ai HTTP API. MIT licensed.
