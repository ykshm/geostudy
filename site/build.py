#!/usr/bin/env python3
"""text/ のMarkdown正本から静的サイト(_site/)を生成する。

原則: 正本(text/, authors/, README.md)には一切手を入れない。
書式の解釈と変換はすべてこのスクリプトが吸収する。
章の書式が壊れている場合はビルドを失敗させる(lint を兼ねる)。
変換規則と除外の方針は site/README.md を参照。
"""

import html
import json
import re
import shutil
import sys
from pathlib import Path

import markdown

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "_site"

# シリーズの一覧(トップページの表示順)。text/<キー>/ の章を _site/<キー>/ に出す。
# 章別地図のデータは site/geo/<キー>/<slug>.json、出力は _site/maps/<キー>-<slug>.html。
SERIES = {
    "usa": "第1シリーズ: アメリカ50州",
    "japan": "第2シリーズ: 臥遊風土記",
}

MD = markdown.Markdown(extensions=["tables"])

errors: list[str] = []
warnings: list[str] = []


def err(msg: str) -> None:
    errors.append(msg)


def warn(msg: str) -> None:
    warnings.append(msg)


# ---------------------------------------------------------------- 共通部品

CSS = (ROOT / "site" / "style.css").read_text(encoding="utf-8")

PAGE = """<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<style>
{css}
</style>
</head>
<body>
<header class="site-header"><a href="{home}">geostudy</a></header>
<main>
{body}
</main>
<footer class="site-footer">
<p>本文の正本は <a href="https://github.com/ykshm/geostudy">GitHubリポジトリ</a> のMarkdownファイルです。このページはそこから機械生成されています。</p>
</footer>
{extra}</body>
</html>
"""


def render_page(title: str, body: str, home: str, extra: str = "") -> str:
    return PAGE.format(title=html.escape(title), css=CSS, body=body, home=home,
                       extra=extra)


# ---------------------------------------------------------------- 章の変換

FIG_RE = re.compile(r"^\u56f3(\d+): (.+?)[\uff08(](.+?)[\uff09)]\s*$")
SEC_RE = re.compile(r"^## (\d+)\. (.+?)\s*$")
NOTE_RE = re.compile(r"^注(\d+): ")
TOC_ITEM_RE = re.compile(r"^(\d+)\. (.+?)\s*$")


def transform_chapter(path: Path, author_file: Path | None,
                      geo: dict | None = None) -> tuple[str, str]:
    """章のMarkdownを、書式検査をかけながらHTML断片に変換する。

    geo はウェブ版限定の地図設定(site/geo/*.json)。渡されると、指定の節/注の
    初出の地名を <a class="geo" data-i="N"> でリンク化し、章末におまけ地図を
    付ける。正本のMarkdownには一切手を入れない。

    戻り値: (章題, 本文HTML)
    """
    rel = path.relative_to(ROOT)
    lines = path.read_text(encoding="utf-8").split("\n")

    geo_places = list(geo["places"]) if geo else []
    geo_done: set[int] = set()
    cur_sec = ""

    def linkify(text: str, *, sec: str = "", note: str = "") -> str:
        """text 中の対象地名(その節/注が指定と一致し、未リンクのもの)の
        初出をリンク化して返す。text はHTML文脈(エスケープ済みか、
        markdownに生HTMLとして通る行)であること。"""
        for p in geo_places:
            if p["i"] in geo_done:
                continue
            if note:
                if p.get("note") != note:
                    continue
            elif not sec or p.get("sec") != sec:
                continue
            pos = text.find(p["name"])
            if pos < 0:
                continue
            anchor = f'<a class="geo" data-i="{p["i"]}">{p["name"]}</a>'
            text = text[:pos] + anchor + text[pos + len(p["name"]):]
            geo_done.add(p["i"])
        return text

    if not lines or not lines[0].startswith("# "):
        err(f"{rel}: 先頭が『# 章題』ではない")
        return ("?", "")
    title = lines[0][2:].strip()

    # 冒頭ブロックの検査: 著者行とプロフィール行
    if len(lines) < 5 or not lines[2].startswith("**著者: "):
        err(f"{rel}: 3行目が著者行(**著者: …**)ではない")
        return (title, "")
    author_line = lines[2].strip().strip("*")
    profile_line = lines[3].strip()
    if "PLACEHOLDER" in profile_line:
        err(f"{rel}: プロフィールが差し込まれていない(PLACEHOLDER が残存)")
    if author_file is not None:
        canonical = (ROOT / author_file).read_text(encoding="utf-8").split("\n")
        if len(canonical) >= 3 and canonical[2].strip() != profile_line:
            err(f"{rel}: 章冒頭のプロフィールが正本({author_file})と一致しない")

    out: list[str] = []
    out.append(f"<h1>{html.escape(title)}</h1>")
    out.append(f'<p class="author">{html.escape(author_line)}</p>')
    out.append(f'<p class="profile">{html.escape(profile_line)}</p>')

    note_numbers: list[int] = []
    sec_numbers: list[int] = []
    i = 4
    n = len(lines)
    body_md: list[str] = []  # markdown にそのまま渡す行(生HTMLブロック混在)

    def flush_raw(html_block: str) -> None:
        body_md.append("")
        body_md.append(html_block)
        body_md.append("")

    while i < n:
        line = lines[i]

        # 目次ブロック → 節へのリンク付きリスト
        if line.strip() == "目次":
            items = []
            i += 1
            while i < n and TOC_ITEM_RE.match(lines[i]):
                m = TOC_ITEM_RE.match(lines[i])
                items.append(
                    f'<li><a href="#sec-{m.group(1)}">{m.group(1)}. '
                    f"{html.escape(m.group(2))}</a></li>"
                )
                i += 1
            flush_raw('<nav class="toc"><p>目次</p><ol class="toc-list">'
                      + "".join(items) + "</ol></nav>")
            continue

        # 節見出し
        m = SEC_RE.match(line)
        if m:
            sec_numbers.append(int(m.group(1)))
            cur_sec = m.group(1)
            flush_raw(f'<h2 id="sec-{m.group(1)}">{m.group(1)}. '
                      f"{html.escape(m.group(2))}</h2>")
            i += 1
            continue
        if line.startswith("## "):
            err(f"{rel}:{i+1}: 節見出しが『## N. 題』の書式ではない: {line!r}")

        # 注の見出し
        if line.strip() == "### 注":
            flush_raw('<h3 class="notes-head">注</h3>')
            i += 1
            continue

        # 図の行 + 直後の説明段落
        m = FIG_RE.match(line)
        if m:
            fig_no, fig_title, img_rel = m.group(1), m.group(2), m.group(3)
            caption_lines = []
            i += 1
            while i < n and lines[i].strip():
                caption_lines.append(lines[i].strip())
                i += 1
            caption = " ".join(caption_lines)
            img_path = path.parent / img_rel
            inner = ""
            if img_path.is_file():
                inner = (f'<img src="{html.escape(img_rel)}" '
                         f'alt="{html.escape(fig_title)}">')
            else:
                warn(f"{rel}: 図{fig_no} の画像が未収録({img_rel})")
                inner = '<p class="fig-missing">(画像は準備中)</p>'
            cap_title = linkify(html.escape(fig_title), sec=cur_sec)
            cap_body = linkify(html.escape(caption), sec=cur_sec)
            flush_raw(
                f'<figure id="fig-{fig_no}">{inner}'
                f'<figcaption><span class="fig-no">図{fig_no}:</span> '
                f"{cap_title}<br>{cap_body}"
                f"</figcaption></figure>"
            )
            continue

        # 注の段落(1行=1注)
        m = NOTE_RE.match(line)
        if m:
            note_numbers.append(int(m.group(1)))
            note_html = linkify(html.escape(line.strip()), note=m.group(1))
            flush_raw(f'<p class="note" id="note-{m.group(1)}">'
                      f"{note_html}</p>")
            i += 1
            continue

        # 本文の段落: 指定の節の初出の地名をリンク化(表とHTMLブロックは除外)
        if (geo_places and cur_sec and line.strip()
                and not line.startswith(("|", "#", "<"))):
            line = linkify(line, sec=cur_sec)
        body_md.append(line)
        i += 1

    # lint: 節番号と注番号の連番検査
    if sec_numbers != list(range(1, len(sec_numbers) + 1)):
        err(f"{rel}: 節番号が1からの連番ではない: {sec_numbers}")
    if note_numbers != list(range(1, len(note_numbers) + 1)):
        err(f"{rel}: 注番号が1からの連番ではない: {note_numbers}")

    MD.reset()
    out.append(MD.convert("\n".join(body_md)))

    # ウェブ版限定のおまけ地図(章末)。正本には存在しない。
    if geo:
        for p in geo_places:
            if p["i"] not in geo_done:
                warn(f"{rel}: 地名『{p['name']}』をリンク化できなかった"
                     f"(指定: {p.get('sec') and p['sec'] + '節' or '注' + p['note']})")
        out.append(
            '<hr class="sep">'
            '<section class="map-appendix">'
            '<h2 class="map-appendix-head">おまけ: 地図で歩き直す</h2>'
            '<p class="map-appendix-note">ここから先は本文のおまけである。'
            'ピンを押すと写真が開き、写真をもう一度タップすると大きく表示される。'
            '📷のピンは「暮らしのスナップ」——'
            '本文の筋とは関係なく、観光地でもない、'
            f'この{"州" if rel.parts[1] == "usa" else "土地"}のふだんの生活の一場面を'
            '場面の良さだけで選んだ。'
            '(このおまけと本文中の📍リンクはウェブ版だけの機能である)</p>'
            f'<iframe class="map-appendix-frame" src="../{geo["map"]}?rich" '
            f'width="100%" height="520" loading="lazy" '
            f'title="{html.escape(geo.get("title", "章の地名地図"))}"></iframe>'
            '</section>'
        )
    return (title, "\n".join(out))


# ---------------------------------------------------------------- 章別地図

MAP_TEMPLATE = ROOT / "site" / "maps" / "template.html"
WIKIMEDIA_IMG = "https://upload.wikimedia.org/"


def check_geo(series: str, slug: str, geo: dict) -> None:
    """geo/<シリーズ>/<slug>.json の書式検査(ビルドはlintを兼ねる)。"""
    src = f"site/geo/{series}/{slug}.json"
    for key in ("map", "title", "places"):
        if key not in geo:
            err(f"{src}: 必須キー『{key}』がない")
            return
    if geo["map"] != f"maps/{series}-{slug}.html":
        err(f"{src}: mapは『maps/{series}-{slug}.html』でなければならない")
    for p in geo["places"]:
        where = f"{src}: places『{p.get('name', '?')}』"
        for key in ("i", "name", "lat", "lng", "text", "rich", "img", "credit"):
            if key not in p:
                err(f"{where}: キー『{key}』がない")
        if bool(p.get("sec")) == bool(p.get("note")):
            err(f"{where}: sec(節番号)とnote(注番号)はどちらか一方を指定する")
        if "img" in p and not p["img"].startswith(WIKIMEDIA_IMG):
            err(f"{where}: imgがWikimediaのURLではない")
    for s in geo.get("snaps", []):
        where = f"{src}: snaps『{s.get('name', '?')}』"
        for key in ("name", "lat", "lng", "era", "text", "img", "credit"):
            if key not in s:
                err(f"{where}: キー『{key}』がない")
        if "img" in s and not s["img"].startswith(WIKIMEDIA_IMG):
            err(f"{where}: imgがWikimediaのURLではない")


def render_map(geo: dict, template: str) -> str:
    data = {"places": geo["places"], "snaps": geo.get("snaps", [])}
    return (template
            .replace("__TITLE__", html.escape(geo["title"]))
            .replace("__DATA__", json.dumps(data, ensure_ascii=False)))


# ---------------------------------------------------------------- 一覧の解釈

CHAPTER_ROW_RE = re.compile(
    r"^\|\s*(.+?)\s*\|\s*(text/[^|]+?\.md)\s*\|\s*(.+?)[\uff08(](authors/[^|]+?\.md)[\uff09)]")


def parse_assignments() -> list[dict]:
    """authors/index.md の割り振り表から章の一覧を得る。"""
    chapters = []
    for line in (ROOT / "authors" / "index.md").read_text(encoding="utf-8").split("\n"):
        m = CHAPTER_ROW_RE.match(line)
        if m:
            chapters.append({
                "title": m.group(1),
                "file": Path(m.group(2)),
                "author": m.group(3).strip(),
                "author_file": Path(m.group(4)),
            })
    if not chapters:
        err("authors/index.md から章の割り振りを読み取れない")
    return chapters


# ---------------------------------------------------------------- ビルド本体

def main() -> int:
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True)

    chapters = parse_assignments()
    cards: dict[str, list[str]] = {key: [] for key in SERIES}
    for ch in chapters:
        src = ROOT / ch["file"]
        if not src.is_file():
            err(f"{ch['file']}: 割り振り表にあるが実体がない")
            continue
        series = ch["file"].parts[1]  # text/<シリーズ>/<slug>.md
        if series not in SERIES:
            err(f"{ch['file']}: 未知のシリーズ『{series}』(build.py の SERIES に無い)")
            continue
        slug = src.stem  # tx, nv, ... / hachijo, izu, ...
        geo = None
        geo_path = ROOT / "site" / "geo" / series / f"{slug}.json"
        if geo_path.is_file():
            geo = json.loads(geo_path.read_text(encoding="utf-8"))
            check_geo(series, slug, geo)
            map_out = OUT / geo["map"]
            map_out.parent.mkdir(parents=True, exist_ok=True)
            map_out.write_text(
                render_map(geo, MAP_TEMPLATE.read_text(encoding="utf-8")),
                encoding="utf-8")
        title, body = transform_chapter(src, ch["author_file"], geo)
        extra = ""
        if geo:
            extra = (f'<script src="../assets/map-panel.js" '
                     f'data-map="../{geo["map"]}"></script>\n')
        page = render_page(f"{title} — geostudy", body, home="../index.html",
                           extra=extra)
        (OUT / series).mkdir(exist_ok=True)
        (OUT / series / f"{slug}.html").write_text(page, encoding="utf-8")
        cards[series].append(
            f'<li><a href="{series}/{slug}.html">{html.escape(title)}</a>'
            f'<span class="byline">{html.escape(ch["author"])}</span></li>'
        )

    # 画像(あれば)をシリーズごとにそのまま持っていく
    for series in SERIES:
        img_dir = ROOT / "text" / series / "img"
        if img_dir.is_dir():
            (OUT / series).mkdir(exist_ok=True)
            shutil.copytree(img_dir, OUT / series / "img")

    # 地図機能の静的資産(あれば)を持っていく(章別地図はgeo/*.jsonから生成済み)
    assets_dir = ROOT / "site" / "assets"
    if assets_dir.is_dir():
        shutil.copytree(assets_dir, OUT / "assets")

    # トップページ: シリーズごとの章の一覧 + README全文
    MD.reset()
    readme_html = MD.convert((ROOT / "README.md").read_text(encoding="utf-8"))
    series_lists = []
    for series, label in SERIES.items():
        if not cards[series]:
            continue
        series_lists.append(
            f'<h2 class="series-head">{html.escape(label)}</h2>'
            '<ul class="chapter-list">' + "".join(cards[series]) + "</ul>"
        )
    index_body = (
        '<h1 class="site-title">geostudy</h1>'
        '<p class="site-sub">読書会のための教養の読み物</p>'
        + "".join(series_lists) +
        '<hr class="sep">'
        '<section class="about">' + readme_html + "</section>"
    )
    (OUT / "index.html").write_text(
        render_page("geostudy", index_body, home="index.html"), encoding="utf-8")

    for w in warnings:
        print(f"warning: {w}")
    if errors:
        for e in errors:
            print(f"error: {e}", file=sys.stderr)
        return 1
    n_chapters = sum(len(c) for c in cards.values())
    print(f"built {n_chapters} chapters -> {OUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
