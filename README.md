# Public Universe plugin

Free astronomy tools and seven reusable workflows for **Claude Code, Cursor, Codex, ChatGPT, Gemini CLI, GitHub Copilot, Grok and any MCP client**. Explore catalogue data, prepare lessons, explain objects and plan an evening of stargazing with [Public Universe](https://publicuniverse.net), a pro bono astronomy service by Wicked Sick Ltd.

- Plugin name: **`public-universe`** (display name: Public Universe)
- MCP connection name: **`publicuniverse`**
- Repository: https://github.com/Wicked-Sick-Ltd/public-universe
- Licence: MIT, © Wicked Sick Limited. Please credit "Wicked Sick Ltd" when you reuse it (see [NOTICE](NOTICE)).

Clone and install from `https://github.com/Wicked-Sick-Ltd/public-universe`. This repository is `Wicked-Sick-Ltd/solar-plugin` until that rename lands; GitHub will then redirect the old name. A local checkout works either way. `Wicked-Sick-Ltd/publicuniverse-plugin` is not this repository, and links that use it 404.

The plugin id changed from `publicuniverse` to `public-universe` in 0.5.0. The MCP connection name stays `publicuniverse`, so existing MCP configs and tool prefixes that already use that name keep working. Disable an older `publicuniverse` or `solar` plugin before installing this one, so the tools and skills are not loaded twice.

## What it does

Public Universe is a read-only astronomy catalogue. This plugin connects an agent to the public MCP server (no API key) and adds seven workflows:

- Plan what to see tonight from a town, postcode or coordinates.
- Explain a planet, moon, asteroid, comet or meteor shower at a chosen reading level.
- Build UK key-stage lessons and worksheets from live catalogue values.
- Check astronomy claims and say when a definition difference is the cause.
- Explain upcoming asteroid and comet close approaches, without calling a flyby harmless.
- Draft a sourced sky roundup or social copy that links back to publicuniverse.net.
- Compare catalogue rows with the recorded upstream sources.

The same server also covers NASA confirmed exoplanets (`list_exoplanets`, `get_exoplanet`, `get_exoplanet_host`) and a map of measured host-star positions (`galaxy_map`). Solar-system positions are two-body estimates: fine for "which constellation, and is it up?", not for pointing a telescope. The service does not include weather, and it does not control telescopes.

Live counts change. On 9 October 2026, `get_stats` reported about 1.6 million solar-system objects, alongside a separate exoplanet catalogue of several thousand confirmed planets. Call `get_stats` for the current figures.

## Quick start

Add the public MCP server. No API key.

```sh
claude mcp add --transport http publicuniverse https://api.sol.wickedsick.com/mcp
```

Other clients use the same URL. A typical JSON entry:

```json
{ "mcpServers": { "publicuniverse": { "type": "http", "url": "https://api.sol.wickedsick.com/mcp" } } }
```

Then ask: "Use Public Universe to retrieve Mars's catalogue record and cite the source." You should see a real tool call, not a guessed answer.

That MCP-only route gives you the tools. It does not install the seven workflows. For tools and skills together, use the full plugin for your client below. Pick one route per client.

## Remote MCP server

| Setting | Value |
| --- | --- |
| Connection name | `publicuniverse` |
| Transport | Streamable HTTP |
| URL | `https://api.sol.wickedsick.com/mcp` |
| Authentication | None (free public service) |
| Tool reference | [docs/tools.md](docs/tools.md) |
| REST documentation | https://api.sol.wickedsick.com/docs |

Checked on 9 October 2026: `initialize` succeeded and the server advertised 33 read-only tools. Some clients show the service's own name, `solar-system-db`. In this plugin the connection name remains `publicuniverse`.

The planned long-term URL is `https://api.publicuniverse.net/mcp`. This package keeps the current URL until that host is live.

The repository is still internal. The MCP URL above is already public. Cloning or installing the plugin from GitHub needs access to `Wicked-Sick-Ltd/public-universe` (or a local checkout) until a separate visibility change. This package does not change visibility.

## Install

Commands below use `https://github.com/Wicked-Sick-Ltd/public-universe`. Longer per-client notes, including skills copied without a plugin system, are in [docs/clients.md](docs/clients.md) and [docs/openai.md](docs/openai.md).

The Wicked Sick catalogue (`Wicked-Sick-Ltd/ai-marketplace`) still lists this plugin as `publicuniverse` and points at `publicuniverse-plugin`, which does not resolve. Do not install from that catalogue entry. This repository does not submit a catalogue or marketplace update.

### Claude Code

```sh
/plugin marketplace add https://github.com/Wicked-Sick-Ltd/public-universe.git
/plugin install public-universe@public-universe
```

Local checkout: `claude --plugin-dir /path/to/public-universe`. MCP only:

```sh
claude mcp add --transport http publicuniverse https://api.sol.wickedsick.com/mcp
```

Try `/public-universe:tonight-sky`. Details: [docs/clients.md](docs/clients.md#claude-code).

### Cursor

Copy this repository to `~/.cursor/plugins/local/public-universe/` (the folder must contain `plugin.json`, `mcp.json` and `skills/tonight-sky/SKILL.md`) and reload the window. If a folder named `publicuniverse` is already there from 0.4.0, remove it first. MCP only: merge [clients/cursor.json](clients/cursor.json) into `~/.cursor/mcp.json`. Details: [docs/clients.md](docs/clients.md#cursor-full-plugin).

### Codex (CLI, desktop, IDE)

MCP and local skills work without a catalogue:

```sh
codex mcp add publicuniverse --url https://api.sol.wickedsick.com/mcp
```

Or merge [clients/codex.toml](clients/codex.toml) into `~/.codex/config.toml`. Copy each skill directory you want from `skills/` into `.agents/skills/` or `~/.agents/skills/`. Details: [docs/openai.md](docs/openai.md#codex).

### ChatGPT

Developer mode, then add an MCP connection named **Public Universe** with the URL above (no auth). Skills are not imported by an MCP connection. Details: [docs/openai.md](docs/openai.md#chatgpt).

### Gemini CLI

```sh
gemini extensions install https://github.com/Wicked-Sick-Ltd/public-universe
```

Pin a reviewed release with `--ref <tag-or-sha>`. A local checkout works with `gemini extensions install /path/to/public-universe`. Details: [docs/clients.md](docs/clients.md#gemini-cli).

### GitHub Copilot (CLI and VS Code)

From a local checkout:

```sh
copilot plugin install /absolute/path/to/public-universe
```

VS Code: add that checkout path to `chat.pluginLocations` in user settings. MCP only: merge [clients/vscode.json](clients/vscode.json) into `.vscode/mcp.json` (the key is `servers`, not `mcpServers`). Details: [docs/clients.md](docs/clients.md#github-copilot-cli-full-plugin).

### Grok (Grok CLI, grok.com, xAI API)

Grok CLI reads Claude Code marketplaces and plugins, so the Claude route above works as is. Or:

```sh
grok plugin install Wicked-Sick-Ltd/public-universe
grok mcp add --transport http publicuniverse https://api.sol.wickedsick.com/mcp
```

On grok.com, add a custom MCP connector with the URL above. Via the xAI API, add `{"type": "mcp", "server_url": "https://api.sol.wickedsick.com/mcp", "server_label": "publicuniverse"}` to `tools`. Details: [docs/clients.md](docs/clients.md#grok).

### Any other MCP client

Add a remote **Streamable HTTP** server named `publicuniverse` with the URL above and no authentication. Most clients accept:

```json
{ "mcpServers": { "publicuniverse": { "type": "http", "url": "https://api.sol.wickedsick.com/mcp" } } }
```

To use the skills without a plugin system, copy whole folders from `skills/` into your client's Agent Skills directory (see [docs/clients.md](docs/clients.md#skills-without-a-full-plugin)).

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

Every skill carries its own reference files, so it can be installed independently. Workflows distinguish unavailable tools from verified results and never invent live values. On Claude Code the new plugin exposes them as `/public-universe:<skill>`.

## Tools

Thirty-three read-only tools, grouped below. Arguments, units and limits are in [docs/tools.md](docs/tools.md).

| Group | Tools |
| --- | --- |
| Find a solar-system body | `search`, `find_objects`, `get_object`, `get_discovery`, `get_designations`, `list_object_types` |
| Moons, rings, families | `list_moons`, `get_rings`, `get_atmosphere`, `list_dwarf_planets`, `list_neos`, `list_periodic_comets`, `list_tnos` |
| Sky and orbits | `get_sky_position`, `compute_position`, `next_perihelion`, `plan_observing_night`, `discover_observing_targets` |
| Close approaches and showers | `find_close_approaches`, `get_close_approaches`, `list_meteor_showers`, `get_meteor_shower` |
| Exoplanets and the wider sky | `list_exoplanets`, `get_exoplanet`, `get_exoplanet_host`, `galaxy_map`, `list_starter_targets`, `get_starter_target` |
| Catalogue metadata | `get_stats`, `get_sources`, `get_schema`, `get_download_info`, `get_catalogue_identity` |

The same data is published as REST. Interactive reference: https://api.sol.wickedsick.com/docs.

## Suggest a feature

- Website form, once it is deployed: https://publicuniverse.net/feedback. On 9 October 2026 that page was not being served yet. Use it for ideas, corrections and contact messages when it is.
- Plugin bugs, install problems and skill changes: [GitHub issues](https://github.com/Wicked-Sick-Ltd/public-universe/issues). Until the rename finishes, the same issues are on `Wicked-Sick-Ltd/solar-plugin`, and GitHub will redirect that address.
- Email: hello@wickedsick.com.

## Upgrading

From `publicuniverse` 0.4.0:

- Remove the `publicuniverse` plugin, then install `public-universe`.
- Claude skill commands change from `/publicuniverse:…` to `/public-universe:…`.
- The MCP connection name stays `publicuniverse`. Tool names are unchanged. You do not need to edit a saved MCP config that already uses that name.
- The audit skill directory stays `publicuniverse-data-audit`.

From `solar`:

- Remove the old `solar` plugin before enabling `public-universe`.
- The MCP connection name changed from `solar-system-db` to `publicuniverse` in 0.4.0. Tool names are unchanged, but client prefixes change (for example Claude's `mcp__…solar-system-db__get_object` becomes `mcp__…publicuniverse__get_object`). Update any saved permission allowlists.
- `/solar:…` commands are now `/public-universe:…`. `solar-data-audit` is now `publicuniverse-data-audit`.

## Develop and package

Python 3.11+, no third-party dependencies:

```sh
python3 scripts/package.py generate   # regenerate client files from plugin.json + mcp.json
python3 scripts/package.py check
python3 -m unittest discover -s tests -v
python3 scripts/package.py build      # dist/public-universe-<version>.zip and .plugin
```

Edit only root `plugin.json` (metadata) and `mcp.json` (connection). `generate` writes the Claude manifest and marketplace, `.mcp.json`, `gemini-extension.json`, the MCP Registry `server.json` and the `clients/` profiles; `check` rejects drift. See [validation](docs/validation.md) and [listings](docs/listings.md).

## Data, safety and licence

This is astronomy, not astrology. Keep the source, retrieval date, units, method and limitations with derived answers. These workflows do not control telescopes or certify pointing accuracy. Never look at the Sun through binoculars or a telescope without proper solar filters and supervision.

The plugin is MIT licensed, © 2026 Wicked Sick Limited; please credit "Wicked Sick Ltd" ([NOTICE](NOTICE)). Catalogue datasets keep their own terms, including credit to NASA/JPL and the IAU Minor Planet Center where applicable.

Built by [Wicked Sick Ltd](https://wickedsick.com).
