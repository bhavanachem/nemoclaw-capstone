# Monitoring baseline — IoT electricity data

Current bookmark: 2014-04-01 06:59:00 UTC (state.json)
Last run: 2026-10-28T02:33:34.983975+00:00

## Baseline stats (from cycle 5, window 2014-03-25 18:00 to 2014-04-01 06:59 UTC)

| Meter | Avg | Std | P50 | P95 | P99 | Max | Character |
|-------|-----|-----|-----|-----|-----|-----|-----------|
| B1E | 1.1 | 4.7 | 0 | 20 | 21 | 22 | Very low, near-zero baseline |
| B2E | 34.5 | 49.5 | 5 | 145 | 177 | 192 | Low-mid, moderate variance |
| BME | 103.4 | 143.6 | 3 | 335 | 339 | 1511 | Spiky; rare large bursts |
| CDE | 82.1 | 613.6 | 0 | 0 | 4797 | 4949 | Extreme spiky; mostly zero |
| CWE | 6.5 | 48.3 | 0 | 0 | 178 | 1042 | Extreme spiky; mostly zero |
| DNE | 2.2 | 3.0 | 1 | 11 | 14 | 15 | Tiny, stable |
| DWE | 29.8 | 145.9 | 0 | 14 | 781 | 807 | Spiky |
| EBE | 0.0 | 0.0 | 0 | 0 | 0 | 0 | Dead meter |
| EQE | 37.9 | 2.6 | 38 | 41 | 43 | 47 | Very stable (fridge-like) |
| FGE | 53.5 | 67.9 | 0 | 137 | 151 | 467 | Spiky |
| FRE | 129.5 | 25.7 | 125 | 135 | 336 | 345 | Stable baseline ~125W |
| GRE | 1.4 | 1.3 | 2 | 4 | 4 | 6 | Tiny, stable |
| HPE | 306.3 | 652.9 | 38 | 1818 | 2484 | 3322 | Very spiky; high variance |
| HTE | 8.0 | 8.6 | 5 | 31 | 43 | 68 | Low-mid |
| OFE | 21.3 | 21.7 | 16 | 69 | 108 | 662 | Mostly low, rare bursts |
| OUE | 0.0 | 0.1 | 0 | 0 | 0 | 3 | Nearly dead |
| RSE | 202.4 | 386.0 | 63 | 520 | 2453 | 4802 | Very spiky; high variance |
| TVE | 55.9 | 80.2 | 22 | 249 | 330 | 372 | Mid, spiky |
| UTE | 39.2 | 0.5 | 39 | 40 | 40 | 41 | Extremely stable always-on |
| WHE | 1349.5 | 1093.9 | 968 | 3500 | 5702 | 9189 | Main house; high load, strong daily cycle |
| WOE | 10.1 | 180.8 | 0 | 0 | 1 | 3710 | Extreme spiky; mostly zero |

## Hourly profile — WHE

Low load: HR 0–5 (avg 530–922W), HR 23 (809W).
High load: HR 6–22 (avg 1149–2463W); peak avg at HR 7 (2463W).
Max WHE: 9189W at HR 16 — normal high-load pattern.

## Working spike definition

A spike is a reading or sustained period where:
- Magnitude: significantly exceeds per-meter P99 for that hour-of-day, or exceeds P50 by 5x+, especially if sustained across multiple consecutive readings
- Duration: more than a single isolated reading
- Time of day: occurs during normally low-load hours AND is large relative to that hour's baseline
- Multi-meter: several meters move together (whole-house event, not single appliance)

Ordinary non-spike peaks: brief appliance cycles within historical P99/max range.

## Cycle log

- 2026-10-27 22:23 UTC: Cycle 1 — baseline built, bookmark 2014-04-01 06:59 UTC. No email.
- 2026-10-27 22:29 UTC: Cycle 2 — NO_NEW_DATA.
- 2026-10-27 22:30 UTC: Cycle 3 — --until rejected, rerun without flag → NO_NEW_DATA.
- 2026-10-28 02:23 UTC: Cycle 4 — --until 2014-03-25T18:00:00, status report written and emailed (SENT). Bookmark at 2014-03-25 18:00:00 UTC.
- 2026-10-28 02:33 UTC: Cycle 5 — window 2014-03-25 18:00 to 2014-04-01 06:59 UTC, 197,799 rows. All max values match baseline. Verdict: NO_SPIKE. Bookmark at 2014-04-01 06:59:00 UTC. No email sent.