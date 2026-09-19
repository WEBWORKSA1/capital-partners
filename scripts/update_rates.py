#!/usr/bin/env python3
"""Fetch the latest WSJ Prime Rate from FRED (series DPRIME, no API key). Keeps the old value on any failure."""
import csv, io, json, os, sys, urllib.request, datetime
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PATH = os.path.join(ROOT, "data/rates.json")
cur = json.load(open(PATH))
try:
    req = urllib.request.Request("https://fred.stlouisfed.org/graph/fredgraph.csv?id=DPRIME", headers={"User-Agent": "capital.partners rate bot"})
    rows = list(csv.reader(io.StringIO(urllib.request.urlopen(req, timeout=30).read().decode())))
    latest = [r for r in rows[1:] if len(r) == 2 and r[1] not in ("", ".")][-1]
    prime = round(float(latest[1]), 2)
    if not 1.0 <= prime <= 20.0: raise ValueError(f"implausible prime {prime}")
except Exception as e:
    print(f"Rate fetch failed, keeping {cur['prime']}%: {e}"); sys.exit(0)
changed = prime != cur["prime"]
cur.update({"prime": prime, "as_of": datetime.date.today().isoformat(), "source": "WSJ Prime Rate (FRED series DPRIME)"})
json.dump(cur, open(PATH, "w"))
print(f"Prime {prime}% ({'CHANGED' if changed else 'unchanged'}), effective {latest[0]}")
