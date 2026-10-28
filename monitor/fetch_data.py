#!/usr/bin/env python3
"""Read-only data pull for the monitoring agent. Does not consume the stream.
  python3 fetch_data.py            # test run: bookmark NOT moved
  python3 fetch_data.py --commit   # real cycle: moves the bookmark
"""
import sys; sys.path.insert(0, "/sandbox/.openclaw/pylibs")
import argparse, json, warnings
from datetime import datetime, timedelta, timezone
from decimal import Decimal
from pathlib import Path

warnings.filterwarnings("ignore", category=FutureWarning)
import snowflake.connector  # noqa: E402

ENV_PATH = "/sandbox/.openclaw/agent-snowflake.env"
STATE = Path("/sandbox/.openclaw/workspace/monitor/state.json")

def load_env():
    env = {}
    with open(ENV_PATH) as f:
        for line in f:
            if "=" in line and not line.startswith("#"):
                k, v = line.strip().split("=", 1)
                env[k] = v
    return env

def emit(obj, code=0):
    print(json.dumps(obj, indent=2,
          default=lambda o: float(o) if isinstance(o, Decimal) else str(o)))
    sys.exit(code)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--table", default="IOT_DB.CLEAN.ELECTRICITY_READINGS")
    ap.add_argument("--days", type=int, default=7, help="first-look lookback from newest data")
    ap.add_argument("--profile-meter", default="WHE")
    ap.add_argument("--commit", action="store_true")
    ap.add_argument("--until", help="simulate now, UTC, e.g. 2014-03-25T18:00:00")
    a = ap.parse_args()

    env = load_env()
    conn = snowflake.connector.connect(
        user=env["SF_USER"], password=env["SF_PASSWORD"], account=env["SF_ACCOUNT"],
        warehouse=env["SF_WAREHOUSE"], database=env["SF_DATABASE"], schema=env["SF_SCHEMA"])
    cur = conn.cursor(snowflake.connector.DictCursor)
    try:
        state = json.loads(STATE.read_text()) if STATE.exists() else {}
        cur.execute(f"SELECT MAX(TS_UTC) AS M FROM {a.table}")
        hi = cur.fetchone()["M"]
        if hi is None:
            emit({"status": "NO_DATA"})
        hi = hi.replace(tzinfo=None)
        if a.until:
            hi = min(hi, datetime.fromisoformat(a.until))
        if state.get("last_seen_ts_utc"):
            lo = datetime.fromisoformat(state["last_seen_ts_utc"])
            first_look = False
            if hi <= lo:
                emit({"status": "NO_NEW_DATA", "last_seen_ts_utc": str(lo)})
        else:
            lo, first_look = hi - timedelta(days=a.days), True

        win, p = "TS_UTC > %s AND TS_UTC <= %s", (lo, hi)
        cur.execute(f"""SELECT METER_ID, COUNT(*) AS N,
              ROUND(AVG(REAL_POWER),1) AS AVG_W, ROUND(STDDEV(REAL_POWER),1) AS STD_W,
              MIN(REAL_POWER) AS MIN_W, ROUND(MEDIAN(REAL_POWER)) AS P50_W,
              ROUND(PERCENTILE_CONT(0.95) WITHIN GROUP (ORDER BY REAL_POWER)) AS P95_W,
              ROUND(PERCENTILE_CONT(0.99) WITHIN GROUP (ORDER BY REAL_POWER)) AS P99_W,
              MAX(REAL_POWER) AS MAX_W
            FROM {a.table} WHERE {win} GROUP BY METER_ID ORDER BY METER_ID""", p)
        meters = cur.fetchall()
        cur.execute(f"""SELECT HOUR(TS_LOCAL) AS HR, ROUND(AVG(REAL_POWER)) AS AVG_W,
              MAX(REAL_POWER) AS MAX_W FROM {a.table}
            WHERE METER_ID = %s AND {win} GROUP BY 1 ORDER BY 1""", (a.profile_meter, lo, hi))
        hourly = cur.fetchall()
        cur.execute(f"""SELECT METER_ID, TS_LOCAL, REAL_POWER AS W FROM {a.table}
            WHERE {win}
            QUALIFY ROW_NUMBER() OVER (PARTITION BY METER_ID ORDER BY REAL_POWER DESC) <= 3
            ORDER BY METER_ID, W DESC""", p)
        top = cur.fetchall()

        if a.commit:
            STATE.parent.mkdir(parents=True, exist_ok=True)
            STATE.write_text(json.dumps({"last_seen_ts_utc": hi.isoformat(),
                "last_run_utc": datetime.now(timezone.utc).isoformat(), "table": a.table}))
        emit({"status": "OK", "first_look": first_look,
              "window_utc": {"from": lo, "to": hi}, "rows": sum(m["N"] for m in meters),
              "meters": meters, "hourly_profile_meter": a.profile_meter,
              "hourly_profile": hourly, "top_readings_per_meter": top,
              "bookmark_moved": a.commit})
    except Exception as e:
        emit({"status": "ERROR", "error": str(e)}, 1)
    finally:
        cur.close(); conn.close()

if __name__ == "__main__":
    main()
