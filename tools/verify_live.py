#!/usr/bin/env python3
"""Machine half of verification/weekly-page.md: is the live page what main says, and is main sound?

Run from an up-to-date checkout of main:
  git pull --ff-only && python3 tools/verify_live.py --forbid WORD [WORD ...]

--forbid takes words that must not appear in anything served (the other entity's name).
The runner supplies them; they are never written into this public repo. Without them the
entity check fails rather than passing unchecked.

Prints one JSON object of verdicts and exits 0 only when every verdict is true.
Matches of personal traces are reported by count and file, never by value.
"""
import argparse, datetime as dt, glob, hashlib, json, pathlib, re, sys, time, unicodedata, urllib.request, urllib.error

ROOT = pathlib.Path(__file__).resolve().parent.parent
LIVE = "https://ttrng3.github.io/Ecopm-Sitecheck/"
# Tracked but never served (.pages-allow); each must answer 404.
PRIVATE = ["README.md", "CLAUDE.md", "REVIEW.md", "docs/weekly-refresh.md", "data/.last-check",
           "tools/parse_sitecheck.py", "tools/build-fragment.py", "tools/reconcile.py", "tools/verify_live.py",
           "verification/weekly-page.md", "work/261001-weekly-page-protocol/intent.md",
           ".github/scripts/freshness.py", ".pages-allow"]
TRACES = re.compile(r"/personal/|sharepoint\.com|1drv\.ms|[\w.+-]+@[A-Za-z0-9-]+\.[A-Za-z]{2,}", re.I)
HEARTBEAT_MAX = 9  # the watchdog pipeline-wiring's collect_status.py sets for this pipeline
DATA_MAX = 24      # MAX_DATA_AGE_DAYS default in .github/scripts/freshness.py


def get(path, tries=2):
    """One retry on a network error: a blip must not read as a mismatch (first full run, 01/10)."""
    url = f"{LIVE}{path}?v={int(time.time())}"
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "verify-live"}), timeout=30) as r:
            return r.status, r.read()
    except urllib.error.HTTPError as e:
        return e.code, b""
    except Exception as e:
        return get(path, tries - 1) if tries > 1 else (str(e), b"")


def age_days(stamp):
    """Days since an ISO stamp ('...Z', '+00:00', fractions all fine); None if unreadable."""
    try:
        t = dt.datetime.fromisoformat(stamp.strip().replace("Z", "+00:00"))
        t = t if t.tzinfo else t.replace(tzinfo=dt.timezone.utc)
        return round((dt.datetime.now(dt.timezone.utc) - t).total_seconds() / 86400, 1)
    except (ValueError, AttributeError):
        return None


def norm(t):
    """Compare Vietnamese text NFC-normalised and case-folded, so 'Tháng 9' and 'THÁNG 9' match."""
    return unicodedata.normalize("NFC", str(t or "")).casefold()


def month_labels(week_id):
    """Coverage month labels a week id can sit under: 'THÁNG 9' or 'THÁNG 12.25'."""
    y, m = week_id[:4], int(week_id[5:7])
    return {norm(f"THÁNG {m}"), norm(f"THÁNG {m}.{y[2:]}")}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--forbid", nargs="*", default=[])
    forbid = [w.lower() for w in ap.parse_args().forbid if w.strip()]

    d = json.loads((ROOT / "data/index.json").read_text(encoding="utf-8"))
    wk, depts, detail = d.get("wk", []), set(d["depts"]), d.get("detail", {})
    files = sorted(pathlib.Path(f).stem for f in glob.glob(str(ROOT / "data/weeks/*.json")))
    week_text = {x: (ROOT / f"data/weeks/{x}.json").read_text(encoding="utf-8") for x in files}

    v, info, live = {}, {}, {}
    v["has_weeks"] = bool(wk) and bool(files)
    served = ["index.html", "data/index.json"] + [f"data/weeks/{x}.json" for x in files]
    for p in served:
        st, body = get(p)
        live[p] = body
        info[p] = {"status": st, "live": hashlib.sha256(body).hexdigest()[:12],
                   "main": hashlib.sha256((ROOT / p).read_bytes()).hexdigest()[:12]}
    v["served_equals_main"] = all(info[p]["status"] == 200 and info[p]["live"] == info[p]["main"] for p in served)

    priv = {p: get(p)[0] for p in PRIVATE}
    info["private_status"] = priv
    v["private_not_served"] = all(s == 404 for s in priv.values())

    ids = [w["id"] for w in wk]
    v["weeks_ordered_unique"] = ids == sorted(ids) and len(set(ids)) == len(ids)
    # raised totals always; outstanding only where the week carries it (full weeks do; raised/gap may not)
    v["sums_match"] = all(sum(w.get("raised", {}).values()) == w.get("total", 0) and
                          ("outTotal" not in w or sum(w.get("out", {}).values()) == w["outTotal"]) for w in wk)
    # The coverage map and heading count `coverage` files; a run that appends to `wk` only leaves them behind.
    v["coverage_matches_weeks"] = sum(len(m["files"]) for m in d.get("coverage", [])) == len(wk)
    v["dept_keys_known"] = all(set(w.get("raised", {})) <= depts and set(w.get("out", {})) <= depts for w in wk)

    rows = sum(len(json.loads(t)) for t in week_text.values())
    v["detail_files_match"] = sorted(detail.values()) == files and all(k == x for k, x in detail.items())
    v["detail_rows_match"] = rows == d.get("detailRows")
    # A week without row detail must say so where the runbook (step 4) puts it: that month's
    # coverage note. The week's own note counts too. The 22/09 run said nothing anywhere.
    missing = [w for w in wk if w["id"] not in detail]
    def declared(w):
        if norm("chi tiết") in norm(w.get("note")):
            return True
        wnn = w["id"][-3:]
        return any(norm(m["m"]) in month_labels(w["id"]) and
                   any(f[0] == wnn and norm("chi tiết") in norm(f[-1]) for f in m["files"] if f)
                   for m in d.get("coverage", []))
    v["missing_detail_declared"] = all(declared(w) for w in missing)
    info["weeks"] = {"count": len(wk), "newest": ids[-1] if ids else None,
                     "without_detail": [w["id"] for w in missing], "rows": rows}

    beat = ((ROOT / "data/.last-check").read_text(encoding="utf-8").split() or [""])[0]
    info["heartbeat_age_days"], info["data_age_days"] = age_days(beat), age_days(str(d.get("generatedUtc", "")))
    v["heartbeat_fresh"] = info["heartbeat_age_days"] is not None and info["heartbeat_age_days"] <= HEARTBEAT_MAX
    v["data_fresh"] = info["data_age_days"] is not None and info["data_age_days"] <= DATA_MAX

    # Everything Pages serves: the live copies fetched above plus every tracked week file.
    texts = {p: b.decode("utf-8", "replace") for p, b in live.items()}
    texts.update({f"data/weeks/{x}.json": t for x, t in week_text.items() if f"data/weeks/{x}.json" not in texts})
    hits = {p: len(TRACES.findall(t)) for p, t in texts.items()}
    info["traces"] = {p: n for p, n in hits.items() if n}
    v["no_personal_traces"] = not info["traces"]
    info["forbid_checked"] = len(forbid)
    v["no_forbidden_words"] = bool(forbid) and not any(w in t.lower() for w in forbid for t in texts.values())

    print(json.dumps({"pass": all(v.values()), "verdicts": v, "info": info}, ensure_ascii=False, indent=1))
    sys.exit(0 if all(v.values()) else 1)


if __name__ == "__main__":
    main()
