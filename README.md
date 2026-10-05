# PublicUniverse plugin

Astronomy tools and seven reusable workflows for **Codex, Claude, Cursor, Gemini CLI and GitHub Copilot**, with a separate ChatGPT connection route. Explore catalogue data, prepare lessons, explain objects and plan an evening of stargazing with [PublicUniverse](https://publicuniverse.net).

The package name is **`publicuniverse`** from version 0.3.0. Website links use `publicuniverse.net`; the existing MCP URL remains until its replacement is confirmed. See [migration and public submission](docs/submission.md) before switching an existing `solar` installation.

## Choose your client

| Client | Installation |
| --- | --- |
| ChatGPT | [Connect the public MCP server; add packaged skills where supported](docs/openai.md#chatgpt) |
| Codex CLI, desktop and IDE | [Portable plugin or MCP plus local skills](docs/openai.md#codex) |
| Cursor | [Local portable plugin](docs/clients.md#cursor-full-plugin) |
| GitHub Copilot CLI | [Local portable plugin](docs/clients.md#github-copilot-cli-full-plugin) |
| GitHub Copilot in VS Code | [Local portable plugin](docs/clients.md#github-copilot-in-vs-code-full-plugin) |
| Claude Code | [Existing Claude plugin format](docs/clients.md#claude-code-existing-plugin-compatibility) |
| Gemini CLI | [Native extension with the same seven skills](docs/clients.md#gemini-cli) |
| Other MCP clients | Add the HTTPS endpoint below using the client's Streamable HTTP setup. Skills need separate Agent Skills support. |

The root `plugin.json`, `mcp.json` and `skills/` use the [portable Agent Plugins format](https://agent-plugins.org/). Claude compatibility files are also included. A tools-only MCP connection does **not** install the skills. Client version, account and organisation policies affect availability; this is not a claim of public marketplace approval.

Clone the reviewed revision into a new directory, or extract the built archive. Follow the guide for your client and preserve any existing configuration. Public catalog installation is pending the repository transfer, visibility change and live MCP acceptance.

## Connection

- Server name: `solar-system-db`
- Transport: **Streamable HTTP**
- URL: **`https://api.sol.wickedsick.com/mcp`**
- Authentication: the intended public service requires no API key.

**Live acceptance deferred to the domain move:** this URL returned HTTP 404 to an MCP initialization request on 2026-10-02. Craig identified Cloudflare WAF rules as the issue on 2026-10-03; address them during the move to the new domain, then repeat live client checks. See the [validation record](docs/validation.md) for the current evidence and remaining checks.

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
| `publicuniverse-data-audit` | Compare catalogue data with official sources |

Every skill includes its own reference files, so it can be installed independently. The same source skills are used by every client. Workflow instructions distinguish unavailable tools from verified results.

## Develop and package

Run these commands from a source checkout with Python 3.11 or newer; packaging has no third-party dependencies.

```sh
python3 scripts/package.py generate
python3 scripts/package.py check
python3 -m unittest discover -s tests -v
python3 scripts/package.py build
```

The build produces `dist/publicuniverse-0.3.0.zip` and the equivalent `.plugin` archive. CI also attaches these packages to its validation runs. Archives contain the installable plugin and setup guides; development scripts and tests remain in the source checkout.

Edit root `plugin.json` for package metadata and root `mcp.json` for the connection. Regenerate the Claude compatibility files, Gemini extension and standalone client profiles, then commit those generated files with the source change. `check` rejects drift. The build includes an explicit set of package files and excludes repository history and unrelated local files. See [validation and client acceptance](docs/validation.md).

## Data and observing

This is astronomy, not astrology. Keep the source, retrieval date, units, calculation method and limitations with derived answers. These workflows do not control telescopes or certify pointing accuracy. Never look at the Sun through binoculars or a telescope without specialist solar observing equipment and appropriate supervision.

The plugin code is MIT licensed; source datasets retain their own terms and attribution requirements. Consult the catalogue's source records, including credit to the IAU Minor Planet Center where applicable.

Built by Wicked Sick Ltd. Feedback: hello@wickedsick.com.
