---
name: object-explainer
description: >
  This skill should be used when the user asks "tell me about Europa", "explain Halley's Comet to a 7-year-old",
  "what is 2022 UP6", "make a fact card for Ceres", "describe Neptune for my class", or wants any planet, moon,
  comet, asteroid, dwarf planet or meteor shower explained at a chosen reading level using live Solar data.
metadata:
  version: "0.1.0"
---

# Object explainer

Turn any catalogue object into a clear explanation or fact card at the right level.

## Steps
1. **Find it.** Use `search(query)` if the name is ambiguous (e.g. "Halley" matches a comet and an asteroid). Ask which one if it's still unclear. For showers, use `get_meteor_shower`.
2. **Gather the data** with the Solar MCP (`solar-system-db`):
   - `get_object`: type, parent, orbit (a, e, i, period, perihelion and aphelion), physical properties, and discovery details
   - `get_discovery` and `get_designations` for the story behind the name
   - `list_moons` and `get_rings` for planets. `get_atmosphere` where one exists.
   - `get_sky_position` for "can I see it?" (with lat/lon if a location is known)
   - `next_perihelion` for comets. `get_close_approaches` for near-Earth objects.
   If the radius is missing, estimate size from H using the method in `references/data-caveats.md`, and say it's an estimate.
3. **Pick the level.** Default to general adult. Ask if it's for a child. The levels are:
   - **Child (5–11)**: 5–8 short sentences, comparisons to familiar things (a bus, a football pitch, London to Edinburgh), one "wow" fact, no jargon.
   - **Teen (11–16)**: key numbers with units, one idea of why it matters, a simple "try this" on Solar.
   - **Adult or enthusiast**: full data card with orbit, physical data, discovery, observing notes and uncertainties.
4. **Make comparisons concrete.** Scale everything against Earth, the Moon or everyday objects, and show the arithmetic behind each comparison.

## Output
- A short explanation, then a **fact card** listing type, size, distance from the Sun, orbit period, moons, discovered (when and by whom), and whether you can see it.
- Link to the object's page: `https://sol.wickedsick.com/objects/<id>`, using the `id` from `get_object`.
- End with "Data: Solar (NASA/JPL, IAU MPC), retrieved <date>."
- Keep astronomy separate from astrology. Never use zodiac framing.
