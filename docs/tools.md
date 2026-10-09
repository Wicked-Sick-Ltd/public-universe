# MCP tool reference

Public Universe exposes a read-only [Model Context Protocol](https://modelcontextprotocol.io) server:

| Setting | Value |
| --- | --- |
| URL | `https://api.sol.wickedsick.com/mcp` |
| Transport | Streamable HTTP |
| Authentication | None |
| Connection name in this plugin | `publicuniverse` |

This list was taken from that server on 9 October 2026: **33 tools**, each annotated read-only. Clients often prefix the names (Claude uses a form like `mcp__publicuniverse__get_object`). Match the names and argument schemas your client actually shows. If a tool is missing, say so. Do not invent a live result.

The same catalogue is available as REST. Interactive reference: https://api.sol.wickedsick.com/docs.

## How to read the arguments

Required arguments are listed without a marker. Everything else is optional and is marked "optional". Types below are the ones the server advertised: string, number, integer or boolean. Dates are ISO 8601 (`2026-10-09` or `2026-10-09T21:00:00Z`) unless a tool says otherwise. Omit optional arguments you do not need. Do not send placeholder values.

## Limits that apply to every answer

- Astronomy, not astrology. The server does not write data and does not control a telescope.
- `compute_position` and `get_sky_position` use two-body Kepler propagation. For the planets that is about a degree: enough to name a constellation and say whether the body is up. It is not a pointing solution. Use JPL Horizons when you need arcsecond precision.
- `get_sky_position` can place planets, dwarf planets, asteroids, comets, the Sun, and moons other than Earth's Moon (those other moons use a parent-body proxy). Earth's Moon is not available on that tool. `plan_observing_night` can include the Moon.
- Close-approach rows are catalogue geometry. They are not a hazard ruling. A high orbit-condition code means the path can still move as new observations arrive.
- `galaxy_map` drops host stars with no measured distance. It does not guess those distances, and it is not a planet ephemeris.
- Exoplanet rows can mix measurements from more than one paper. Keep the source fields that come back with the row.
- There is no weather tool. For cloud, use a forecast or the object page on publicuniverse.net.
- Never look at the Sun through binoculars or a telescope without a proper solar filter and supervision.

Object pages on the website use `https://publicuniverse.net/objects/<id>`, with the `id` returned by `get_object`.

## Find a solar-system body

| Tool | What it returns | Arguments |
| --- | --- | --- |
| `search` | Names, designations and discoverers matching free text. "Halley" returns both comet 1P/Halley and asteroid (2688) Halley. | `query`. Optional: `limit`. |
| `find_objects` | Object summaries filtered by type, parent, size, orbit and classification. Pages with `after` (the last id from the previous page). `limit` is 1 to 1000, default 50. | Optional: `object_type` (`planet`, `moon`, `dwarf_planet`, `dwarf_planet_candidate`, `asteroid`, `comet`, `tno`, `centaur`), `parent`, `min_radius_km`, `max_radius_km`, `min_diameter_km`, `max_eccentricity`, `min_semi_major_axis_au`, `max_semi_major_axis_au`, `neo`, `pha`, `named_only`, `orbit_class` (for example `MBA`, `APO`, `TNO`, `JFc`), `max_moid_au`, `max_condition_code` (0 best, 9 worst), `discovered_after`, `after`, `limit`. |
| `get_object` | Full record: orbit, physical and visual properties, classification and provenance. Resolves an id, exact name, exact designation or a partial match such as "Ceres" or "1P/Halley". | `name_or_designation` |
| `get_discovery` | Discovery date, discoverers, site, and the naming citation when one exists. | `name_or_designation` |
| `get_designations` | Permanent number, name, provisional designations, alternates and legacy ids. | `name_or_designation` |
| `list_object_types` | Each `object_type` present in the catalogue, with a row count. | None |

## Moons, rings and families

| Tool | What it returns | Arguments |
| --- | --- | --- |
| `list_moons` | Moons of a planet or dwarf planet, nearest first. | `planet_name` |
| `get_rings` | Ring components ordered by inner radius. | `planet_name` |
| `get_atmosphere` | Surface pressure, temperature, density, scale height, winds and composition by volume, from NASA fact sheets. | `planet` |
| `list_dwarf_planets` | The IAU-recognised dwarf planets. Candidates (Orcus, Quaoar, Sedna, Gonggong, Salacia) only when requested. | Optional: `include_candidates` |
| `list_neos` | Near-Earth objects, brightest absolute magnitude first. Diameter filters use the estimated diameter in kilometres. | Optional: `min_diameter_km`, `max_diameter_km` |
| `list_periodic_comets` | Numbered comets with period under 200 years, shortest period first. `limit` is 1 to 2000, default 500. | Optional: `limit` |
| `list_tnos` | Trans-Neptunian objects and centaurs, by semi-major axis. `limit` is 1 to 2000, default 500. | Optional: `limit` |

## Where things are

| Tool | What it returns | Arguments |
| --- | --- | --- |
| `get_sky_position` | RA/Dec (J2000), constellation, hemisphere, distance from Earth and elongation from the Sun. With `lat` and `lon`, also altitude, azimuth, whether it is up after dark, and rise, transit and set. `date` defaults to now. | `name_or_designation`. Optional: `date`, `lat`, `lon`. Give latitude and longitude together. |
| `compute_position` | Heliocentric ecliptic J2000 position from two-body propagation: x, y, z in AU, plus radius and true anomaly. | `name_or_designation`, `date` |
| `next_perihelion` | Next perihelion as a Julian Date. A two-body estimate: usable for periodic comets and minor planets over a short look-ahead, not for mission planning. | `name_or_designation` |
| `plan_observing_night` | Geometric windows for one local noon-to-noon night. Times are UTC. Weather is not included, and a result is not a promise that you can see the target. Optional horizon mask is a user-entered circle, not a surveyed horizon. Targets are a comma-separated list of supported planets, the Moon, or exact pinned `bsc5p:` / `openngc:` ids, up to eight combined. Sun and Earth are excluded. | `date`, `timezone`, `lat`, `lon`. Optional: `targets`, `min_altitude_deg`, `sun_altitude_deg`, `min_moon_separation_deg`, `window_start_utc`, `window_end_utc`, `horizon_mask`. |
| `discover_observing_targets` | A short, bounded shortlist from the packaged starter sample plus the Moon and the seven planets. `equipment_mode` is `naked_eye`, `binocular` or `telescope` (an editorial preference, not an aperture limit). No weather, and no all-sky sweep. | `date`, `timezone`, `lat`, `lon`, `equipment_mode`. Optional: `preference`, `true_field_deg`, `max_catalogue_v_magnitude`, `shortlist_limit`, `min_altitude_deg`, `sun_altitude_deg`, `min_moon_separation_deg`, `window_start_utc`, `window_end_utc`, `horizon_mask`. |

## Close approaches and meteor showers

| Tool | What it returns | Arguments |
| --- | --- | --- |
| `find_close_approaches` | Every catalogued approach to `body` between two ISO dates, nearest first. One lunar distance is about 0.00257 AU. | `date_min`, `date_max`. Optional: `body` (default Earth), `max_dist_au`, `limit`. |
| `get_close_approaches` | Approaches of one body to the planets or the Moon. Dates are ISO. Nearest in time first. | `name_or_designation`. Optional: `date_min`, `date_max`, `body`, `limit`. |
| `list_meteor_showers` | IAU Meteor Data Center showers. A shower can have several parameter sets. `established_only` keeps status codes 1 and 6. `active_on` (`YYYY-MM-DD`) keeps showers whose peak solar longitude is within 15 degrees of the Sun on that date. | Optional: `established_only`, `active_on`, `limit`. |
| `get_meteor_shower` | One shower by 3-letter code (`GEM`) or name (`Geminids`), all parameter sets, plus the parent body when the centre has linked one. | `code_or_name` |

## Exoplanets and the wider sky

These tools are separate from `find_objects`. They read the NASA Exoplanet Archive copy shipped with the catalogue.

| Tool | What it returns | Arguments |
| --- | --- | --- |
| `list_exoplanets` | Confirmed exoplanets by planet or host name, discovery method, and distance in parsecs. | Optional: `q`, `discovery_method`, `max_distance_pc`, `limit`, `offset`. |
| `get_exoplanet` | One exoplanet by name or stable id, with the archive measurements and references. | `name` |
| `get_exoplanet_host` | Host astrometry, coordinate-frame metadata, and that star's confirmed planets. | `name` |
| `galaxy_map` | Sun-centred Galactic and Galactocentric positions, in parsecs, for hosts with a measured distance. Includes frame metadata and counts of rows dropped because distance or the result limit left them out. Not stellar motion, and not a planet ephemeris. | Optional: `max_distance_pc`, `limit`. |
| `list_starter_targets` | Bounded samples of bright stars, double stars or deep-sky objects, with source licences. Static catalogue coordinates, not a visibility prediction. Double-star separations have no measurement date. | Optional: `family` (`bright_star`, `double_star`, `deep_sky`), `q`, `limit`, `offset`. |
| `get_starter_target` | One starter target by its source-namespaced id, with the original row and provenance. | `target_id` |

## Catalogue metadata

| Tool | What it returns | Arguments |
| --- | --- | --- |
| `get_stats` | Total objects, counts by type, and the time of the latest build. | None |
| `get_sources` | Upstream sources and the last-retrieved time for each. Includes NASA Planetary Fact Sheets, JPL Solar System Dynamics, JPL Small-Body Database and the IAU Minor Planet Center (via SBDB). | None |
| `get_schema` | SQLite DDL for the catalogue, including views, for anyone querying a local copy. | None |
| `get_download_info` | How to download the catalogue as one SQLite file: URL, size, SHA-256, build date, row counts, enrichment coverage and licence. | None |
| `get_catalogue_identity` | Logical and build identifiers and recorded source provenance. Unknown on older or modified files. An id does not promise that historical snapshots stay online. | None |

## REST

https://api.sol.wickedsick.com/docs is the OpenAPI reference for the same service (`/api/v1/objects`, `/api/v1/exoplanets`, `/api/v1/galaxy`, and the other routes listed there). The plugin talks to the MCP URL. Use the REST docs when you are calling HTTP yourself.
