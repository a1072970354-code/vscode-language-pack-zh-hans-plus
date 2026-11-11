#!/usr/bin/env python3
"""给 VS Code 简体中文语言包打补丁：补齐新版 UI 未翻译的字符串。

背景：官方 ms-ceintl.vscode-language-pack-zh-hans 长期停在 1.131，
VS Code 1.146 新增的 Sessions / Agent Host / Copilot 等界面没有官方译文。
本脚本把本地译文字典合并进语言包的 translations/main.i18n.json。

用法:
  vscode_zh_patch.py               # 只体检，打印覆盖率
  vscode_zh_patch.py --apply       # 合并本地译文字典（先自动备份）
  vscode_zh_patch.py --clear-cache # 删除 clp 缓存，逼 VS Code 重建
  vscode_zh_patch.py --apply --clear-cache
"""
import argparse
import glob
import json
import os
import re
import shutil
import sys
import time

APP = "/Applications/Visual Studio Code.app/Contents/Resources/app"
OUT = os.path.join(APP, "out")
EXTRA = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "extras", "zh_146.json")
CJK = re.compile(r"[\u4e00-\u9fff]")


def pack_path():
    pats = os.path.expanduser(
        "~/.vscode/extensions/ms-ceintl.vscode-language-pack-zh-hans-*/translations/main.i18n.json"
    )
    hits = [p for p in glob.glob(pats) if os.path.exists(p)]
    if not hits:
        sys.exit("找不到中文语言包 translations/main.i18n.json")
    return max(hits, key=lambda p: os.path.getmtime(p))


def clp_dir():
    return os.path.expanduser("~/Library/Application Support/Code/clp")


def load_app_pairs():
    keys = json.load(open(os.path.join(OUT, "nls.keys.json"), encoding="utf-8"))
    en = json.load(open(os.path.join(OUT, "nls.messages.json"), encoding="utf-8"))
    pairs = [(m, k) for m, ks in keys for k in ks]
    return pairs, {p: en[i] for i, p in enumerate(pairs)}


def coverage(pack, pairs, enmap):
    contents = pack.get("contents", {})
    missing = []
    for m, k in pairs:
        v = contents.get(m, {}).get(k)
        if not (isinstance(v, str) and CJK.search(v)):
            # 纯 ASCII 标识符无需中文
            src = str(enmap.get((m, k), ""))
            if not re.search(r"[A-Za-z]{2,}", src):
                continue
            missing.append((m, k))
    total = len(pairs)
    return total, missing


def report():
    pack_p = pack_path()
    pack = json.load(open(pack_p, encoding="utf-8"))
    pairs, enmap = load_app_pairs()
    total, missing = coverage(pack, pairs, enmap)
    print(f"语言包  : {pack_p}")
    print(f"应用条目: {total}")
    print(f"待补译  : {len(missing)}")
    print(f"覆盖率  : {100 * (1 - len(missing) / total):.2f}%")
    if missing:
        print("\n缺口最多模块:")
        from collections import Counter
        for m, n in Counter(m for m, _ in missing).most_common(10):
            print(f"  {n:4d}  {m}")
    return len(missing)


def apply():
    if not os.path.exists(EXTRA):
        sys.exit(f"缺少译文字典 {EXTRA}")
    extra = json.load(open(EXTRA, encoding="utf-8"))
    pack_p = pack_path()
    pack = json.load(open(pack_p, encoding="utf-8"))
    contents = pack.setdefault("contents", {})

    added = skipped = 0
    for k, v in extra.items():
        if "::" not in k or not isinstance(v, str) or not v:
            continue
        m, key = k.split("::", 1)
        slot = contents.setdefault(m, {})
        cur = slot.get(key)
        if isinstance(cur, str) and CJK.search(cur):
            skipped += 1
            continue
        slot[key] = v
        added += 1

    stamp = time.strftime("%Y%m%d-%H%M%S")
    shutil.copy2(pack_p, f"{pack_p}.bak-{stamp}")
    tmp = pack_p + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(pack, f, ensure_ascii=False, separators=(",", ":"))
    os.replace(tmp, pack_p)
    print(f"已写入 {pack_p}")
    print(f"新增 {added} 条，跳过已译 {skipped} 条（备份 .bak-{stamp}）")


def clear_cache():
    d = clp_dir()
    if os.path.isdir(d):
        shutil.rmtree(d, ignore_errors=True)
        print(f"已删除 {d}（VS Code 重启后重建）")
    else:
        print("clp 缓存不存在，无需清理")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--clear-cache", action="store_true")
    a = ap.parse_args()
    if a.apply:
        apply()
    if a.clear_cache:
        clear_cache()
    if a.apply or a.clear_cache:
        print()
    sys.exit(0 if report() == 0 else 0)