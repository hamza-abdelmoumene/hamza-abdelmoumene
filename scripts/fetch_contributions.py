#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fetch a GitHub contribution calendar from the PUBLIC HTML endpoint -- no token,
no GraphQL. Writes data/contributions.json (raw days + derived stats).

    https://github.com/users/<username>/contributions
"""
import json
import os
import re
import sys
from datetime import date

import requests
from bs4 import BeautifulSoup

USERNAME = os.environ.get("GH_USERNAME", "hamza-abdelmoumene")
OUT = os.path.join(os.path.dirname(__file__), "..", "data", "contributions.json")
UA = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")


def fetch_html(user):
    url = f"https://github.com/users/{user}/contributions"
    r = requests.get(url, headers={"User-Agent": UA,
                                   "X-Requested-With": "XMLHttpRequest"}, timeout=30)
    r.raise_for_status()
    return r.text


def parse(html):
    soup = BeautifulSoup(html, "html.parser")

    # counts live in <tool-tip for="cell-id">"N contributions on ..."</tool-tip>
    tips = {}
    for tt in soup.find_all("tool-tip"):
        cid = tt.get("for")
        if not cid:
            continue
        m = re.match(r"\s*(No|\d[\d,]*)\s+contribution", tt.get_text())
        tips[cid] = 0 if (m and m.group(1) == "No") else (int(m.group(1).replace(",", "")) if m else 0)

    days = []
    for td in soup.select("td.ContributionCalendar-day"):
        d = td.get("data-date")
        if not d:
            continue
        level = int(td.get("data-level", 0) or 0)
        cid = td.get("id")
        count = tips.get(cid)
        if count is None:
            dc = td.get("data-count")
            count = int(dc) if dc is not None else None
        days.append({"date": d, "level": level, "count": count})

    days.sort(key=lambda x: x["date"])

    # total: prefer the page's own "N contributions in the last year" headline
    total = None
    h = soup.find(string=re.compile(r"contribution[s]? in the last year"))
    if h:
        m = re.search(r"([\d,]+)\s+contribution", h)
        if m:
            total = int(m.group(1).replace(",", ""))
    if total is None:
        total = sum((x["count"] or 0) for x in days)

    return days, total


def derive(days, total):
    def active(d):  # a "green" day: level>0, or count>0 when known
        return d["level"] > 0 if d["count"] is None else d["count"] > 0

    # longest streak
    longest = cur = 0
    for d in days:
        cur = cur + 1 if active(d) else 0
        longest = max(longest, cur)

    # current streak: walk back from the most recent day
    current = 0
    for d in reversed(days):
        if active(d):
            current += 1
        else:
            # allow today itself to be empty without breaking the streak
            if d is days[-1]:
                continue
            break

    best = max(days, key=lambda x: (x["count"] or 0), default=None)
    known = [d for d in days if d["count"] is not None]
    active_days = sum(1 for d in days if active(d))

    # monthly totals (last 12 buckets present in the window)
    months = {}
    for d in days:
        ym = d["date"][:7]
        months[ym] = months.get(ym, 0) + (d["count"] or 0)

    return {
        "generated": date.today().isoformat(),
        "username": USERNAME,
        "total_last_year": total,
        "current_streak": current,
        "longest_streak": longest,
        "active_days": active_days,
        "best_day": {"date": best["date"], "count": best["count"]} if best else None,
        "counts_known": len(known) == len(days) and len(days) > 0,
        "months": months,
        "days": days,
    }


def main():
    user = sys.argv[1] if len(sys.argv) > 1 else USERNAME
    globals()["USERNAME"] = user
    days, total = parse(fetch_html(user))
    if not days:
        print("ERROR: no contribution cells parsed -- GitHub markup may have changed",
              file=sys.stderr)
        sys.exit(1)
    data = derive(days, total)
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=1)
    print(f"{user}: {len(days)} days, {total} contributions, "
          f"streak {data['current_streak']} (best run {data['longest_streak']})")


if __name__ == "__main__":
    main()
