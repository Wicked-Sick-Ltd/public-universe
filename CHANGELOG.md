# Changelog

## 0.2.0 (unreleased)
- Add portable Agent Plugins packaging for Codex, Cursor and Copilot while retaining Claude compatibility.
- Document ChatGPT hosted MCP connection and separate packaged-skill setup.
- Generate standalone client profiles from one canonical MCP configuration and package metadata.
- Keep all seven skills and their references portable across client tool namespaces.
- Add deterministic packaging, drift checks and offline CI; record pending live endpoint acceptance.

## 0.1.0 (2026-09-28)
- First release: connects the public Solar MCP server (`https://api.sol.wickedsick.com/mcp`).
- Skills: tonight-sky, lesson-builder, space-fact-check, object-explainer, close-approach-watch, sky-this-week, solar-data-audit.
- Shared data caveats (moon counts, GM/R² gravity, Venus's two kinds of day, two-body accuracy, UTC).
