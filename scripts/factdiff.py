#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""factdiff.py — 改稿の前後で事実の表現が増減していないかを見る(docs/文体改稿の手引き.md 2節)。

使い方:
    python3 scripts/factdiff.py 旧ファイル 新ファイル

二つの章ファイルから、数字(桁区切り・小数・%・年・時刻を含む)、カタカナ語
(二文字以上)、英字列、「」内の語を抜き出し、新にあって旧にないもの、旧に
あって新にないものを列挙する。

新ファイルの -check ファイル(例: tx.md → tx-check.md)に表記の対応表があれば
読み、対応する組は差分から除く。対応表の書式: 「↔」(または <->)を含む行。
例:
    - 約4割 ↔ およそ40%
左右それぞれの側から抜き出される要素どうしを対応済みとして扱う。

終了コード: 差分が無ければ 0、あれば 1。
"""

import os
import re
import sys
from collections import Counter

# 数字: 桁区切り・小数・%・年・時刻・単位の接尾を含む
RE_NUMBER = re.compile(
    r"[0-90-9][0-90-9,,..::]*"
    r"(?:%|%|年|時|分|秒|世紀|km|m|cm|mm|ヘクタール|トン|ドル|円|ルーブル|元|人|世帯|頭|羽|隻|軒|店|校|社|基|本|枚|回|倍|割)?"
)
RE_KATAKANA = re.compile(r"[ァ-ヴー]{2,}")
RE_LATIN = re.compile(r"[A-Za-zA-Za-z][A-Za-zA-Za-z0-9&.\-]*")
RE_QUOTED = re.compile(r"「([^」]+)」")


def extract_facts(text):
    """事実の指標になる表現を Counter で返す。"""
    facts = Counter()
    for m in RE_NUMBER.finditer(text):
        tok = m.group(0).rstrip(",,..")
        # 素の一桁数字は文脈語が多すぎるので、単位付き・複数桁だけ拾う
        facts["数 " + tok] += 1
    for m in RE_KATAKANA.finditer(text):
        facts["カ " + m.group(0)] += 1
    for m in RE_LATIN.finditer(text):
        facts["英 " + m.group(0)] += 1
    for m in RE_QUOTED.finditer(text):
        inner = m.group(1)
        if len(inner) <= 24:  # 長い引用文は語ではなく文なので除く
            facts["「」 " + inner] += 1
    return facts


def load_text(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def check_path_for(path):
    base, ext = os.path.splitext(path)
    return base + "-check" + ext


def load_correspondences(check_file):
    """対応表を [(左側の要素集合, 右側の要素集合)] で返す。"""
    pairs = []
    if not os.path.exists(check_file):
        return pairs
    with open(check_file, encoding="utf-8") as f:
        for line in f:
            if "↔" in line or "<->" in line:
                line = line.strip().lstrip("-*  ")
                sides = re.split(r"↔|<->", line)
                if len(sides) == 2:
                    left = set(extract_facts(sides[0]))
                    right = set(extract_facts(sides[1]))
                    pairs.append((left, right))
    return pairs


def apply_correspondences(only_old, only_new, pairs):
    """対応表に載った組を差分から除く。左右どちらの表記も、旧のみ・新のみの両方から外す。"""
    for left, right in pairs:
        for k in left | right:
            only_old.pop(k, None)
            only_new.pop(k, None)
    return only_old, only_new


def main(argv):
    if len(argv) != 3:
        print(__doc__)
        return 2
    old_path, new_path = argv[1], argv[2]
    for p in (old_path, new_path):
        if not os.path.exists(p):
            print(f"ファイルが無い: {p}", file=sys.stderr)
            return 2

    old_facts = extract_facts(load_text(old_path))
    new_facts = extract_facts(load_text(new_path))

    only_old = {k: v for k, v in old_facts.items() if k not in new_facts}
    only_new = {k: v for k, v in new_facts.items() if k not in old_facts}

    pairs = load_correspondences(check_path_for(new_path))
    only_old, only_new = apply_correspondences(only_old, only_new, pairs)

    def show(title, items):
        print(title)
        if not items:
            print("  (無し)")
        for k in sorted(items):
            print(f"  {k}")

    show(f"新にあって旧にない({new_path}):", only_new)
    show(f"旧にあって新にない({old_path}):", only_old)
    if pairs:
        print(f"(対応表 {check_path_for(new_path)} の {len(pairs)} 組を除外済み)")
    return 1 if (only_old or only_new) else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
