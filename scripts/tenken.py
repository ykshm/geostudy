#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""tenken.py — 点検役(目隠し役・照合役)に渡す文面を組む(docs/文体改稿の手引き.md 2節)。

三つの用法:

  python3 scripts/tenken.py mekakushi 章 [--key 答えファイル]
      authors/声の設計表.md から全著者の名前と声の軸(文体・文の長さ・文末の
      偏り・一人称・言い切り・脱線・冒頭の型・締めの型)だけを読む(専門・
      音叉・解禁は渡さない)。章から本文の段落三つ(冒頭の節・中ほどの節・
      終節から各一つ)と注一つ(声の段があるもの)を抜く。当て馬として、別の
      著者に割り振られた章のうち -check に「改稿:」の記録があるものから本文の
      段落二つを抜く(無ければ当て馬なし)。全部を無作為に並べ替えて番号を
      振り、依頼の一文と答えの書式を添えた文面を stdout に出す。番号と出所の
      対応表は --key のファイルに書き、stdout には含めない。

  python3 scripts/tenken.py shogo 章 節 [--taisho]
      設計表の当該著者の行、その著者の文体カードの全文、文体台帳の全文、
      当該節の本文と注を、一つの文面に組む。--taisho を付けると末尾に
      「対照を求める」と足す。

  python3 scripts/tenken.py sample 段落ファイル… [--key 答えファイル]
      工程A用。設計表の声の軸と、著者ごとの試し書きの段落(ファイル名に著者の
      ローマ字名を含める)から、目隠しの文面と答えを組む。

組んだ文面はそのままサブエージェントに渡す。一語も足さない(WRITING.md 5節)。
"""

import os
import random
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
import voice  # noqa: E402

DESIGN = os.path.join(ROOT, "authors", "声の設計表.md")
LEDGER = os.path.join(ROOT, "authors", "文体台帳.md")
INDEX = os.path.join(ROOT, "authors", "index.md")

VOICE_AXES = ["文体", "文の長さ", "文末の偏り", "一人称", "言い切り", "脱線", "冒頭の型", "締めの型"]
ALL_COLS = VOICE_AXES + ["解禁", "音叉"]


# ---------------------------------------------------------------- 楽屋の読み込み

def load_design_rows():
    """設計表の表の行を {著者名: {軸: 値}} で返す。"""
    rows = {}
    with open(DESIGN, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line.startswith("|"):
                continue
            cells = [c.strip() for c in line.strip("|").split("|")]
            if len(cells) < len(ALL_COLS) + 1:
                continue
            name = cells[0]
            if name in ("著者", "") or set(name) <= {"-", ":", " "}:
                continue
            rows[name] = dict(zip(ALL_COLS, cells[1:]))
    return rows


def load_author_files():
    """index.md の著者一覧から {著者名: authors/xxx.md} を返す。"""
    mapping = {}
    with open(INDEX, encoding="utf-8") as f:
        for line in f:
            m = re.match(r"\|\s*([^|]+?)\s*\|\s*(authors/[a-z\-]+\.md)\s*\|", line)
            if m:
                mapping[m.group(1)] = m.group(2)
    return mapping


def load_chapter_authors():
    """index.md の割り振りから {章の相対パス: 著者名} を返す。"""
    mapping = {}
    with open(INDEX, encoding="utf-8") as f:
        for line in f:
            m = re.match(r"\|[^|]*\|\s*(text/[^|]+?\.md)\s*\|\s*([^((|]+)", line)
            if m:
                mapping[m.group(1).strip()] = m.group(2).strip()
    return mapping


def rel_chapter(path):
    p = os.path.relpath(os.path.abspath(path), ROOT)
    return p.replace(os.sep, "/")


def fmt_voice_row(name, row):
    parts = [f"{ax}={row.get(ax, '') or '—'}" for ax in VOICE_AXES]
    return f"- {name}: " + " / ".join(parts)


ANSWER_FORMAT = """答えの書式(この形以外で答えない):

文章1: 著者名 / 確信 高・中・低 / 根拠: 「引用」…。文末は である○割・体言止め○割、平均文長およそ○字、…。次点: 著者名(違う点)
文章2: …

一覧の中に該当する声が無いと思うときは「該当なし」と書き、いちばん近い二人と、どこが違うかを書く。"""

REQUEST_LINE = (
    "以下に、著者の名前と声の規定の一覧と、番号を振った無記名の文章がある。"
    "文章ごとに、一覧の誰が書いたかを一人だけ挙げ、根拠を、その文章から引いた文と数で示すこと。"
)


def build_blind_sheet(voice_rows, numbered_texts):
    """voice_rows: {著者名: 軸の辞書}, numbered_texts: [文章のテキスト]"""
    out = [REQUEST_LINE, "", "声の規定の一覧:", ""]
    for name, row in voice_rows.items():
        out.append(fmt_voice_row(name, row))
    out.append("")
    for i, text in enumerate(numbered_texts, 1):
        out.append(f"文章{i}:")
        out.append(text)
        out.append("")
    out.append(ANSWER_FORMAT)
    return "\n".join(out)


# ---------------------------------------------------------------- mekakushi

RE_NOTE_MARK = re.compile(r"【注\d+】")


def pick_paragraph(paras, rng):
    """引用に足る長さの段落を優先して一つ選ぶ。"""
    good = [p for p in paras if len(p) >= 80]
    pool = good or paras
    return rng.choice(pool) if pool else None

def clean(par):
    return RE_NOTE_MARK.sub("", par).strip()


def cmd_mekakushi(chapter, key_file):
    rng = random.SystemRandom()
    design = load_design_rows()
    if not design:
        print("声の設計表に行が無い", file=sys.stderr)
        return 1
    parsed = voice.parse_chapter(chapter)
    secs = [s for s in parsed["sections"] if s[2]]
    if len(secs) < 3:
        print("節が三つ未満の章には使えない", file=sys.stderr)
        return 1

    items = []  # (出所の説明, テキスト)
    first, mid, last = secs[0], secs[len(secs) // 2], secs[-1]
    if mid is first:
        mid = secs[1]
    if mid is last and len(secs) >= 3:
        mid = secs[len(secs) // 2 - 1]
    for label, sec in (("冒頭の節", first), ("中ほどの節", mid), ("終節", last)):
        par = pick_paragraph(sec[2], rng)
        if par:
            items.append((f"{rel_chapter(chapter)} {sec[0]}節({label})", clean(par)))

    notes = []
    for _, _, _, ns in parsed["sections"]:
        for num, text in ns:
            seg = voice.note_voice_segment(text)
            if len(seg) >= 60:
                notes.append((num, seg))
    if notes:
        num, seg = rng.choice(notes)
        items.append((f"{rel_chapter(chapter)} 注{num}", clean(seg)))

    # 当て馬: 別の著者の、-check に「改稿:」の記録がある章から二段落
    ch_authors = load_chapter_authors()
    own_author = ch_authors.get(rel_chapter(chapter))
    decoy_pool = []
    for rel, author in ch_authors.items():
        if author == own_author:
            continue
        chk = os.path.join(ROOT, rel.replace(".md", "-check.md"))
        full = os.path.join(ROOT, rel)
        if os.path.exists(chk) and os.path.exists(full):
            with open(chk, encoding="utf-8") as f:
                if "改稿:" not in f.read():
                    continue
            decoy_pool.append((rel, author))
    rng.shuffle(decoy_pool)
    used_authors = set()
    decoys = []
    for rel, author in decoy_pool:
        if len(decoys) >= 2:
            break
        if author in used_authors and len(decoy_pool) > 2:
            continue
        p = voice.parse_chapter(os.path.join(ROOT, rel))
        paras = voice.body_paragraphs(p)
        par = pick_paragraph(paras, rng)
        if par:
            decoys.append((f"当て馬 {rel}({author})", clean(par)))
            used_authors.add(author)
    items.extend(decoys)

    rng.shuffle(items)
    sheet = build_blind_sheet(design, [t for _, t in items])
    print(sheet)
    if key_file:
        with open(key_file, "w", encoding="utf-8") as f:
            f.write(f"# 答えの対応表: {rel_chapter(chapter)}(著者: {own_author or '不明'})\n")
            for i, (src, _) in enumerate(items, 1):
                f.write(f"文章{i}: {src}\n")
    return 0


# ---------------------------------------------------------------- shogo

def section_text(chapter, sec_num):
    """章ファイルから当該節の原文(見出しから次の節見出しの手前まで)を返す。"""
    with open(chapter, encoding="utf-8") as f:
        lines = f.read().split("\n")
    out = []
    in_sec = False
    for line in lines:
        m = voice.RE_SECTION.match(line)
        if m:
            if in_sec:
                break
            if int(m.group(1)) == sec_num:
                in_sec = True
        if in_sec:
            out.append(line)
    return "\n".join(out).strip()


def cmd_shogo(chapter, sec_num, taisho):
    design = load_design_rows()
    ch_authors = load_chapter_authors()
    author_files = load_author_files()
    rel = rel_chapter(chapter)
    author = ch_authors.get(rel)
    if not author:
        print(f"authors/index.md に割り振りが無い: {rel}", file=sys.stderr)
        return 1
    row = design.get(author)
    if not row:
        print(f"声の設計表に行が無い: {author}", file=sys.stderr)
        return 1
    afile = author_files.get(author)
    card_path = os.path.join(ROOT, afile.replace(".md", "-style.md")) if afile else None
    card = ""
    if card_path and os.path.exists(card_path):
        with open(card_path, encoding="utf-8") as f:
            card = f.read().strip()
    with open(LEDGER, encoding="utf-8") as f:
        ledger = f.read().strip()
    body = section_text(chapter, sec_num)
    if not body:
        print(f"節が見つからない: {sec_num}", file=sys.stderr)
        return 1

    out = []
    out.append(f"著者「{author}」の一節の照合を求める。")
    out.append("")
    out.append("声の規定(声の設計表の行):")
    out.append(fmt_voice_row(author, row))
    out.append(f"- 解禁={row.get('解禁') or '無し'} / 音叉={row.get('音叉') or '—'}")
    out.append("")
    out.append("文体カード:")
    out.append("")
    out.append(card or "(文体カード無し)")
    out.append("")
    out.append("文体台帳(全著者共通の避けたい言い回しと構図):")
    out.append("")
    out.append(ledger)
    out.append("")
    out.append("一節の本文と注:")
    out.append("")
    out.append(body)
    if taisho:
        out.append("")
        out.append("対照を求める")
    print("\n".join(out))
    return 0


# ---------------------------------------------------------------- sample

def cmd_sample(files, key_file):
    rng = random.SystemRandom()
    design = load_design_rows()
    author_files = load_author_files()
    romaji_to_name = {}
    for name, afile in author_files.items():
        stem = os.path.splitext(os.path.basename(afile))[0]
        romaji_to_name[stem] = name

    items = []  # (著者名, テキスト)
    for path in files:
        base = os.path.basename(path)
        matched = [n for stem, n in romaji_to_name.items() if stem in base]
        if not matched:
            print(f"ファイル名に著者のローマ字名が無い: {path}", file=sys.stderr)
            return 1
        name = max(matched, key=len)
        with open(path, encoding="utf-8") as f:
            text = f.read().strip()
        if not text:
            print(f"空のファイル: {path}", file=sys.stderr)
            return 1
        items.append((name, clean(text)))

    rng.shuffle(items)
    sheet = build_blind_sheet(design, [t for _, t in items])
    print(sheet)
    if key_file:
        with open(key_file, "w", encoding="utf-8") as f:
            f.write("# 答えの対応表(試し書き)\n")
            for i, (name, _) in enumerate(items, 1):
                f.write(f"文章{i}: {name}\n")
    return 0


# ---------------------------------------------------------------- main

def main(argv):
    args = list(argv[1:])
    if not args:
        print(__doc__)
        return 2
    cmd = args.pop(0)
    key_file = None
    if "--key" in args:
        i = args.index("--key")
        key_file = args[i + 1]
        del args[i:i + 2]
    taisho = "--taisho" in args
    args = [a for a in args if a != "--taisho"]

    if cmd == "mekakushi":
        if len(args) != 1:
            print(__doc__)
            return 2
        return cmd_mekakushi(args[0], key_file)
    if cmd == "shogo":
        if len(args) != 2:
            print(__doc__)
            return 2
        return cmd_shogo(args[0], int(args[1]), taisho)
    if cmd == "sample":
        if not args:
            print(__doc__)
            return 2
        return cmd_sample(args, key_file)
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
