import json

with open("test_subs.en-orig.json3", "r", encoding="utf-8") as f:
    d = json.load(f)

for ev in d.get("events", []):
    t = ev.get("tStartMs", 0) / 1000.0
    if 1080 <= t <= 1165:
        text = " ".join([s.get("utf8", "") for s in ev.get("segs", [])]).strip()
        if text:
            print(f"{t:.1f}s: {text}")
