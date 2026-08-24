#!/usr/bin/env python3
"""text/ のMarkdown正本から静的サイト(_site/)を生成する。

原則: 正本(text/, authors/, README.md)には一切手を入れない。
書式の解釈と変換はすべてこのスクリプトが吸収する。
章の書式が壊れている場合はビルドを失敗させる(lint を兼ねる)。
変換規則と除外の方針は site/README.md を参照。
"""

import html
import re
import shutil
import sys
from pathlib import Path

import markdown

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "_site"
SERIES_DIR = ROOT / "text" / "usa"

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
</body>
</html>
"""


def render_page(title: str, body: str, home: str) -> str:
    return PAGE.format(title=html.escape(title), css=CSS, body=body, home=home)


# ---------------------------------------------------------------- 章の変換

FIG_RE = re.compile(r"^\u56f3(\d+): (.+?)[\uff08(](.+?)[\uff09)]\s*$")
SEC_RE = re.compile(r"^## (\d+)\. (.+?)\s*$")
NOTE_RE = re.compile(r"^注(\d+): ")
TOC_ITEM_RE = re.compile(r"^(\d+)\. (.+?)\s*$")


def transform_chapter(path: Path, author_file: Path | None) -> tuple[str, str]:
    """章のMarkdownを、書式検査をかけながらHTML断片に変換する。

    戻り値: (章題, 本文HTML)
    """
    rel = path.relative_to(ROOT)
    lines = path.read_text(encoding="utf-8").split("\n")

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
            flush_raw(
                f'<figure id="fig-{fig_no}">{inner}'
                f'<figcaption><span class="fig-no">図{fig_no}:</span> '
                f"{html.escape(fig_title)}<br>{html.escape(caption)}"
                f"</figcaption></figure>"
            )
            continue

        # 注の段落(1行=1注)
        m = NOTE_RE.match(line)
        if m:
            note_numbers.append(int(m.group(1)))
            flush_raw(f'<p class="note" id="note-{m.group(1)}">'
                      f"{html.escape(line.strip())}</p>")
            i += 1
            continue

        body_md.append(line)
        i += 1

    # lint: 節番号と注番号の連番検査
    if sec_numbers != list(range(1, len(sec_numbers) + 1)):
        err(f"{rel}: 節番号が1からの連番ではない: {sec_numbers}")
    if note_numbers != list(range(1, len(note_numbers) + 1)):
        err(f"{rel}: 注番号が1からの連番ではない: {note_numbers}")

    MD.reset()
    out.append(MD.convert("\n".join(body_md)))
    return (title, "\n".join(out))


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
    (OUT / "usa").mkdir(parents=True)

    chapters = parse_assignments()
    cards = []
    for ch in chapters:
        src = ROOT / ch["file"]
        if not src.is_file():
            err(f"{ch['file']}: 割り振り表にあるが実体がない")
            continue
        title, body = transform_chapter(src, ch["author_file"])
        slug = src.stem  # tx, nv, ...
        page = render_page(f"{title} — geostudy", body, home="../index.html")
        (OUT / "usa" / f"{slug}.html").write_text(page, encoding="utf-8")
        cards.append(
            f'<li><a href="usa/{slug}.html">{html.escape(title)}</a>'
            f'<span class="byline">{html.escape(ch["author"])}</span></li>'
        )

    # 画像(あれば)をそのまま持っていく
    img_dir = SERIES_DIR / "img"
    if img_dir.is_dir():
        shutil.copytree(img_dir, OUT / "usa" / "img")

    # トップページ: 章の一覧 + README全文
    MD.reset()
    readme_html = MD.convert((ROOT / "README.md").read_text(encoding="utf-8"))
    index_body = (
        '<h1 class="site-title">geostudy</h1>'
        '<p class="site-sub">読書会のための教養の読み物 — 第1シリーズ: アメリカ50州</p>'
        '<ul class="chapter-list">' + "".join(cards) + "</ul>"
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
    print(f"built {len(cards)} chapters -> {OUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
