#!/usr/bin/env python3
"""
每日自动归集：搜 GitHub 上 Seedance / MiniMax H3 相关的新仓库，
更新已有条目的 star 数，新发现的写入 data/candidates.json 待人工整理。

用法：
    GITHUB_TOKEN=xxx python3 scripts/collect.py   # token 可选，有则配额更高
    python3 scripts/collect.py --dry-run          # 只打印，不写文件

设计原则：
- 机器只做"发现 + 保鲜"（搜新仓库、刷新 star 数），不做"提炼入库"；
  提炼是人的活，新条目先进 candidates.json，人工确认后才进正文。
- README 里两个自动区（AUTO-SKILLS / AUTO-REPOS）由本脚本重写，
  人工写的部分不动。
"""
import json
import os
import sys
import time
import urllib.request
import urllib.parse
from datetime import datetime, timedelta, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
README = os.path.join(ROOT, "README.md")
TOKEN = os.environ.get("GITHUB_TOKEN", "")
DRY_RUN = "--dry-run" in sys.argv

# 搜索关键词组：每组一个查询，命中任一即收录候选
QUERIES = [
    "seedance prompt",
    "seedance 2.5",
    "minimax h3 prompt",
    "minimax h3 video",
    "seedance skill",
    "h3 video prompt",
]
MIN_STARS = 20          # star 硬线
MAX_AGE_DAYS = 365      # 一年内有更新
PER_QUERY = 20          # 每查询取前 N


def api_get(url):
    req = urllib.request.Request(url, headers={
        "Accept": "application/vnd.github+json",
        "User-Agent": "awesome-seedance-h3-collector",
    })
    if TOKEN:
        req.add_header("Authorization", f"Bearer {TOKEN}")
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def search_repos(query):
    q = urllib.parse.quote(f"{query} stars:>={MIN_STARS}")
    url = (f"https://api.github.com/search/repositories?q={q}"
           f"&sort=stars&order=desc&per_page={PER_QUERY}")
    data = api_get(url)
    return data.get("items", [])


def load_json(name, default):
    p = os.path.join(DATA, name)
    if os.path.exists(p):
        with open(p) as f:
            return json.load(f)
    return default


def save_json(name, obj):
    p = os.path.join(DATA, name)
    if DRY_RUN:
        print(f"[dry-run] 将写入 {name}")
        return
    with open(p, "w") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)
        f.write("\n")


def fresh(item):
    if item.get("archived"):
        return False
    updated = datetime.fromisoformat(item["updated_at"].replace("Z", "+00:00"))
    return datetime.now(timezone.utc) - updated < timedelta(days=MAX_AGE_DAYS)


def main():
    tracked = load_json("tracked.json", [])       # 已收录：[{full_name, section, note}]
    candidates = load_json("candidates.json", [])  # 待整理：[{full_name, ...}]
    known = {t["full_name"].lower() for t in tracked}
    known |= {c["full_name"].lower() for c in candidates}

    seen = {}
    for q in QUERIES:
        try:
            for it in search_repos(q):
                if it["stargazers_count"] >= MIN_STARS and fresh(it):
                    seen[it["full_name"].lower()] = it
        except Exception as e:
            print(f"查询失败 [{q}]: {e}", file=sys.stderr)
        time.sleep(2)  # 给 search API 留配额

    # 1. 保鲜：刷新已收录条目的 star 数
    refreshed = 0
    for t in tracked:
        key = t["full_name"].lower()
        if key in seen:
            new_stars = seen[key]["stargazers_count"]
            if t.get("stars") != new_stars:
                t["stars"] = new_stars
                refreshed += 1

    # 2. 发现：未知仓库进候选池
    new_found = []
    today = datetime.now(timezone.utc).date().isoformat()
    for key, it in sorted(seen.items(), key=lambda kv: -kv[1]["stargazers_count"]):
        if key not in known:
            candidates.append({
                "full_name": it["full_name"],
                "url": it["html_url"],
                "description": (it.get("description") or "")[:200],
                "stars": it["stargazers_count"],
                "updated_at": it["updated_at"][:10],
                "discovered": today,
            })
            new_found.append(it["full_name"])

    save_json("tracked.json", tracked)
    save_json("candidates.json", candidates)

    # 3. 重写 README 自动区
    update_readme(tracked)

    print(f"保鲜：{refreshed} 条 star 数更新；新发现：{len(new_found)} 个")
    for n in new_found:
        print(f"  + {n}")


def section_table(tracked, section):
    rows = [t for t in tracked if t["section"] == section]
    rows.sort(key=lambda t: -(t.get("stars") or 0))
    out = []
    for t in rows:
        name = t["full_name"]
        url = f"https://github.com/{name}"
        note = t.get("note", "")
        stars = t.get("stars", "?")
        out.append(f"| [{name}]({url}) | {note} | {stars} |")
    return "\n".join(out)


def update_readme(tracked):
    with open(README) as f:
        text = f.read()

    def replace(marker, body):
        start = f"<!-- AUTO-{marker}:START -->"
        end = f"<!-- AUTO-{marker}:END -->"
        i, j = text.find(start), text.find(end)
        if i < 0 or j < 0:
            print(f"README 缺少标记 {marker}，跳过", file=sys.stderr)
            return text
        head = text[: i + len(start)]
        tail = text[j:]
        return head + "\n" + body + "\n" + tail

    text = replace("SKILLS", section_table(tracked, "skills"))
    text = replace("REPOS", section_table(tracked, "repos"))

    if DRY_RUN:
        print("[dry-run] README 不写入")
        return
    with open(README, "w") as f:
        f.write(text)
    print("README 自动区已更新")


if __name__ == "__main__":
    main()
