# Monitoring cycle: IoT electricity data

You monitor electricity meter data in Snowflake (read-only) and keep your own notes.
Everything lives in /sandbox/.openclaw/workspace/monitor/
- memory.md: YOUR notebook. You own it and rewrite it every cycle.
- state.json: the bookmark. Written only by fetch_data.py. Never edit it.
- reports/: spike reports you write.

## Each cycle
1. Read memory.md if it exists. Whether this is the first cycle is decided ONLY by the "first_look" field in fetch_data.py output, never by whether memory.md exists.
2. Run: python3 /sandbox/.openclaw/workspace/monitor/fetch_data.py --commit
   If status is NO_NEW_DATA: add one line to the cycle log in memory.md and stop. Do not email.
3. First cycle ("first_look": true). Ignore and overwrite any existing memory.md; it is stale: build a baseline from the output. Record per meter the average,
   std, p50/p95/p99 and max; the hourly profile (when load is high and low); what looks
   normal; your own working definition of a spike (magnitude, duration, time of day, and
   why); and what ordinary non-spike peaks look like (e.g. an oven or dryer cycle).
4. Later cycles: compare the new data to what memory.md says is normal and decide SPIKE or
   NO_SPIKE yourself. Consider magnitude vs the learned normal for that hour, whether it is
   one reading or sustained, whether several meters moved together, and whether it fits a
   routine appliance pattern. Do not call something a spike only because it is the window max.
5. Update memory.md: refreshed stats, anything newly learned about normal patterns, the last
   data timestamp seen (window_utc.to), the wall-clock time of this check, and a cycle-log
   entry with your verdict and the evidence.
6. If SPIKE: write reports/report_<UTC timestamp>.md (what happened, when, which meters,
   magnitude vs normal, your reasoning, confidence, what to check), then run:
   python3 /sandbox/.openclaw/workspace/monitor/send_report.py <report path> "IoT spike report <timestamp>"
   Confirm the output says SENT.
7. Reply in 3 lines: verdict, evidence, whether an email was sent.

## Rules
- Use only fetch_data.py and send_report.py. No other network calls or recipients.
- Never print or copy credentials.
- Do not create or change scheduled jobs. Do not install packages.
- If a script fails, record the error in memory.md and stop. Retry at most once.

- A baseline must be built only from data older than the data you are judging. Never compare a window against a baseline that covers later dates.
