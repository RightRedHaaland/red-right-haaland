#!/usr/bin/env python3
"""Rebuild index.html from template.html with live FPL API data.

Runs in GitHub Actions on a schedule. Stdlib only — no pip installs.
Updates, for every player already in the embedded DATA: price, ownership,
status, news, chance-of-playing and form. Adds any brand-new players with
minimal records. Refreshes deadlines and the 'generated' stamp.
The Elo model, fixtures, DefCon history, expert board and squad are static
here — they are curated in Claude sessions and arrive via template updates.
"""
import json, re, sys, urllib.request
from datetime import datetime, timezone

API = "https://fantasy.premierleague.com/api/bootstrap-static/"
POS = {1: "GKP", 2: "DEF", 3: "MID", 4: "FWD"}

def main():
    req = urllib.request.Request(API, headers={"User-Agent": "Mozilla/5.0 (rrh-live refresh)"})
    with urllib.request.urlopen(req, timeout=60) as r:
        api = json.load(r)

    tpl = open("template.html", encoding="utf-8").read()
    m = re.search(r"const DATA = (\{.*?\});\n", tpl, re.S)
    if not m:
        sys.exit("DATA block not found in template.html")
    data = json.loads(m.group(1))

    els = {e["id"]: e for e in api["elements"]}
    byid = {p["id"]: p for p in data["players"]}

    for p in data["players"]:
        e = els.get(p["id"])
        if e is None:
            p["status"] = "u"; p["news"] = "No longer in the game"; continue
        p["price"] = e["now_cost"] / 10
        p["own"] = float(e["selected_by_percent"])
        p["status"] = e["status"]
        p["team"] = e["team"]
        p["news"] = (e.get("news") or "")[:90]
        p["chance"] = e.get("chance_of_playing_next_round")
        p["form"] = e.get("form")

    for eid, e in els.items():
        if eid not in byid:
            data["players"].append({
                "id": eid, "code": e.get("code"), "name": e["web_name"],
                "pos": POS[e["element_type"]], "team": e["team"],
                "price": e["now_cost"] / 10, "own": float(e["selected_by_percent"]),
                "status": e["status"], "ls": None,
                "news": (e.get("news") or "")[:90],
                "chance": e.get("chance_of_playing_next_round"),
                "form": e.get("form"),
            })

    data["deadlines"] = {str(ev["id"]): ev["deadline_time"] for ev in api["events"]}
    data["generated"] = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    out = tpl[: m.start()] + "const DATA = " + json.dumps(
        data, separators=(",", ": "), ensure_ascii=False) + ";\n" + tpl[m.end():]
    open("index.html", "w", encoding="utf-8").write(out)
    print(f"index.html written: {len(data['players'])} players, generated {data['generated']}")

if __name__ == "__main__":
    main()
