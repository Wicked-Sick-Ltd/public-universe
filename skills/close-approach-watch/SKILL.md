---
name: close-approach-watch
description: >
  This skill should be used when the user asks "which asteroids are passing Earth this month",
  "any close approaches this week", "is any asteroid going to hit us", "near-Earth objects coming up",
  "asteroid flyby for our assembly/newsletter", or wants upcoming close approaches explained in plain English.
metadata:
  version: "0.1.0"
---

# Close-approach watch

Report upcoming asteroid and comet flybys calmly and accurately, with sizes and distances people can picture.

## Steps
1. **Window and threshold.** Default to the next 30 days, with Earth as the body and `max_dist_au=0.05` (about 19.5 lunar distances). Narrow to 0.01 AU for "really close" lists.
2. **Query** `find_close_approaches(date_min, date_max, body="Earth", max_dist_au, limit)` from the Solar MCP (`solar-system-db`). For interesting objects, follow up with `get_object`, which includes orbit quality (`condition_code`), `pha` status and observation arc.
3. **Size.** Use `radius_km` if present. Otherwise estimate the diameter from `absolute_magnitude_h` using the method in `references/data-caveats.md` and give a range (e.g. "roughly 6–15 m, about the size of a bus").
4. **Distance.** Convert AU to km (1 AU = 149,597,871 km) and to **lunar distances** (LD = 384,400 km). Also use `dist_min_au` to say the pass can't be closer than that.
5. **Speed.** `v_rel_km_s`, with an everyday comparison (e.g. "about 30 times faster than a rifle bullet"). Show the arithmetic.

## Framing
- Lead with reassurance where it's true, e.g. "None of these will hit Earth. The closest passes about X times farther than the Moon." Don't claim an impact probability. Solar lists close approaches, not impact risk assessments. For risk, point to ESA NEOCC or NASA CNEOS Sentry.
- Flag very small objects (under about 20 m) as common and harmless. Explain "potentially hazardous asteroid" as a classification by size and orbit, not a prediction.
- Note that orbits with a high `condition_code` (uncertain orbits) can shift as more observations arrive.

## Output
A short intro, then a table sorted by date:

| Date (local) | Object | Est. size | Closest distance | Speed | Link |

Links go to `https://sol.wickedsick.com/objects/<id>`. For assemblies or newsletters, add a 3-sentence kid-friendly summary on request.
