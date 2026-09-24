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
近い順に、著者名とともに出す。-check に改稿の記録が無い章には「(未改稿)」、
archive/v1/ の章には「(旧)」を付ける。

測定の約束: 本文から注の合図(【注N】)を落として文を切る。文末の括弧書きは
括弧の前の語で、「〜のだろう」は疑問の語を含めば問いとして数える。
一人称は「」『』の中を数えない。ダッシュは二倍ダッシュ(——)だけを数える。
「死んだ」「泳いだ」のような撥音便・イ音便の過去形は「た」に数える。
距離の文長の項は、固定の11字で割る(比べる章の顔ぶれで距離が動かないように)。
"""

import os
import re
import signal
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

# 本文から注を指す合図(【注3】)。文末の判定と文長の測定の前に落とす——
# 落とさないと「〜た【注3】。」が「】」で終わる体言止めに数えられ、文長も伸びる。
RE_NOTE_MARK = re.compile(r"【注\d+】")


def strip_note_marks(text):
    return RE_NOTE_MARK.sub("", text)


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


# 「である」に見えて動詞「ある」の文末: 積んである(〜んで+ある)、欄まである(まで+ある)。
# 繋辞の「なんである」「盛んである」「〜さんである」「3日ぶんである」「ままである」は除かない。
# 「でもある」は繋辞(で+も+ある)なので「である」に数える。
RE_ARU_VERB = re.compile(r"((?<![なさぶ盛])んである|(?<!ま)まである)$")


# 撥音便・イ音便の過去形(死んだ・並んだ・膨らんだ・泳いだ)。「〜するんだ」「なんだ」「てっぺんだ」
# 「〜さんだ」のような説明の「のだ」・名詞+だ、「盛んだ」、「商いだ」「嫌いだ」は除く。
RE_ONBIN_PAST = re.compile(
    r"((?:[\u4e00-\u9fff々](?<!盛)|[^\u4e00-\u9fff々うくすつぬふむゆるぐずづぶぷなただいのさぺ])んだ"
    r"|[泳稼塞脱急継仰注紡嗅騒剥研漕繋担揺凪跨]いだ)$"
)
# 数詞の「つ」で終わる名詞(一つ・二つ・いくつ)
RE_COUNTER_TSU = re.compile(r"([一二三四五六七八九幾]つ|ひとつ|ふたつ|みっつ|よっつ|いつつ|むっつ|ななつ|やっつ|ここのつ|いくつ)$")
# 文末の括弧書き(「〜高い(一月あたり)。」)。括弧の前の語で判定する。
RE_TAIL_PAREN = re.compile(r"[((][^(()()]*[))]$")
# 「〜のだろう。」は、疑問の語を含めば問いに数える(「誰が住めるのだろう。」)。
RE_INTERROGATIVE = re.compile(r"(誰|何|なぜ|なに|どこ|いつ|どう|どれ|どの|どんな|いくら|いくつ|幾)")


def sentence_ending(sentence):
    """文末の種別: である/だ/た/る・い/敬体/体言止め/問い/その他"""
    core = strip_note_marks(sentence).strip()
    core = core.rstrip("。!?!?…—― ")
    m = RE_TAIL_PAREN.search(core)
    if m and m.start() > 0:  # 文全体が括弧なら、中身で判定する
        core = core[:m.start()]
    core = core.rstrip("。!?!?」』))…—―")
    core = core.rstrip("。!?!?")
    if not core:
        return "その他"
    if RE_KEITAI.search(core):
        return "敬体"
    if RE_ARU_VERB.search(core):
        return "る・い"
    if re.search(r"(である|であった|であろう|でもある)$", core):
        return "である"
    if core.endswith("だろう") and RE_INTERROGATIVE.search(core):
        return "問い"
    if RE_ONBIN_PAST.search(core):  # 「死んだ」「泳いだ」は過去の「た」
        return "た"
    if core.endswith("だ") or core.endswith("だろう"):
        return "だ"
    if core.endswith("た"):
        return "た"
    if core.endswith("か"):
        return "問い"
    if RE_COUNTER_TSU.search(core):  # 「王国一つ。」は体言止め(「つ」を動詞の終止形と読まない)
        return "体言止め"
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


RE_QUOTED_SPAN = re.compile(r"「[^「」]*」|『[^『』]*』")
RE_FIRST_PERSON = re.compile(r"私(?![立語物淑心情服製有設営鉄道費財掠企募塾学権邸])|筆者")


def measure_text(paras):
    """段落のリストを測る。文と字数は注の合図(【注N】)を落として数える。"""
    paras = [strip_note_marks(p) for p in paras]
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
    # 一人称: 「」『』の中(引用・人の言葉)の「私」は著者の一人称ではないので数えない。
    # 私立・私有・私鉄・私掠船などの熟語も除く。
    unquoted = RE_QUOTED_SPAN.sub("", joined)
    ichi = len(RE_FIRST_PERSON.findall(unquoted))
    kakko = len(re.findall(r"[((]", joined))
    # ダッシュは二倍ダッシュ(——)だけを数える。一本の「—」は区間・範囲の記号(モスクワ—ヤクーツク)。
    dash = len(re.findall(r"――|——", joined))
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


RE_REVISED = re.compile(r"^## 改稿", re.M)


def is_revised(chapter_path):
    """章の -check に改稿の記録(「## 改稿: …」「## 改稿(…)」の見出し)があるか。"""
    chk = re.sub(r"\.md$", "-check.md", chapter_path)
    if not os.path.exists(chk):
        return False
    with open(chk, encoding="utf-8") as f:
        return bool(RE_REVISED.search(f.read()))


# 設計表の文の長さの区分(章の本文の平均文長): 短=30字未満、中=30〜40字、長=40字超
# 距離の文長の項を割る字数。以前は比べる全章の文長の散らばり(標準偏差)で割っていたが、それだと
# 関係の無い章の書き直しで二章の間の距離が動き、最近傍が入れ替わる。2026-09-24 の88章の散らばり
# (11.0字)に固定する。
LEN_SCALE = 11.0

LENGTH_CLASS = {
    "短": lambda x: x < 30.0,
    "中": lambda x: 30.0 <= x <= 40.0,
    "長": lambda x: x > 40.0,
}
LENGTH_RANGE = {"短": "30字未満", "中": "30〜40字", "長": "40字超"}


def design_length_class(author):
    """声の設計表から、その著者の文の長さの区分(短/中/長)を返す。"""
    path = os.path.join(ROOT, "authors", "声の設計表.md")
    if not author or not os.path.exists(path):
        return None
    with open(path, encoding="utf-8") as f:
        for line in f:
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if len(cells) > 2 and cells[0] == author:
                return cells[2] if cells[2] in LENGTH_CLASS else None
    return None


def length_verdict(author, avg):
    """手引き6節2(a): 章の本文の平均文長が設計表の区分に入るか。"""
    cls = design_length_class(author)
    if not cls:
        return None
    ok = LENGTH_CLASS[cls](avg)
    return f"文の長さの区分: 設計表={cls}({LENGTH_RANGE[cls]})、実測={avg:.1f}字 → {'合' if ok else '外れ'}"


def compare(target):
    mapping = load_index_assignments()
    entries = []  # (相対パス, 著者名, 表示用の著者, 旧か, 未改稿か, パス)
    for rel, author in sorted(mapping.items()):
        for prefix, tag in (("", ""), (os.path.join("archive", "v1"), "旧")):
            p = os.path.join(ROOT, prefix, rel) if prefix else os.path.join(ROOT, rel)
            if os.path.exists(p):
                label = os.path.join(prefix, rel) if prefix else rel
                unrevised = not tag and not is_revised(p)
                if unrevised:
                    tag = "未改稿"  # 第4版の声のまま——比較相手として数えない
                entries.append((label, author, author + (f"({tag})" if tag else ""),
                                tag == "旧", unrevised, p))

    target_abs = os.path.abspath(target)
    target_rel = os.path.relpath(target_abs, ROOT).replace(os.sep, "/")
    own_author = mapping.get(target_rel)
    measures = {}
    for label, _, _, _, _, p in entries:
        measures[label] = measure_chapter(p)["本文"]
    m_target = measure_chapter(target_abs)["本文"]

    std_len = LEN_SCALE

    rows = []
    for label, author, shown, old, unrevised, p in entries:
        if os.path.abspath(p) == target_abs:
            continue
        m = measures[label]
        d_end = sum(
            abs(m["文末"][c] - m_target["文末"][c]) for c in END_CATS[:6]
        )
        d_len = abs(m["平均文長"] - m_target["平均文長"]) / std_len
        rows.append((d_end + d_len, d_end, d_len, label, shown, author, old, unrevised))
    rows.sort()
    print(f"距離(近い順): {target_rel} から(文長の差は{LEN_SCALE:.0f}字で割る)")
    print("  距離   (文末   文長)  章 — 著者")
    for d, de, dl, label, shown, *_ in rows:
        print(f"  {d:5.3f}  ({de:5.3f} {dl:5.3f})  {label} — {shown}")

    # 手引き6節2(b)の判定。「未改稿」の章は比べる相手に数えない。
    counted = [r for r in rows if not r[7]]
    if not own_author or not counted:
        return
    current = [r for r in counted if not r[6]]
    if current:
        c0 = current[0]
        print(f"\n旧版を除いた最近傍: {c0[3]} — {c0[4]}({c0[0]:.3f})")
    own_revised = [r for r in counted if r[5] == own_author and not r[6]]
    top = counted[0]
    print()
    if own_revised:
        if top[5] == own_author and not top[6]:
            print(f"判定(6節2(b)): 合——最近傍は自分の著者の改稿済み章({top[3]})")
        elif top[5] == own_author and top[6]:
            print(f"判定(6節2(b)): 否——最近傍が自分の著者の旧版({top[3]})。旧の声が残っている")
        else:
            # 文長の区分が同じ著者どうしでは、文長の差は声を見分ける材料にならない(区分の中の揺れ)。
            # そのときは文末の分布だけで比べ、自分の著者の改稿済み章が最も近ければ合とする。
            ends_only = sorted((r[1], r) for r in current)
            e0 = ends_only[0][1]
            same_class = design_length_class(top[5]) == design_length_class(own_author)
            if same_class and e0[5] == own_author:
                print(f"判定(6節2(b)): 合——最近傍は文長の区分が同じ他の著者の章({top[3]} — {top[4]})だが、"
                      f"文末の分布だけで比べた最近傍は自分の著者の章({e0[3]}、文末{e0[1]:.3f})")
            else:
                print(f"判定(6節2(b)): 否——最近傍が他の著者の章({top[3]} — {top[4]})")
    else:
        own_old = f"archive/v1/{target_rel}"
        rank = next((i + 1 for i, r in enumerate(counted) if r[3] == own_old), None)
        ok = rank is None or rank > 10
        print(f"判定(6節2(b)、自分の著者の改稿済み章が無いとき): {'合' if ok else '否'}"
              f"——自章の旧版は近い順で{rank if rank else '圏外'}位(10位以内なら否)。"
              "あわせて文の長さの区分(6節2(a))を見る")


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
    rel = os.path.relpath(os.path.abspath(target), ROOT).replace(os.sep, "/")
    verdict = length_verdict(load_index_assignments().get(rel), m["本文"]["平均文長"])
    if verdict:
        print(verdict)
    if do_compare:
        print()
        compare(target)
    return 0


if __name__ == "__main__":
    signal.signal(signal.SIGPIPE, signal.SIG_DFL)  # head などで出力を切っても BrokenPipe を出さない
    sys.exit(main(sys.argv))
