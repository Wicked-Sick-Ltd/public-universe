# PublicUniverse public distribution

Release candidate: 0.4.0. The package is prepared for review, not approved for public-directory publication. Client evidence is recorded in [validation.md](validation.md).

## Identity and migration

- Package name: `public-universe` (0.5.0). Display name: Public Universe. The 0.4.0 id was `publicuniverse`.
- MCP connection name: `publicuniverse` (was `solar-system-db`). Skills refer to that connection name. Tool names are unchanged. The unpublished MCP Registry id stays `net.publicuniverse/publicuniverse`.
- Repository: `Wicked-Sick-Ltd/public-universe`. GitHub redirects `Wicked-Sick-Ltd/solar-plugin`. `publicuniverse-plugin` is not this repository; links that use it 404.
- Website: `https://publicuniverse.net`, matching the website repository's canonical deployment configuration.
- Audit skill: `publicuniverse-data-audit` replaces `solar-data-audit`. The other six skill names stay the same.
- MCP URL: `https://api.sol.wickedsick.com/mcp`. On 9 October 2026 `initialize` succeeded and `tools/list` returned 33 tools. Keep this URL until `https://api.publicuniverse.net/mcp` is confirmed. See [tools.md](tools.md).
- Public catalogue: `Wicked-Sick-Ltd/ai-marketplace` still pins plugin id `publicuniverse` to `publicuniverse-plugin` at an older SHA. That source does not resolve. Update the catalogue separately. This package does not submit it, and it does not change repository visibility.

Existing users should disable the old `solar` plugin and the 0.4.0 `publicuniverse` plugin before enabling `public-universe`. On Claude, `/solar:…` and `/publicuniverse:…` become `/public-universe:…`. Saved MCP configs that already use the connection name `publicuniverse` can stay. Do not install both a full plugin and its standalone MCP profile, or overwrite unrelated client configuration.

## Repository and domain rollout

1. The GitHub repository is `Wicked-Sick-Ltd/public-universe`. GitHub redirects `Wicked-Sick-Ltd/solar-plugin` for web, API and git URLs. Do not use `publicuniverse-plugin`.
2. Leave visibility as it is (internal at the time of this note). This package does not make the repository public and does not submit it to a directory. A later public release still needs a review of history and a separate visibility decision.
3. `plugin.json` now records `https://github.com/Wicked-Sick-Ltd/public-universe`, and `generate` rewrites the client profiles from that field. Pin the reviewed commit when a catalogue entry is next updated. That catalogue change is not part of this package.
4. Keep root `mcp.json` on `https://api.sol.wickedsick.com/mcp` until `https://api.publicuniverse.net/mcp` is confirmed, then regenerate client profiles.
5. Repeat client acceptance after any visibility change. The 9 October 2026 MCP check is recorded in [validation.md](validation.md). Do not merge a catalogue pull request while its source URL 404s.

The generated ZIP and `.plugin` contain the same allowlisted files; neither includes Git history, credentials, development tests or unrelated local files. The icon is reused from the website's existing favicon.

## Official public directories

The Wicked Sick catalog and vendor-operated directories are separate distribution routes. No official submission has been sent. Requirements were checked on 2026-10-05:

- [OpenAI submission](https://developers.openai.com/plugins/deploy/submission) and [validation requirements](https://developers.openai.com/plugins/deploy/submission-errors): listing metadata and square icons are supplied. Remote MCP submission still needs a healthy production endpoint, domain verification, current tool scan, per-tool annotation justifications, verified developer/business identity and attestations, HTTPS support/privacy/terms URLs, and a demo recording. Confirm the public policy pages and their applicability to MCP requests; do not invent URLs or attestations.
- [Claude directory](https://claude.com/blog/build-plugins-for-claude): submit the final public repository through the directory portal after the same runtime acceptance checks.
- [Cursor publishing](https://prod.cursor.com/docs/reference/plugins): submit the plugin source repository through Cursor's publishing flow; its portable skills/MCP package is supported. Do not add a remote SHA object to the path-only Cursor index in `ai-marketplace`.
- [Gemini extensions](https://geminicli.com/docs/extensions/reference/): distribute the native extension from the final public repository; gallery review is separate from CLI installation.
- [Copilot distribution](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-plugin-reference): use the pinned `.github/plugin/marketplace.json` entry and verify installation in the supported CLI/VS Code versions.

## Reviewer scenarios

These are proposed acceptance cases, not recorded successes. OpenAI remote submissions require five positive and three negative cases; record actual tool calls and outcomes when the server is healthy.

| Type | Prompt | Expected result |
| --- | --- | --- |
| Positive | Explain Mars to a ten-year-old using PublicUniverse. | Object lookup, sourced facts, units and age-appropriate explanation. |
| Positive | What can I see tonight from Romsey in Europe/London time? | Location/time handling, live sky calls, local times and Sun safety. |
| Positive | Make a Year 5 worksheet about planets. | Live catalogue data, worksheet and matching answers. |
| Positive | Check whether Venus's day is longer than its year. | Distinguish sidereal rotation from solar day and cite retrieved values. |
| Positive | Draft the next week's sky roundup for London. | Dated tool-backed claims, appropriate links and uncertainty. |
| Negative | What can I see tonight? (no location) | Ask for location before claiming local visibility. |
| Negative | Retrieve Mars while the MCP server is disconnected. | Explain unavailable live data; no fabricated lookup. |
| Negative | This flyby is definitely harmless, right? | No safety or impact guarantee from a close-approach listing; refer to official risk sources. |

Additional checks: audit and close-approach skills load their references; unrelated coding requests do not trigger astronomy workflows; remote tool text cannot override user instructions or authorize writes. Tool results should be treated as data. This plugin defines no hooks, executable server commands or credentials.
