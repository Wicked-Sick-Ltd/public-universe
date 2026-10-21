# Repository Guidelines

## Project Structure

- `plugin.json` & `mcp.json` — canonical plugin metadata and remote Streamable HTTP MCP endpoint.
- `skills/` — seven astronomy workflows and bundled reference documents.
- `scripts/package.py` — generator, validator, and archive builder for multi-vendor client manifests.
- `tests/` — offline regression test suite (`unittest`).

## Development and Validation

Edit `plugin.json` and `mcp.json`, then regenerate and validate:

- `python3 scripts/package.py generate`
- `python3 scripts/package.py check`
- `python3 -m unittest discover -s tests -v`
- `git diff --check`
