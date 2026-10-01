#!/usr/bin/env python3
"""Machine half of verification/weekly-page.md: is the live page what main says, and is main sound?

Run from an up-to-date checkout of main:
  git pull --ff-only && python3 tools/verify_live.py [--forbid WORD ...]

--forbid takes words that must not appear in anything served (the other entity's name).
The runner supplies them; they are never written into this public repo.

Prints one JSON object of verdicts and exits 0 only when every verdict is true.
"""
import argparse, datetime as dt, glob, hashlib, json, pathlib, re, sys, time, urllib.request, urllib.error

ROOT = pathlib.Path(__file__).resolve().parent.parent
LIVE = "https://ttrng3.github.io/Ecopm-Sitecheck/"
# Tracked but never served (.pages-allow); each must answer 404.
PRIVATE = ["README.md", "CLAUDE.md", "REVIEW.md", "docs/weekly-refresh.md", "data/.last-check",
           "tools/parse_sitecheck.py", "tools/verify_live.py", ".pages-allow"]
TRACES = re.compile(r"/personal/|sharepoint\.com|1drv\.ms|[\w.+-]+@[A-Za-z0-9-]+\.[A-Za-z]{2,}", re.I)


def get(path):
    url = f"{LIVE}{path}?v={int(time.time())}"
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "verify-live"}), timeout=30) as r:
            return r.status, r.read()
    except urllib.error.HTTPError as e:
        return e.code, b""
    except Exception as e:
        return str(e), b""


def age_days(stamp):
    t = dt.datetime.strptime(stamp, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=dt.timezone.utc)
    return round((dt.datetime.now(dt.timezone.utc) - t).total_seconds() / 86400, 1)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--forbid", nargs="*", default=[])
    forbid = [w.lower() for w in ap.parse_args().forbid]

    d = json.loads((ROOT / "data/index.json").read_text(encoding="utf-8"))
    wk, depts, detail = d["wk"], set(d["depts"]), d["detail"]
    files = sorted(pathlib.Path(f).stem for f in glob.glob(str(ROOT / "data/weeks/*.json")))
    served = ["index.html", "data/index.json", f"data/weeks/{files[-1]}.json"]

    v, info = {}, {}
    live = {}
    for p in served:
        st, body = get(p)
        live[p] = body
        info[p] = {"status": st, "live": hashlib.sha256(body).hexdigest()[:12],
                   "main": hashlib.sha256((ROOT / p).read_bytes()).hexdigest()[:12]}
    v["served_equals_main"] = all(i["status"] == 200 and i["live"] == i["main"] for i in info.values())

    priv = {p: get(p)[0] for p in PRIVATE}
    info["private_status"] = priv
    v["private_not_served"] = all(s == 404 for s in priv.values())

    ids = [w["id"] for w in wk]
    v["weeks_ordered_unique"] = ids == sorted(ids) and len(set(ids)) == len(ids)
    v["sums_match"] = all(sum(w["raised"].values()) == w["total"] and
                          sum(w.get("out", {}).values()) == w.get("outTotal") for w in wk)
    # The coverage map and heading count `coverage` files; a run that appends to `wk` only leaves them behind.
    v["coverage_matches_weeks"] = sum(len(m["files"]) for m in d["coverage"]) == len(wk)
    v["dept_keys_known"] = all(set(w["raised"]) <= depts and set(w.get("out", {})) <= depts for w in wk)

    rows = sum(len(json.loads(pathlib.Path(f).read_text(encoding="utf-8"))) for f in glob.glob(str(ROOT / "data/weeks/*.json")))
    v["detail_files_match"] = sorted(detail.values()) == files and all(k == x for k, x in detail.items())
    v["detail_rows_match"] = rows == d["detailRows"]
    # A week published without row detail must say so in its own note (2026-09-22 run did not).
    missing = [w["id"] for w in wk if w["id"] not in detail]
    v["missing_detail_declared"] = all("theo dòng" in w.get("note", "").lower() for w in wk if w["id"] in missing)
    info["weeks"] = {"count": len(wk), "newest": ids[-1], "without_detail": missing, "rows": rows}

    beat = (ROOT / "data/.last-check").read_text(encoding="utf-8").split()[0]
    info["heartbeat_age_days"], info["data_age_days"] = age_days(beat), age_days(d["generatedUtc"])
    v["heartbeat_fresh"] = info["heartbeat_age_days"] <= 9
    v["data_fresh"] = info["data_age_days"] <= 24

    text = b"".join(live.values()).decode("utf-8", "replace")
    info["traces"] = sorted(set(TRACES.findall(text)))[:5]
    v["no_personal_traces"] = not info["traces"]
    local = "".join((ROOT / p).read_text(encoding="utf-8") for p in ["index.html", "data/index.json"] +
                    [f"data/weeks/{x}.json" for x in files]).lower()
    v["no_forbidden_words"] = not any(w in text.lower() or w in local for w in forbid)
    info["forbid_checked"] = len(forbid)

    print(json.dumps({"pass": all(v.values()), "verdicts": v, "info": info}, ensure_ascii=False, indent=1))
    sys.exit(0 if all(v.values()) else 1)


if __name__ == "__main__":
    main()
