# Solar plugin

Live Solar System data from **Solar** (https://sol.wickedsick.com), a free catalogue of more than 1.5 million objects built nightly from NASA/JPL and IAU Minor Planet Center data. The plugin connects Claude to Solar's public MCP server and adds skills for teachers, stargazers, content writers and the Solar team.

## Connection
`.mcp.json` registers the public MCP server:

- `solar-system-db`, streamable HTTP at `https://api.sol.wickedsick.com/mcp`. No authentication is needed.

The server exposes 28 read-only tools, including `get_object`, `list_moons`, `search`, `get_sky_position`, `compute_position`, `find_close_approaches`, `list_meteor_showers`, `next_perihelion` and `get_stats`.

## Skills
| Skill | Use it for |
|---|---|
| **tonight-sky** | "What can I see tonight from Romsey?": planets up, directions, heights and times in local time |
| **lesson-builder** | Lessons and worksheets from KS1 to A-level with live values, curriculum links and answers |
| **space-fact-check** | Check a worksheet, brochure, post or AI answer against the catalogue, with safer wording |
| **object-explainer** | Explain any planet, moon, comet, asteroid or shower for a child, teen or adult, with a fact card |
| **close-approach-watch** | Upcoming asteroid flybys in plain English, with sizes, lunar distances and a calm tone |
| **sky-this-week** | Blog, newsletter and social copy with SEO metadata that links back to Solar pages |
| **solar-data-audit** | For the Solar team: catalogue QA against official figures, with fixes and verify checks |

Each skill carries `references/data-caveats.md`, which lists the known definition traps (moon counts, GM/R² gravity, Venus's two kinds of day, two-body accuracy, UTC).

## Notes
- Solar is astronomy, not astrology.
- Positions are accurate to about 1°. That's fine for "is it up and where", but not for telescope pointing.
- Data licences: NASA/JPL data is public domain. IAU MPC data needs the credit "Data: IAU Minor Planet Center".
- Built by Wicked Sick Ltd. Feedback and feature ideas: hello@wickedsick.com

## Install
From the Wicked Sick marketplace (`Wicked-Sick-Ltd/ai-marketplace`), install **solar**. Or install the `.plugin` file built from this repo:

```bash
zip -r solar.plugin . -x ".git/*" "*.plugin"
```
