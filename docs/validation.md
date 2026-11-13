# Multi-vendor validation

Development acceptance record for Public Universe 0.4.2. Package checks and live service checks are separate.

At 0.4.2, `python3 scripts/package.py check` validates 46 allowlisted files on `main` (`f660a494163def6b3d9e4427eebcf9cf1190f052`). Open pull request #10 removes unused manifests and will lower that count; this page does not state a post-#10 number. The compatibility table below is the 2026-10-05 run for package 0.3.0, including that run's 35-file package check.

## PublicUniverse compatibility results (2026-10-05)

The ZIP was extracted into a temporary marketplace and installed into isolated client profiles. No model inference or user-profile configuration changes were needed.

| Client | Evidence | Remaining acceptance |
| --- | --- | --- |
| Codex CLI 0.160.0 | Native marketplace registration and plugin installation succeeded. App-server `plugin/read` reported PublicUniverse 0.3.0 installed/enabled, all seven namespaced skills, `solar-system-db`, descriptions and icon paths. | Live tool execution and conversational workflows. |
| Claude Code 2.1.273 | `claude plugin validate .` accepted the manifest. A model-free stream-JSON initialization with `--plugin-dir` discovered all seven `publicuniverse:` skill commands in an isolated profile and exited 0. | This version predates MCP-entry validation; live tools and conversational workflows remain unverified. |
| Gemini CLI 0.62.0, Node 24.21.0 | Native extension installation exited 0. Extension/skill discovery found all seven skills and the MCP server. | Live tool execution; discovery reports the inaccessible server. Node 25.6.1 hit an installer shutdown assertion after writing the installation; use the tested Node 24 runtime. |
| GitHub Copilot CLI 1.0.91 | Installed the archive with seven skills; `plugin list` and `skill list` confirmed version 0.3.0 and every workflow. | Live tools and VS Code UI acceptance. Direct installs are deprecated by this CLI; prefer the marketplace entry for distribution. |
| Cursor | Root manifests pass the official Agent Plugins 1.0.0 schemas, the format documented by Cursor for skills and MCP. | No Cursor executable available on this machine: desktop discovery and live execution remain unverified. |

On that 2026-10-05 run, offline package validation passed for all 35 allowlisted files. The 19-test suite passed on Windows with four symlink cases skipped because this account lacks symlink privilege; Linux CI runs those security checks. Both distributable archives build. The root portable manifest carries OpenAI metadata, so a duplicate `.codex-plugin` manifest is unnecessary.

The canonical website returned HTTP 200. MCP initialization returned HTTP 404 at that time; see the live MCP section below for current status. These results establish package compatibility, not public-directory approval or full end-to-end support.

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

Package 0.4.2 advertises `https://api.publicuniverse.net/mcp`. `https://api.sol.wickedsick.com/mcp` keeps working: the two hosts serve in parallel, with no redirect. Checks dated before 2026-11-11 were run against the alias host and are unchanged.

### 2026-11-11 (advertised host)

From the 0.4.2 review environment, against `https://api.publicuniverse.net/mcp`:

- `initialize` → HTTP 200 (`text/event-stream`), `mcp-session-id` set, protocol `2025-03-26`, `serverInfo.name` `solar-system-db` `1.30.0`. No `Location` redirect and no `cf-mitigated` header.
- `notifications/initialized` → HTTP 202.
- `tools/list` → 33 tools, all `readOnlyHint: true` and `destructiveHint: false`.

`get_stats` and `get_object` were not repeated on this host. Those calls in the 2026-10-16 section below are the alias host. The same `initialize` on `https://api.sol.wickedsick.com/mcp` also returned HTTP 200 with no `Location` header.

### 2026-10-16 (end-to-end; supersedes earlier partial checks)

From this cloud agent environment:

- `POST https://api.sol.wickedsick.com/mcp` `initialize` → HTTP 200 (`text/event-stream`), `mcp-session-id` set, protocol `2025-03-26`, `serverInfo.name` `solar-system-db` `1.30.0`.
- `notifications/initialized` → HTTP 202.
- `tools/list` → 33 tools (all `readOnlyHint: true`).
- `tools/call` `get_stats` → live catalogue counts (for example `total_objects` 1,578,967).
- `tools/call` `get_object` with `name_or_designation: "Mars"` → Mars catalogue record with orbital elements.

No authentication required. On that date this satisfied marketplace review connectivity for the then-documented endpoint, `https://api.sol.wickedsick.com/mcp`.

### 2026-10-11 (supersedes the 2026-10-08 result below)

`POST https://api.sol.wickedsick.com/mcp` `initialize` returned HTTP 200 (`text/event-stream`) with an `mcp-session-id`, protocol `2025-03-26` and serverInfo `solar-system-db` 1.30.0. `notifications/initialized` returned 202 and `tools/list` returned 33 tools, all annotated `readOnlyHint: true`, `destructiveHint: false`. No authentication is required; `/.well-known/oauth-protected-resource` returns 404 (expected for an unauthenticated server). Tool calls and client acceptance scenarios were not run in this check. Note the server still reports its name as `solar-system-db`, not `publicuniverse`.

### 2026-10-08 and 2026-10-02

On 2026-10-08 and 2026-10-02, `POST https://api.sol.wickedsick.com/mcp` returned HTTP 404 from the origin. The 2026-10-11, 2026-10-16 and 2026-11-11 initialize results above supersede those checks.

Repeat a bounded initialization check:

```sh
curl --max-time 20 -i https://api.publicuniverse.net/mcp \
  -H 'Content-Type: application/json' \
  -H 'Accept: application/json, text/event-stream' \
  --data '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-03-26","capabilities":{},"clientInfo":{"name":"publicuniverse-check","version":"0.4.2"}}}'
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
