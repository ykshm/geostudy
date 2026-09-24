#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""tenken.py — 点検役(目隠し役・照合役)に渡す文面を組む(docs/文体改稿の手引き.md 2節)。

四つの用法:

  python3 scripts/tenken.py mekakushi 章 [--key 答えファイル]
      authors/声の設計表.md から全著者の名前と声の軸(文体・文の長さ・文末の
      偏り・一人称・言い切り・脱線・冒頭の型・締めの型)だけを読む(専門・
      音叉・解禁は渡さない)。章から本文の段落三つ(冒頭=前書きと第1節から・
      中ほどの節・終節から各一つ)と注一つ(声の段があるもの)を抜く。節番号や
      他の章への言及を含む段落は、ほかに候補があれば抜かない。当て馬として、
      別の著者に割り振られた章のうち -check に改稿の記録(「## 改稿」の見出し)
      があるものから本文の段落二つを抜く(無ければ当て馬なし)——一つは文末の
      分布と平均文長で最も近い他の著者の章から、一つは無作為に別の著者から。全部を無作為に
      並べ替えて番号を振り、依頼の一文と答えの書式を添えた文面を stdout に
      出す。番号と出所の対応表は --key のファイルに書き、stdout には含めない。

  python3 scripts/tenken.py shogo 章 節 [--taisho] [--sai]
      節は番号。0(または「前書き」)は第1節より前の本文(章の冒頭)。
      設計表の当該著者の行、文体カードの物差しの節(声・この人はこう書く・
      台帳からの解禁・観測された癖。更新記録・代表章・調律は載せない)、
      文体台帳の全文、当該節の本文と注を、一つの文面に組む。文面の頭に、
      この一節の章の中の位置と、開き・締めの軸を判定するか(開き=章の冒頭、
      締め=終節だけ)と、機械の測定(平均文長・文末の内訳)を置く。終節には
      参照として章の冒頭の段落を添える。図の行と説明文は据え置き部分なので
      印に置き換える。章の本文の平均文長と区分を載せ、文の長さはそれで判定させる
      (一節の測定は参考)。前書き(0)には、前書きの合図が呼ぶ注(紙面では第1節の
      注にある)を添える。文体台帳は項目行だけを載せる。--taisho を付けると末尾に
      「対照を求める」と足す。--sai は以前の減量版の名残で、いまは初回と同じ文面。

  python3 scripts/tenken.py sample 段落ファイル… [--key 答えファイル]
      工程A用。設計表の声の軸と、著者ごとの試し書きの段落(ファイル名に著者の
      ローマ字名を含める)から、目隠しの文面と答えを組む。

  python3 scripts/tenken.py selfcheck 章 [節]
      照合役に掛ける前の機械検査。節を省くと前書きを含む全節。指摘(終了
      コード1): 400字を超える段落(本文と、注の声の段)、文体台帳と -check の
      臨時規則から拾った禁句の本文一致、旧版(archive/v1/)より少ない段落・
      違う注の番号・違う節の並び。参考情報: 節ごとの文末の内訳、70字を超える
      文、ダッシュの数、段落末の決め文句(「わけです。」等)、留保の無い称号語、
      頻度の癖の語の回数、節・章への言及(「5節の」「次の節」「別の章」。「この章」
      「この節」と注の番号は拾わない。図の説明文も見る。出典の「3.1.3節」は除く)、図の説明文の禁句、旧版より
      多い段落、設計表の文末の語が一つも無い段落と注(目隠しで外れやすい)。指摘が残る文面を照合役に回さない(docs/文体改稿の手引き.md 5節)。

組んだ文面はそのままサブエージェントに渡す。一語も足さない(WRITING.md 5節)。
"""

import os
import random
import re
import signal
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

RE_NOTE_MARK = voice.RE_NOTE_MARK


def pick_paragraph(paras, rng):
    """引用に足る長さの段落を優先して一つ選ぶ。節番号や他の章への言及(「5節の」)を
    含む段落は、目隠し役に汚染と判定されるので、ほかに候補があれば選ばない。"""
    clean_pool = [p for p in paras if not section_refs(clean(p))]
    base = clean_pool or paras
    good = [p for p in base if len(p) >= 80]
    pool = good or base
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
    # 冒頭の一つは、前書き(第1節より前の本文)と第1節を合わせた中から選ぶ——
    # 章の開きの型は前書きに置かれることが多く、第1節だけでは掛からない。
    front = [("前書き", p) for p in parsed["front"]]
    opening = front + [(f"{first[0]}節", p) for p in first[2]]
    choice = pick_paragraph([p for _, p in opening], rng)
    if choice:
        where = next(w for w, p in opening if p == choice)
        items.append((f"{rel_chapter(chapter)} {where}(冒頭)", clean(choice)))
    for label, sec in (("中ほどの節", mid), ("終節", last)):
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

    # 当て馬: 別の著者の、-check に改稿の記録(「## 改稿」の見出し)がある章から二段落
    ch_authors = load_chapter_authors()
    own_author = ch_authors.get(rel_chapter(chapter))
    decoy_pool = []
    for rel, author in ch_authors.items():
        if author == own_author:
            continue
        full = os.path.join(ROOT, rel)
        if os.path.exists(full) and voice.is_revised(full):
            decoy_pool.append((rel, author))
    rng.shuffle(decoy_pool)
    # 一本目は、測りで最も近い他の著者の章から取る(紛らわしい声を必ず混ぜる)。
    # 二本目は、残りから無作為に別の著者を取る。
    if decoy_pool:
        m_self = voice.measure_chapter(chapter)["本文"]

        def closeness(item):
            m = voice.measure_chapter(os.path.join(ROOT, item[0]))["本文"]
            return (sum(abs(m["文末"][c] - m_self["文末"][c]) for c in voice.END_CATS[:6])
                    + abs(m["平均文長"] - m_self["平均文長"]) / 10.0)
        nearest = min(decoy_pool, key=closeness)
        decoy_pool.remove(nearest)
        decoy_pool.insert(0, nearest)
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

RE_TOC_ITEM = re.compile(r"^\d+\.\s")


def chapter_lines(chapter):
    with open(chapter, encoding="utf-8") as f:
        return f.read().split("\n")


def front_lines(lines):
    """前書き(目次の後から第1節の見出しの手前まで)の行。プロフィール・目次・表は除く。"""
    out = []
    state = "head"  # head → toc → front
    for line in lines:
        if voice.RE_SECTION.match(line):
            break
        s = line.strip()
        if state == "head":
            if s == "目次":
                state = "toc"
            continue
        if state == "toc":
            if not s or RE_TOC_ITEM.match(s):
                continue
            state = "front"
        if line.startswith("|"):  # 州のプロフィール表などの表
            continue
        out.append(line)
    return out


def section_lines(lines, sec_num):
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
    return out


def drop_figures(lines):
    """図の行と説明の段落を一行の印に置き換える(据え置き部分——照合の対象外)。"""
    out = []
    skipping = False
    for line in lines:
        s = line.strip()
        m = voice.RE_FIG.match(s)
        if m:
            label = s.split(":")[0].split(":")[0]
            out.append(f"〔{label}: 図の行と説明文は据え置き部分のため省略〕")
            skipping = True
            continue
        if skipping:
            if not s:
                skipping = False
                out.append(line)
            continue
        out.append(line)
    return out


def section_text(chapter, sec_num):
    """当該節(0 は前書き)の原文。図の行と説明文は印に置き換える。"""
    lines = chapter_lines(chapter)
    part = front_lines(lines) if sec_num == 0 else section_lines(lines, sec_num)
    return "\n".join(drop_figures(part)).strip()


# 照合役に渡す文体カードの節。初回も再照合(--sai)も同じ物差しにする——
# 回によって載る節が違うと、同じ文面への判定が入れ替わる。
CARD_KEEP = ("声", "この人はこう書く", "台帳からの解禁", "観測された癖")


def card_for_shogo(card):
    """文体カードから、照合の物差しになる節だけを残す(更新記録・代表章・調律は載せない)。"""
    keep = []
    keeping = False
    for line in card.split("\n"):
        if line.startswith("## "):
            keeping = any(line[3:].startswith(k) for k in CARD_KEEP)
        if keeping:
            keep.append(line)
    return "\n".join(keep).strip() or card


def slim_ledger(ledger):
    """--sai 用: 文体台帳から項目行(と節見出し)だけを残す。"""
    keep = []
    section = None
    for line in ledger.split("\n"):
        if line.startswith("## "):
            section = line
            continue
        if line.startswith("- ") and section and "更新記録" not in section:
            if section not in keep:
                keep.append(section)
            keep.append(line)
    return "\n".join(keep).strip() or ledger


def measure_line(paras):
    m = voice.measure_text(paras)
    if not m["文数"]:
        return "本文の文なし"
    ends = "、".join(
        f"{c}{m['文末数'][c]}" for c in voice.END_CATS if m["文末数"][c]
    )
    return (f"文{m['文数']}、平均文長{m['平均文長']:.1f}字、最長段落{m['最長段落長']}字。"
            f"文末の内訳: {ends}")


def cmd_shogo(chapter, sec_num, taisho, sai=False):
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
            card = card_for_shogo(f.read().strip())
    with open(LEDGER, encoding="utf-8") as f:
        ledger = slim_ledger(f.read().strip())  # 初回も再照合も同じ物差し(項目行だけ)

    parsed = voice.parse_chapter(chapter)
    sec_nums = [s[0] for s in parsed["sections"]]
    has_front = bool(parsed["front"])
    if sec_num == 0:
        if not has_front:
            print("前書き(第1節より前の本文)が無い", file=sys.stderr)
            return 1
        paras = parsed["front"]
    elif sec_num in sec_nums:
        paras = next(s[2] for s in parsed["sections"] if s[0] == sec_num)
    else:
        print(f"節が見つからない: {sec_num}", file=sys.stderr)
        return 1
    body = section_text(chapter, sec_num)

    last = sec_nums[-1] if sec_nums else None
    opening = sec_num == 0 or (sec_num == sec_nums[0] and not has_front)
    closing = sec_num == last
    if sec_num == 0:
        where = f"前書き(第1節より前。章の冒頭。この章は全{len(sec_nums)}節)"
    elif closing:
        where = f"第{sec_num}節(終節。全{len(sec_nums)}節)"
    else:
        where = f"第{sec_num}節(全{len(sec_nums)}節の途中の節)"
        if opening:
            where = f"第{sec_num}節(章の冒頭を含む。前書きは無い。全{len(sec_nums)}節)"

    out = []
    out.append(f"著者「{author}」の一節の照合を求める。")
    out.append("")
    out.append(f"この一節の位置: {where}")
    out.append(f"開きの軸: {'判定する(章の開き)' if opening else '対象外(章の開きではない)'}")
    out.append(f"締めの軸: {'判定する(章の締め)' if closing else '対象外(章の締めではない)'}")
    m_ch = voice.measure_text(voice.body_paragraphs(parsed))
    cls = row.get("文の長さ", "")
    rng = {"短": "30字未満", "中": "30〜40字", "長": "40字超"}.get(cls, "")
    ok = voice.LENGTH_CLASS[cls](m_ch["平均文長"]) if cls in voice.LENGTH_CLASS else None
    out.append(f"章の本文の平均文長: {m_ch['平均文長']:.1f}字(設計表の区分={cls}・{rng}"
               f"{'、区分に入る' if ok else '、区分の外' if ok is False else ''})。"
               "文の長さの軸はこの章の平均で判定する。")
    out.append(f"機械の測定(この一節の本文。注の合図は除く。参考): {measure_line(paras)}")
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
    if closing and not opening:
        first = parsed["front"][0] if has_front else (parsed["sections"][0][2] or [""])[0]
        out.append("参照(照合の対象外): 章の冒頭の段落")
        out.append("")
        out.append(clean(first))
        out.append("")
    out.append("一節の本文と注:")
    out.append("")
    out.append(body)
    if sec_num == 0:
        called = {int(n) for p in parsed["front"] for n in re.findall(r"【注(\d+)】", p)}
        front_notes = [t for _, _, _, ns in parsed["sections"] for n, t in ns if n in called]
        if front_notes:
            out.append("")
            out.append("前書きの合図が呼ぶ注(紙面では第1節の注の下にある):")
            out.append("")
            out.extend(front_notes)
    if taisho:
        out.append("")
        out.append("対照を求める")
    print("\n".join(out))
    return 0


# ---------------------------------------------------------------- selfcheck

RE_QUOTED = re.compile(r"「([^「」]+)」")
RE_TITLE_WORDS = re.compile(r"(最初の|初めて|世界初|全米初|唯一|元祖)")
RE_RESERVE = re.compile(r"(とされ|と言われ|と呼ばれ|とみなされ|は諸説|かもしれ|らしい|言い切りません|確かめられて)")
RE_KIME_END = re.compile(r"(わけです|のである|のだ)[。]?$")
BAN_HINT = re.compile(r"(禁止|禁句|使わない|使わず|しない|せず|置かない|閉じない|開かない|避け|封印|再利用)")
FREQ_HINT = re.compile(r"(連発|毎回|多用|寄る|過半|数回まで|1回まで|一度まで)")
# 置き場所を禁じる規則(「A」を1節末尾に置かない)。語そのものは他の場所で使ってよい
POS_HINT = re.compile(r"(節末|節の末|末尾|節頭|節の頭|冒頭|終節|段落末|段落の頭|章頭|章末|前書き|各節|分散|で閉じ|で開)")
# 禁止ではなく、使う側の語を示す言い方(「A」で開く、「B」に置き換える)
USE_HINT = re.compile(r"^[^。]{0,6}?(で開|で閉じ|で止め|で組|で刻|に置き換|に替え|へ替え|に寄せ|を使う|で書く|を置く)")
# 臨時規則のうち、禁句を拾わない行(軸・声の確認・材料)
RINJI_SKIP = re.compile(r"^[-*\s]*(今回の軸|声の確認|材料|③|④)")
# 同じ組に並ぶ「」どうしの間(「A」「B」、「A」・「B」、「A」や「B」)
LIST_GAP = re.compile(r"^[、・/や と,,\s]*$")
# 章の中の節への言及と、他の章への言及(目隠しで汚染と判定されうる。章の独立にも当たる)。
# 出典の資料の中の節番号(「3.1.3節」)は拾わない。本文の「(注3)」は注を呼ぶ合図の書き方の
# 一つ(WRITING.md 2節)で、著者も章も明かさないので拾わない。
RE_SEC_REF = re.compile(
    r"((?<![0-90-9..])第?[0-90-9]+節|第[一二三四五六七八九十]+節"
    r"|(別の|他の|前の|次の)章|(前の|次の|先の|後の)節|終節)"
)


def section_refs(text):
    """段落(注なら声の段だけ)の中の節・注・章への言及を返す。"""
    seg = voice.note_voice_segment(text) if re.match(r"^注\d+[::]", text) else text
    return [m.group(0) for m in RE_SEC_REF.finditer(RE_NOTE_MARK.sub("", seg))]


def split_rule_sentences(line):
    """臨時規則の一行を文に切る(「」の中では切らない)。"""
    return [s for s in voice.split_sentences(line) if s.strip()]


def banned_in_sentence(sent):
    """一文から禁句を拾う。並んだ「」は一組として、組の直後の語で禁止か使用かを決める。"""
    spans = [(m.start(), m.end(), m.group(1)) for m in RE_QUOTED.finditer(sent)]
    if not spans:
        return []
    groups = [[spans[0]]]
    for prev, cur in zip(spans, spans[1:]):
        gap = sent[prev[1]:cur[0]]
        if LIST_GAP.match(gap):
            groups[-1].append(cur)
        else:
            groups.append([cur])
    sentence_bans = bool(BAN_HINT.search(sent))
    out = []
    for gi, group in enumerate(groups):
        end = group[-1][1]
        nxt = groups[gi + 1][0][0] if gi + 1 < len(groups) else len(sent)
        governing = sent[end:nxt]
        if USE_HINT.search(governing) and not BAN_HINT.search(governing):
            continue
        if BAN_HINT.search(governing) or sentence_bans:
            out.extend(q for _, _, q in group)
    return out


def collect_banned_phrases(chapter):
    """文体台帳と、章の -check の臨時規則の節から、禁句(「」内)を集める。

    プレースホルダ(〜・○・/・…)を含む語や3字以下の語は、素朴な文字列一致が
    誤爆するので拾わない。台帳は項目行の全部、-check は禁止の言葉を含む文だけ。
    臨時規則の「今回の軸」「声の確認」の行と、「A」で開く・「B」に置き換える
    のような使う側の語は拾わない。
    返り値: [(語, 出どころ, 種別)]。種別は「禁句」(指摘)/「頻度」(回数を参考に出す)/
    「位置」(置き場所の規則——参考に出す)。
    """
    phrases = []

    def keep(q):
        return len(q) >= 4 and not any(c in q for c in "〜○◯/…—")

    with open(LEDGER, encoding="utf-8") as f:
        section = None
        for line in f.read().split("\n"):
            if line.startswith("## "):
                section = line
            elif line.startswith("- ") and section and "更新記録" not in section:
                kind = ("頻度" if FREQ_HINT.search(line)
                        else "位置" if POS_HINT.search(line) else "禁句")
                for q in RE_QUOTED.findall(line):
                    if keep(q):
                        phrases.append((q, "台帳", kind))

    check_path = re.sub(r"\.md$", "-check.md", chapter)
    if os.path.exists(check_path):
        with open(check_path, encoding="utf-8") as f:
            in_rinji = False
            for line in f.read().split("\n"):
                if line.startswith("## "):
                    in_rinji = "臨時規則" in line
                    continue
                if not in_rinji or RINJI_SKIP.match(line):
                    continue
                for sent in split_rule_sentences(line):
                    kind = ("頻度" if FREQ_HINT.search(sent)
                            else "位置" if POS_HINT.search(sent) else "禁句")
                    for q in banned_in_sentence(sent):
                        if keep(q):
                            phrases.append((q, "臨時規則", kind))

    seen = set()
    out = []
    for q, src, kind in phrases:
        if q not in seen:
            seen.add(q)
            out.append((q, src, kind))
    return out


def phrase_hits(text, q):
    """禁句 q が text に現れる回数。「である」で始まる禁句は、動詞「ある」の
    「積んである」「欄まである」の中の一致を数えない。"""
    n = 0
    start = 0
    while True:
        i = text.find(q, start)
        if i < 0:
            return n
        start = i + 1
        if q.startswith("である") and i > 0:
            if voice.RE_ARU_VERB.search(text[:i + 3]):
                continue
        n += 1


def design_endings(chapter):
    """設計表のその章の著者の「文末の偏り」を、voice.py の文末の種別の集合で返す。"""
    author = load_chapter_authors().get(rel_chapter(chapter))
    row = load_design_rows().get(author or "")
    if not row:
        return set()
    val = re.sub(r"[((].*?[))]", "", row.get("文末の偏り", ""))
    return {w.strip() for w in val.split("+") if w.strip() in voice.END_CATS}


def iter_captions(chapter):
    """図の説明文(図の行の次の段落)を (図N, 本文) で返す。"""
    lines = chapter_lines(chapter)
    out = []
    i = 0
    while i < len(lines):
        s = lines[i].strip()
        if voice.RE_FIG.match(s):
            label = s.split(":")[0].split(":")[0]
            buf = []
            i += 1
            while i < len(lines) and lines[i].strip():
                buf.append(lines[i].strip())
                i += 1
            out.append((label, "".join(buf)))
        i += 1
    return out


def compare_with_archive(chapter, parsed, sections, findings, info):
    """旧版(archive/v1/)と、節ごとの段落数・注の番号を突き合わせる(手引き5節)。"""
    rel = rel_chapter(chapter)
    old_path = os.path.join(ROOT, "archive", "v1", rel)
    if not os.path.exists(old_path):
        return
    old = voice.parse_chapter(old_path)
    old_secs = {s[0]: s for s in old["sections"]}
    wanted = {s[0] for s in sections}
    if 0 in wanted:
        n_old, n_new = len(old["front"]), len(parsed["front"])
        if n_new < n_old:
            findings.append(f"前書きの段落が旧版より少ない({n_old}→{n_new})")
        elif n_new > n_old:
            info.append(f"前書きの段落が旧版より多い({n_old}→{n_new})——-check に段落の対応表があるか")
    for num, _, paras, notes in sections:
        if num == 0:
            continue
        o = old_secs.get(num)
        if not o:
            findings.append(f"{num}節が旧版に無い(節の数・順を変えない)")
            continue
        if len(paras) < len(o[2]):
            findings.append(f"{num}節の段落が旧版より少ない({len(o[2])}→{len(paras)}。段落を減らさない)")
        elif len(paras) > len(o[2]):
            info.append(f"{num}節の段落が旧版より多い({len(o[2])}→{len(paras)})——-check に段落の対応表があるか")
        old_nums = [n for n, _ in o[3]]
        new_nums = [n for n, _ in notes]
        if old_nums != new_nums:
            info.append(f"{num}節に属する注が旧版と違う(旧 {old_nums} → 新 {new_nums})——注を節の末へ移したなら -check に記録")
    if len(wanted) > 1:
        old_all = [n for n, _ in voice.note_items(old)]
        new_all = [n for n, _ in voice.note_items(parsed)]
        if old_all != new_all:
            findings.append(f"注の番号の並びが旧版と違う(旧 {len(old_all)}個 → 新 {len(new_all)}個。番号と数を変えない)")
    if 0 not in wanted or len(wanted) > 1:
        old_n = [s[0] for s in old["sections"]]
        new_n = [s[0] for s in parsed["sections"]]
        if old_n != new_n and len(wanted) > 1:
            findings.append(f"節の番号の並びが旧版と違う(旧 {old_n} → 新 {new_n})")


def cmd_selfcheck(chapter, sec_num=None):
    parsed = voice.parse_chapter(chapter)
    all_secs = []
    if parsed["front"]:
        all_secs.append((0, "前書き", parsed["front"], []))
    all_secs.extend(parsed["sections"])
    sections = all_secs
    if sec_num is not None:
        sections = [s for s in all_secs if s[0] == sec_num]
        if not sections:
            print(f"節が見つからない: {sec_num}", file=sys.stderr)
            return 2

    def where(num):
        return "前書き" if num == 0 else f"{num}節"

    findings = []
    info = []

    # 段落長(本文)と、注の声の段
    for num, title, paras, notes in sections:
        for i, p in enumerate(paras, 1):
            if len(p) > 400:
                findings.append(f"{where(num)} 本文段落{i}が400字を超える({len(p)}字)")
        for n_num, n_text in notes:
            seg = voice.note_voice_segment(n_text)
            if len(seg) > 400:
                findings.append(f"注{n_num}の声の段が400字を超える({len(seg)}字)")

    # 旧版との段落数・注の番号
    compare_with_archive(chapter, parsed, sections, findings, info)

    # 禁句(見出し行は対象外——節題は据え置き部分)
    banned = collect_banned_phrases(chapter)
    for num, title, paras, notes in sections:
        texts = [(f"{where(num)} 本文段落{i}", p) for i, p in enumerate(paras, 1)]
        texts += [(f"注{n}", t) for n, t in notes]
        freq_count = {}
        for label, text in texts:
            for q, src, kind in banned:
                hits = phrase_hits(text, q)
                if not hits:
                    continue
                if kind == "頻度":
                    freq_count[(q, src)] = freq_count.get((q, src), 0) + hits
                elif kind == "位置":
                    info.append(f"{label}に「{q}」({src}の置き場所の規則——置いた場所が規則に当たらないか確かめる)")
                else:
                    findings.append(f"{label}に禁句「{q}」({src})")
            for ref in section_refs(text):
                info.append(f"{label}に節・章への言及「{ref}」——目隠しで汚染と判定されうる。他の章への参照は書かない")
        for (q, src), n in freq_count.items():
            info.append(f"{where(num)} 頻度の癖の語「{q}」が{n}回({src}——数を確かめる)")

    # 図の説明文(据え置き部分): 禁句と節・章への言及を参考に出す
    if sec_num is None:
        for label, text in iter_captions(chapter):
            for q, src, kind in banned:
                if kind == "禁句" and phrase_hits(text, q):
                    info.append(f"{label}の説明文に禁句「{q}」({src}——据え置き部分。直すかは書き手が決める)")
            for ref in section_refs(text):
                info.append(f"{label}の説明文に節・章への言及「{ref}」——言い換えてよい(図を開かなくても通じる具体性は落とさない)")

    # 設計表の文末の偏りの語が一つも無い段落と注(目隠しで他の著者に流れやすい)
    design_ends = design_endings(chapter)
    if design_ends:
        for num, title, paras, notes in sections:
            texts = [(f"{where(num)} 本文段落{i}", p, 80) for i, p in enumerate(paras, 1)]
            texts += [(f"注{n}", voice.note_voice_segment(t), 60) for n, t in notes]
            for label, text, min_len in texts:
                if len(text) < min_len:
                    continue
                ends = {voice.sentence_ending(x) for x in voice.split_sentences(RE_NOTE_MARK.sub("", text))}
                if not ends & design_ends:
                    info.append(f"{label}に設計表の文末({'・'.join(sorted(design_ends))})が一つも無い——目隠しで外れやすい")

    # 参考情報: 節ごとの文末、長文、決め文句の段落末、留保の無い称号語
    for num, title, paras, notes in sections:
        tally = {}
        long_sents = []
        kime = []
        for i, p in enumerate(paras, 1):
            sents = voice.split_sentences(RE_NOTE_MARK.sub("", p))
            for s in sents:
                cat = voice.sentence_ending(s)
                tally[cat] = tally.get(cat, 0) + 1
                if len(s) > 70:
                    long_sents.append(f"段落{i}: {s[:34]}…({len(s)}字)")
            if sents and RE_KIME_END.search(sents[-1].rstrip("。!?!?」』))")):
                kime.append(f"段落{i}末: {sents[-1][:30]}…")
        parts = "  ".join(f"{k}{v}" for k, v in sorted(tally.items(), key=lambda kv: -kv[1]))
        info.append(f"{where(num)} 文末: {parts}")
        for s in long_sents:
            info.append(f"{where(num)} 70字超 {s}")
        for s in kime:
            info.append(f"{where(num)} 決め文句 {s}")
        for i, p in enumerate(paras, 1):
            for s in voice.split_sentences(p):
                if RE_TITLE_WORDS.search(s) and not RE_RESERVE.search(s):
                    info.append(f"{where(num)} 段落{i} 留保の無い称号語: {s[:40]}…")

    dash = sum(p.count("——") for _, _, ps, _ in sections for p in ps)
    info.append(f"ダッシュ(——): {dash}本")

    for f_msg in findings:
        print(f"指摘: {f_msg}")
    for i_msg in info:
        print(f"参考: {i_msg}")
    if not findings:
        print("指摘: 無し")
    return 1 if findings else 0


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

def sec_arg(a):
    """節の指定。0 か「前書き」は第1節より前の本文。"""
    return 0 if a in ("0", "前書き", "mae") else int(a)


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
    sai = "--sai" in args
    args = [a for a in args if a not in ("--taisho", "--sai")]

    if cmd == "mekakushi":
        if len(args) != 1:
            print(__doc__)
            return 2
        return cmd_mekakushi(args[0], key_file)
    if cmd == "shogo":
        if len(args) != 2:
            print(__doc__)
            return 2
        return cmd_shogo(args[0], sec_arg(args[1]), taisho, sai)
    if cmd == "selfcheck":
        if len(args) not in (1, 2):
            print(__doc__)
            return 2
        return cmd_selfcheck(args[0], sec_arg(args[1]) if len(args) == 2 else None)
    if cmd == "sample":
        if not args:
            print(__doc__)
            return 2
        return cmd_sample(args, key_file)
    print(__doc__)
    return 2


if __name__ == "__main__":
    signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    sys.exit(main(sys.argv))
