"""Detail rows from an ECOPM weekly sitecheck workbook -> data/weeks/<YYYY-MM-Wnn>.json.

Usage:  python3 tools/parse_sitecheck.py <workbook.xlsx> <YYYY-MM-Wnn>
Writes  data/weeks/<YYYY-MM-Wnn>.json  as [{dept, loc, issue, action, resp, deadline, status}].

Columns are found by their HEADER text (Tình trạng, Phương án, Bộ phận chịu, Thời hạn), never
by position. Detail files built before 2026-09-25 put the row's STT number in `status`
(3,413 of 5,440 rows); this parser does not. Restored to the repo 2026-09-25 from the
12/09 working copy.
"""
import openpyxl, json, re, sys
from collections import Counter
MAP={"BQLKV1":"BQLVH 1","BQLKV2":"BQLVH 2","BQLKV3":"BQLVH 3","BQL Osen":"BQL CT21-22","CT6":"BQL SAVILLS CT06","CLB TIỆN ÍCH":"CLB Tiện ích","CÔNG VIÊN":"CV Hồ Thiên Nga","CÔNG VIÊN ":"CV Hồ Thiên Nga",
     # sheet names drift week to week; map them onto the canonical depts in data/index.json
     "BQL OSEN":"BQL CT21-22","BQLVH1":"BQLVH 1"}
def clean(c):
    if c is None: return ""
    s=str(c).strip().replace("\r"," ").replace("\n"," ")
    return re.sub(r"\s+"," ",s)
def find_col(hdrs, *keys):
    for ci,txt in hdrs.items():
        t=txt.lower()
        if any(k in t for k in keys): return ci
    return None
def extract(fn):
    wb=openpyxl.load_workbook(fn, read_only=True, data_only=True); out=[]
    for sn in wb.sheetnames:
        if sn.strip()=='TH': continue
        dept=MAP.get(sn, MAP.get(sn.strip(), sn.strip()))
        ws=wb[sn]; rows=[[clean(c) for c in r] for r in ws.iter_rows(values_only=True)]
        hr=None
        for i,r in enumerate(rows[:14]):
            if any('vị trí' in x.lower() or x.lower()=='địa điểm' for x in r): hr=i; break
        hdrs={}
        if hr is not None:
            ncol=max(len(rows[hr]),(len(rows[hr-1]) if hr>0 else 0))
            for ci in range(ncol):
                a=rows[hr-1][ci] if hr>0 and ci<len(rows[hr-1]) else ""
                b=rows[hr][ci] if ci<len(rows[hr]) else ""
                hdrs[ci]=(a+" "+b).strip()
        c_status=find_col(hdrs,'tình trạng','trạng thái')
        c_action=find_col(hdrs,'phương án','biện pháp')
        c_resp=find_col(hdrs,'bộ phận chịu','bộ phận xử','bộ phận liên')
        c_dead=find_col(hdrs,'thời hạn')
        sec=""
        for r in rows:
            joined=" ".join(x for x in r if x)
            if not joined: continue
            if re.match(r'^tu[aầ]n',joined,re.I) and len(joined)<45: sec=joined; continue
            if r and r[0].isdigit() and len(r)>3:
                loc=r[2] if len(r)>2 else ""
                issue=r[3] if len(r)>3 else ""
                if not issue and not loc: continue
                g=lambda ci: (r[ci] if ci is not None and ci<len(r) else "")
                out.append({"dept":dept,"loc":loc,"issue":issue,"action":g(c_action),
                    "resp":g(c_resp),"deadline":g(c_dead),"status":g(c_status),"sec":sec})
    return out
if __name__=="__main__":
    fn=sys.argv[1]; week=sys.argv[2]
    KEYS=["dept","loc","issue","action","resp","deadline","status"]
    rows=[{k:r[k] for k in KEYS} for r in extract(fn)]
    json.dump(rows, open(f"data/weeks/{week}.json","w",encoding="utf-8"), ensure_ascii=False)
    print(week,"rows:",len(rows),"| by dept:",dict(Counter(r['dept'] for r in rows)))
    st=Counter((r['status'] or '(trống)') for r in rows)
    print("  status coverage: filled",sum(v for k,v in st.items() if k!='(trống)'),"/ ",len(rows))
