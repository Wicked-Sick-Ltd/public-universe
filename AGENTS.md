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

## Cloud agent environment

Cursor Cloud Agents run `bash .cursor/install.sh` (see `.cursor/environment.json`). The script is idempotent and non-interactive. It requires Python 3.11 or newer and creates `.venv`. This repository has no lockfile and no third-party dependencies, so the virtualenv is not seeded with packages. There is no local server to start.

From the repository root, after install:

- `.venv/bin/python scripts/package.py check`
- `.venv/bin/python -m unittest discover -s tests -v`
- `.venv/bin/python scripts/package.py --help`
- `git diff --check`

Install, packaging, and the test suite stay offline. They do not read API keys or database URLs, and they do not call the remote MCP endpoint.
