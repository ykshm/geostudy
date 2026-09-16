#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""voice.py — 文体の測定(WRITING.md 4節2(a)、docs/文体改稿の手引き.md 2節)。

使い方:
    python3 scripts/voice.py 章ファイル
    python3 scripts/voice.py 章ファイル --compare

本文(見出し・目次・表・図の行と説明・プロフィール・注を除く)と注を分けて、
文数、平均文長と散らばり、文末の分布(である/だ/た/る・い/敬体/体言止め)、
段落数と平均・最長段落長、一人称・括弧・ダッシュの千字あたりの回数、
冒頭段落の型(場面/数字/地図/問い/引用/その他)を出す。

--compare は authors/index.md を読み、同じ測定を全章と archive/v1/ の全章に
掛けて、指定章から各章までの距離(文末分布の差の和と、標準化した文長の差の和)を
近い順に、著者名とともに出す。
"""

import os
import re
import sys
import statistics

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ---------------------------------------------------------------- 章の解析

RE_SECTION = re.compile(r"^## (\d+)\. ?(.*)")
RE_FIG = re.compile(r"^図\d+[::]")
RE_NOTE_HEAD = re.compile(r"^### 注")
RE_NOTE_ITEM = re.compile(r"^注(\d+)[::]\s*(.*)")


def parse_chapter(path):
    """章ファイルを読み、本文段落と注に分ける。

    返り値: dict
      front:    第1節より前の本文段落のリスト(プロフィール・目次・図・表を除く)
      sections: [(節番号, 節題, 本文段落のリスト, 注のリスト)] の並び
                注は (注番号, 全文) の組
    """
    with open(path, encoding="utf-8") as f:
        lines = f.read().split("\n")

    front = []
    sections = []  # [num, title, paras, notes]
    cur_paras = front
    cur_notes = None
    in_notes = False
    buf = []
    skip_block = False  # 目次・著者行・図の説明の段落を読み飛ばす
    fig_caption_pending = False

    def flush():
        nonlocal buf
        text = "".join(buf).strip()
        if text:
            if in_notes:
                m = RE_NOTE_ITEM.match(text)
                if m and cur_notes is not None:
                    cur_notes.append((int(m.group(1)), text))
            else:
                cur_paras.append(text)
        buf = []

    for line in lines:
        stripped = line.strip()
        if not stripped:
            flush()
            skip_block = False
            if fig_caption_pending:
                fig_caption_pending = False
            continue
        m = RE_SECTION.match(line)
        if m:
            flush()
            skip_block = False
            in_notes = False
            sec = [int(m.group(1)), m.group(2), [], []]
            sections.append(sec)
            cur_paras = sec[2]
            cur_notes = sec[3]
            continue
        if RE_NOTE_HEAD.match(line):
            flush()
            skip_block = False
            in_notes = True
            continue
        if line.startswith("#"):  # 章題・その他の見出し
            flush()
            skip_block = False
            in_notes = False if line.startswith("## ") else in_notes
            continue
        if skip_block:
            continue
        if stripped == "目次" or line.startswith("**著者"):
            flush()
            skip_block = True
            continue
        if line.startswith("|"):  # 表
            flush()
            continue
        if RE_FIG.match(stripped):  # 図の行。続く段落は説明
            flush()
            fig_caption_pending = True
            continue
        if fig_caption_pending:  # 図の説明の段落
            continue
        buf.append(line)
    flush()

    return {"front": front, "sections": sections, "path": path}


def body_paragraphs(parsed):
    paras = list(parsed["front"])
    for _, _, ps, _ in parsed["sections"]:
        paras.extend(ps)
    return paras


def note_items(parsed):
    notes = []
    for _, _, _, ns in parsed["sections"]:
        notes.extend(ns)
    return notes


def note_voice_segment(note_text):
    """注の全文から、頭の「注N: 」と末尾の「出典: 」以降を落とした声の段を返す。"""
    text = re.sub(r"^注\d+[::]\s*", "", note_text)
    idx = text.find("出典:")
    if idx < 0:
        idx = text.find("出典:")
    if idx >= 0:
        text = text[:idx]
    return text.strip()


# ---------------------------------------------------------------- 文の測定

OPEN_Q = "「『(("
CLOSE_Q = "」』))"


def split_sentences(text):
    """。!?で区切る。「」『』()の中では区切らない。"""
    sents = []
    depth = 0
    buf = []
    for ch in text:
        buf.append(ch)
        if ch in OPEN_Q:
            depth += 1
        elif ch in CLOSE_Q:
            depth = max(0, depth - 1)
        elif ch in "。!?!?" and depth == 0:
            s = "".join(buf).strip()
            if s:
                sents.append(s)
            buf = []
    tail = "".join(buf).strip()
    if tail:
        sents.append(tail)
    return sents


RE_KEITAI = re.compile(
    r"(です|ます|ません|でした|ました|でしょう|ましょう|ですね|ですよ|ですか|ますか|ませんか|ください)[かねよ]?$"
)
KANA_RUI = set("るいうくすつぬむぶぐずゆふじ")


def sentence_ending(sentence):
    """文末の種別: である/だ/た/る・い/敬体/体言止め/その他"""
    core = sentence.rstrip("。!?!?」』))…—―")
    core = core.rstrip("。!?!?")
    if not core:
        return "その他"
    if RE_KEITAI.search(core):
        return "敬体"
    if re.search(r"(である|であった|であろう|でもある)$", core):
        return "である"
    if core.endswith("だ") or core.endswith("だろう"):
        return "だ"
    if core.endswith("た"):
        return "た"
    if core.endswith("か"):
        return "問い"
    last = core[-1]
    if last in KANA_RUI or core.endswith("ない") or core.endswith("しまう"):
        return "る・い"
    # 平仮名で終わらない(漢字・カタカナ・数字・英字・引用符)なら体言止め
    if not ("ぁ" <= last <= "ん"):
        return "体言止め"
    return "その他"


END_CATS = ["である", "だ", "た", "る・い", "敬体", "体言止め", "問い", "その他"]


def first_para_type(par):
    """冒頭段落の型(場面/数字/地図/問い/引用/その他)。目安の見立てである。"""
    if not par:
        return "無し"
    head = par[:60]
    sents = split_sentences(par)
    first = sents[0] if sents else par
    if "地図" in head:
        return "地図"
    if par.startswith("「") or par.startswith("『"):
        return "引用"
    if first.rstrip("。").endswith("か") or first.endswith("?") or first.endswith("?"):
        return "問い"
    if re.search(r"[0-90-9]", first):
        return "数字"
    if sentence_ending(first) in ("る・い", "た", "体言止め"):
        return "場面"
    return "その他"


def measure_text(paras):
    """段落のリストを測る。"""
    sents = []
    for p in paras:
        sents.extend(split_sentences(p))
    total_chars = sum(len(p) for p in paras)
    lens = [len(s) for s in sents]
    endings = {c: 0 for c in END_CATS}
    for s in sents:
        endings[sentence_ending(s)] += 1
    n = len(sents) or 1
    result = {
        "段落数": len(paras),
        "文数": len(sents),
        "総字数": total_chars,
        "平均文長": (sum(lens) / n) if lens else 0.0,
        "文長の散らばり": statistics.pstdev(lens) if len(lens) > 1 else 0.0,
        "平均段落長": (total_chars / len(paras)) if paras else 0.0,
        "最長段落長": max((len(p) for p in paras), default=0),
        "文末": {c: endings[c] / n for c in END_CATS},
        "文末数": endings,
    }
    per1000 = 1000.0 / total_chars if total_chars else 0.0
    joined = "\n".join(paras)
    ichi = len(re.findall(r"私(?![立語物淑心情服製])|筆者", joined))
    kakko = len(re.findall(r"[((]", joined))
    dash = len(re.findall(r"――|——|—|―", joined))
    result["一人称/千字"] = ichi * per1000
    result["括弧/千字"] = kakko * per1000
    result["ダッシュ/千字"] = dash * per1000
    return result


def measure_chapter(path):
    parsed = parse_chapter(path)
    body = body_paragraphs(parsed)
    notes = [note_voice_segment(t) for _, t in note_items(parsed)]
    notes = [t for t in notes if t]
    m_body = measure_text(body)
    m_body["冒頭段落の型"] = first_para_type(body[0] if body else "")
    m_notes = measure_text(notes)
    return {"本文": m_body, "注": m_notes, "path": path}


# ---------------------------------------------------------------- 表示

def fmt_measure(m, label):
    out = [f"[{label}]"]
    out.append(
        f"  段落数 {m['段落数']}  文数 {m['文数']}  総字数 {m['総字数']}"
    )
    out.append(
        f"  平均文長 {m['平均文長']:.1f}字 (散らばり {m['文長の散らばり']:.1f})"
        f"  平均段落長 {m['平均段落長']:.0f}字  最長段落 {m['最長段落長']}字"
    )
    ends = "  ".join(
        f"{c} {m['文末'][c]*100:.0f}%" for c in END_CATS if m["文末数"][c] or c in END_CATS[:6]
    )
    out.append(f"  文末: {ends}")
    out.append(
        f"  一人称 {m['一人称/千字']:.2f}/千字  括弧 {m['括弧/千字']:.2f}/千字"
        f"  ダッシュ {m['ダッシュ/千字']:.2f}/千字"
    )
    if "冒頭段落の型" in m:
        out.append(f"  冒頭段落の型: {m['冒頭段落の型']}")
    return "\n".join(out)


# ---------------------------------------------------------------- 比較

def load_index_assignments():
    """authors/index.md から 章ファイル→著者名 の対応を返す。"""
    path = os.path.join(ROOT, "authors", "index.md")
    mapping = {}
    with open(path, encoding="utf-8") as f:
        for line in f:
            m = re.match(r"\|[^|]*\|\s*(text/[^|]+?\.md)\s*\|\s*([^((|]+)", line)
            if m:
                mapping[m.group(1).strip()] = m.group(2).strip()
    return mapping


def compare(target):
    mapping = load_index_assignments()
    entries = []  # (相対パス, 著者, 測定)
    for rel, author in sorted(mapping.items()):
        for prefix, tag in (("", ""), (os.path.join("archive", "v1"), "旧")):
            p = os.path.join(ROOT, prefix, rel) if prefix else os.path.join(ROOT, rel)
            if os.path.exists(p):
                label = os.path.join(prefix, rel) if prefix else rel
                entries.append((label, author + (f"({tag})" if tag else ""), p))

    target_abs = os.path.abspath(target)
    measures = {}
    for label, author, p in entries:
        measures[label] = (author, measure_chapter(p)["本文"])
    m_target = measure_chapter(target_abs)["本文"]

    lens = [m["平均文長"] for _, m in measures.values()] + [m_target["平均文長"]]
    std_len = statistics.pstdev(lens) or 1.0

    rows = []
    for label, (author, m) in measures.items():
        if os.path.abspath(os.path.join(ROOT, label)) == target_abs:
            continue
        d_end = sum(
            abs(m["文末"][c] - m_target["文末"][c]) for c in END_CATS[:6]
        )
        d_len = abs(m["平均文長"] - m_target["平均文長"]) / std_len
        rows.append((d_end + d_len, d_end, d_len, label, author))
    rows.sort()
    print(f"距離(近い順): {os.path.relpath(target_abs, ROOT)} から")
    print("  距離   (文末   文長)  章 — 著者")
    for d, de, dl, label, author in rows:
        print(f"  {d:5.3f}  ({de:5.3f} {dl:5.3f})  {label} — {author}")


def main(argv):
    args = [a for a in argv[1:] if a != "--compare"]
    do_compare = "--compare" in argv[1:]
    if not args:
        print(__doc__)
        return 1
    target = args[0]
    if not os.path.exists(target):
        print(f"ファイルが無い: {target}", file=sys.stderr)
        return 1
    m = measure_chapter(target)
    print(f"測定: {target}")
    print(fmt_measure(m["本文"], "本文"))
    print(fmt_measure(m["注"], "注(声の段)"))
    if do_compare:
        print()
        compare(target)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
