# Public Universe · Solar plugin

Astronomy tools and seven reusable workflows for **ChatGPT, Codex, Cursor, GitHub Copilot and Claude**. Explore catalogue data from NASA/JPL and other astronomical organisations, prepare lessons, explain objects and plan an evening of stargazing.

The stable package name is **`solar`**. Public Universe is the project name; the existing service URLs remain in place during the domain migration.

## Choose your client

| Client | Installation |
| --- | --- |
| ChatGPT | [Connect the public MCP server; add packaged skills where supported](docs/openai.md#chatgpt) |
| Codex CLI, desktop and IDE | [Portable plugin or MCP plus local skills](docs/openai.md#codex) |
| Cursor | [Local portable plugin](docs/clients.md#cursor-full-plugin) |
| GitHub Copilot CLI | [Local portable plugin](docs/clients.md#github-copilot-cli-full-plugin) |
| GitHub Copilot in VS Code | [Local portable plugin](docs/clients.md#github-copilot-in-vs-code-full-plugin) |
| Claude Code | [Existing Claude plugin format](docs/clients.md#claude-code-existing-plugin-compatibility) |
| Other MCP clients | Add the HTTPS endpoint below using the client's Streamable HTTP setup. Skills need separate Agent Skills support. |

The root `plugin.json`, `mcp.json` and `skills/` use the [portable Agent Plugins format](https://agent-plugins.org/). Claude compatibility files are also included. A tools-only MCP connection does **not** install the skills. Client version, account and organisation policies affect availability; this is not a claim of public marketplace approval.

Clone this repository into a new directory, or extract the built archive. While reviewing the development PR, use its `codex/multi-vendor-plugin` branch; `main` gains these files only after merge. Follow the guide for your client and preserve any existing configuration.

## Connection

- Server name: `solar-system-db`
- Transport: **Streamable HTTP**
- URL: **`https://api.sol.wickedsick.com/mcp`**
- Authentication: the intended public service requires no API key.

**Live acceptance pending:** this URL returned HTTP 404 to an MCP initialization request on 2026-10-02. Installing the package cannot repair a missing server route. See the [validation record](docs/validation.md) for the current evidence and remaining checks.

Discover available tools from the connected server rather than relying on a fixed tool count. Existing workflows use catalogue lookup, sky positions, meteor showers, close approaches and source metadata. Deployment determines which newer catalogue and observing tools are available.

## Skills

| Skill | Use it for |
| --- | --- |
| `tonight-sky` | A viewing plan for a place and evening |
| `lesson-builder` | UK key-stage lessons and worksheets using live values |
| `space-fact-check` | Check astronomy claims and explain definition differences |
| `object-explainer` | Explain catalogue objects at a chosen reading level |
| `close-approach-watch` | Explain upcoming asteroid and comet flybys |
| `sky-this-week` | Draft a sourced sky roundup or social copy |
| `solar-data-audit` | Compare catalogue data with official sources |

Every skill includes its own reference files, so it can be installed independently. The same source skills are used by every client. Workflow instructions distinguish unavailable tools from verified results.

## Develop and package

Run these commands from a source checkout with Python 3.11 or newer; packaging has no third-party dependencies.

```sh
python3 scripts/package.py generate
python3 scripts/package.py check
python3 -m unittest discover -s tests -v
python3 scripts/package.py build
```

The build produces `dist/solar-0.2.0.zip` and the equivalent `.plugin` archive. CI also attaches these packages to its validation runs. Archives contain the installable plugin and setup guides; development scripts and tests remain in the source checkout.

Edit root `plugin.json` for package metadata and root `mcp.json` for the connection. Regenerate the Claude compatibility files and standalone client profiles, then commit those generated files with the source change. `check` rejects drift. The build includes an explicit set of package files and excludes repository history and unrelated local files. See [validation and client acceptance](docs/validation.md).

## Data and observing

This is astronomy, not astrology. Keep the source, retrieval date, units, calculation method and limitations with derived answers. These workflows do not control telescopes or certify pointing accuracy. Never look at the Sun through binoculars or a telescope without specialist solar observing equipment and appropriate supervision.

The plugin code is MIT licensed; source datasets retain their own terms and attribution requirements. Consult the catalogue's source records, including credit to the IAU Minor Planet Center where applicable.

Built by Wicked Sick Ltd. Feedback: hello@wickedsick.com.
