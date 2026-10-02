# Multi-vendor validation

Development acceptance record, 2026-10-02. Package checks and live service checks are separate.

## Repeatable local checks

```sh
python3 scripts/package.py generate
python3 scripts/package.py check
python3 -m unittest discover -s tests -v
python3 scripts/package.py build
claude plugin validate .
```

The packaging tests cover generated configuration drift, skill/reference inclusion and deterministic archives. CI runs offline; it does not depend on live astronomy data or install into a user's client profile.

Verified locally on 2026-10-02:

- Both portable manifests pass the official Agent Plugins 1.0.0 JSON Schemas using `jsonschema`'s Draft 2020-12 validator. This separate schema check fetches the official schemas; the dependency-free CI checker enforces the repository's structural contract and generated-file consistency.
- Claude Code 2.1.285 accepts the compatibility manifest through `claude plugin validate .`.
- Codex CLI 0.159.3 accepts the Streamable HTTP configuration through a command-line override and `mcp get`; no saved user configuration was changed. This verifies configuration parsing, not a server connection.
- All seven skills pass the Skill Creator YAML/frontmatter validator, and the portable archives build successfully.
- An independent review checked client installation formats, archive contents, symlink handling and the distinction between package checks and live acceptance.

## Live MCP check

The existing public endpoint `https://api.sol.wickedsick.com/mcp` returned HTTP 404 with `{"detail":"Not Found"}` on 2026-10-02 at approximately 21:25 UTC. A Python MCP SDK initialization also failed with `Session terminated`. No tool invocation completed. This is an outstanding service acceptance issue, not a successful connection test.

The trailing-slash `/mcp/` also returned 404, while `/healthz` and `/openapi.json` served the REST API successfully. The backend's checked-in php01 systemd unit launches the REST API alone; its separate Docker/Caddy example routes MCP to a different service on port 8002. Missing MCP service/proxy routing on php01 is the likely cause, pending live configuration inspection. This package keeps the documented URL rather than guessing an alternate host. Production service changes require a separate deployment.

[Backend PR #47](https://github.com/Wicked-Sick-Ltd/solar-system-db/pull/47) prepares the separate service, proxy routing, host/origin configuration and rollout checks. Merging the plugin does not activate that service. The proposed rollout must be checked against the live host and explicitly approved before applying it.

Repeat a bounded initialization check after the endpoint has been restored:

```sh
curl --max-time 20 -i https://api.sol.wickedsick.com/mcp \
  -H 'Content-Type: application/json' \
  -H 'Accept: application/json, text/event-stream' \
  --data '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-03-26","capabilities":{},"clientInfo":{"name":"solar-plugin-check","version":"0.2.0"}}}'
```

A healthy result includes negotiated protocol/server capabilities, not just HTTP 200. Then use an MCP client to complete `notifications/initialized`, list tools and call `get_stats` and `get_object` with valid arguments. Follow the returned session/protocol headers where applicable. Check pagination and read-only annotations rather than assuming all advertised tools have the same contract.

## Client acceptance

Before announcing a tested installation for a client, record its version, plugin revision, installation route, actual discovered tools/skills and observed outcomes:

| Scenario | Expected evidence |
| --- | --- |
| Retrieve Mars | Actual catalogue call, source link, units; no fabricated value |
| Tonight from Romsey, explicit date/timezone | Skill loads its references and calls the available sky tools |
| No location supplied | Requests a location before making a local viewing claim |
| Server disconnected or tool missing | Explains the missing capability without claiming live results |
| Fact-check with browsing unavailable | Distinguishes catalogue evidence from an external claim it cannot verify |
| Unrelated coding request | Astronomy skills do not take over the task |

Native ChatGPT, Cursor and Copilot end-to-end acceptance remains pending. Package/schema validation alone is not evidence of those UI flows. No public directory submission, account connection, production deployment or client-wide configuration change is performed by the build.
