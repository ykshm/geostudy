# 多摩章 地図データ 検証記録(tama-check)

対象: site/geo/japan/tama.json → _site/maps/japan-tama.html。作業日 2026-09-01。

## 採用した写真(Commonsファイル名 / 作者 / ライセンス / 確認日)

すべてWikimedia Commons。ライセンスと作者はAPIのextmetadata(LicenseShortName / Artist)で2026-09-01に確認。imgはAPIのthumburl(500px)を正規化(ホストをupload.wikimedia.orgに、クエリ除去)して使用。全21URLと、幅1280pxちょうどの原画像を含む1280px版のHTTP 200をcurlで確認済み。

### places
- 立川駅: 2015 Tachikawa North (18281269556).jpg / Hector Martin / CC BY-SA 2.0
- 青梅市: JR Ome-Line Ome Station Platform.jpg / Mister0124 / CC BY-SA 4.0
- 日の出町: AEON Mall Hinode 3.jpg / 103momo / CC BY-SA 3.0
- 檜原村: 東京都檜原村数馬.JPG / 誾千代 / CC BY-SA 4.0(村の代表写真として数馬集落の景観を使用)
- 奥多摩町: Okutama-HikawaBridge-2016100202.jpg / Hasec / CC0
- 練馬区: A field in Hazawa Nerima.jpg / Koujigenba / CC BY-SA 3.0(紙面の図2と同じ写真の500px版)
- 雲取山: Summit of Mount Kumotori (11169733253).jpg / Guilhem Vellut / CC BY 2.0
- 日原: Nippara limestone cave entrance gate.jpg / さかおり / CC BY-SA 4.0
- 奥多摩駅: Okutama Station 2019.jpg / Kaze315 / CC BY-SA 4.0(紙面の図4と同じ写真の500px版)
- 御岳山: Musashi Mitake Shrine, Tokyo; August 2016 (02).jpg / 雷太 / CC BY 2.0
- 奥多摩湖: Lake Okutama @ Ogouchi Dam (11131615856).jpg / Guilhem Vellut / CC BY 2.0
- 成木: 成木川.jpg / Hanasakijijii / CC BY-SA 3.0(幅1280px。1280px版サムネイルの200を確認)

### snaps
- 立川駅北口のバスのりば: Tachikawa bus at the north exit of Tachikawa station.jpg / Sittaka / CC BY-SA 4.0
- イオンモール日の出のフードコート: Food Court IN Hinode Aeon Mall - panoramio.jpg / moonwalker76 / CC BY 3.0
- 青梅・住江町の商店街: 昭和レトロ商品博物館 2015 (22057046293).jpg / Stephen Kelly / CC BY 2.0(撮影2015年のためeraを「2015年」とした)
- 御岳山ケーブルカーの車内: Mount Mitake cable car (13438727493).jpg / Guilhem Vellut / CC BY 2.0
- 武蔵五日市駅のホーム: JR Itsukaichi-Line Musashi-Itsukaichi Station Platform.jpg / Mister0124 / CC BY-SA 4.0
- 数馬の分校の教室: 小学校内 ストーブ 2008 檜原村 (3013297253).jpg / Hajime NAKANO / CC BY 2.0(撮影2008年のためera「2008年」。実況文は写真に写るものだけを書き、学校の現況には触れていない)

### extras
- 塩船観音寺: Azalea Festival @ Shiofune Kannon-ji temple @ Ome (14051354564).jpg / Guilhem Vellut / CC BY 2.0
- 払沢の滝: Hossawa Falls @ Hinohara (14156434451).jpg / Guilhem Vellut / CC BY 2.0
- 羽村取水堰: TamagawaJosui HamuraWeir.JPG / sewmew / パブリックドメイン

### 見送った写真
- 小澤酒造(澤乃井)のOzawa shuzo1〜5.jpg: extmetadataにArtist・Creditが無く、CC BY-SA 4.0の表示要件を満たせないため不採用。extrasの酒蔵の項自体を見送り、塩船観音寺に差し替えた。
- 西東京バス氷川車庫: 写真は良いが車庫の正確な座標を確かめられず、ピンの信頼性を優先して見送り(武蔵五日市駅のホームに差し替え)。
- 檜原村役場・村内集落の写真数点: 原画像の幅が1280px未満のため不採用。

## 座標の根拠

- 駅(立川・青梅・奥多摩・武蔵五日市)と山・施設(雲取山・武蔵御嶽神社=御岳山・払沢の滝・塩船観音寺・日原鍾乳洞)はWikipedia日本語版の座標プロパティ。青梅駅の座標はこの照合で章の標高の誤りが見つかり、紙面側を訂正した(text/japan/tama-check.md参照)。
- 町村(日の出町・檜原村・奥多摩町・成木・日原・住江町・数馬)は地理院のアドレス検索APIの代表点。日原のピンは鍾乳洞入口の写真のジオタグ(35.8550,139.0427)に合わせ、標高API(谷底の標高約600m台)で妥当性を確認。
- イオンモール日の出はフードコート写真(panoramio)のジオタグ(35.7346,139.2751)。
- 奥多摩湖は小河内ダム地点(標高APIで湖面高約525mを確認済みの座標)。
- 羽村取水堰(35.7616,139.3069)と御岳山ケーブルカーの車内(索道の中間付近35.7878,139.1577)、数馬の分校(数馬集落付近35.7275,139.1080)は地理院地図の読図による近似で、±100m程度の誤差がありうる。
- placesのnameは本文の該当節の表記と一致することをビルド後のHTML(data-iアンカー12件の生成)で確認。「檜原村」は2節の初出が「檜原(ひのはら)村」とルビ括弧を挟むため、素の表記が出る3節にリンクを張った。

## 動作検証(2026-09-01)

- `python3 site/build.py` 警告・エラーなし(19章)。
- `_site/` を `python3 -m http.server` で配信し、Chromium(Playwright)で確認。**リモート実行環境のブラウザからは外部CDN(unpkgのLeaflet・地図タイル・Commonsの画像)にTLSで届かなかったため、site/MAPS.md 6節の但し書きに従い、(1) unpkg・タイル・写真URLの到達性はcurlで別途確認(全て200)、(2) ブラウザ検証は_site側の生成物のLeaflet参照をローカル退避コピーに差し替え、外部リクエストを遮断して実施した**。テンプレート(site/maps/template.html)と正本には手を入れていない。検証後にbuild.pyを再実行し、差し替えを含まない生成物に戻している。
- チェックリスト:
  - [x] 地図パネルが開閉する(「地図」→「✕ 地図を閉じる」のトグルをdocumentElementのgs-map-openクラスで確認)。本文の📍地名タップで該当地点に飛び、吹き出しが開く(立川駅で確認)
  - [x] チップで全地名を巡回できる(チップ13=全体+12地名)。ピンのバッジに節番号(1,2,3,4,5,7)が正しく出る
  - [x] `?rich` でピン21本(places12+📷6+✦3)、実況文・クレジット付きの吹き出し、写真タップで全画面拡大(gs-lightboxがopenになり、キャプションに作者とライセンスを表示。1280px版への差し替えは遮断下ではonerrorで500pxに戻るため、1280px版URLの200はcurlで確認)
  - [x] モバイル幅(390px)でも📍タップ→吹き出しが動く(奥多摩町で確認)
  - [x] 他の章に影響なし(津軽・テキサスの章ページの地名リンク数が従来通り生成される)

## 文の点検

- places/snaps/extrasの文はすべて裏方の声。著者(牧野周)の言い回し(「白状」「帳簿」等)は使っていない。
- extrasは著者が紙面で推した見どころ(御岳山の宿坊)と重複しない。実用情報(営業時間・料金・行き方)は書いていない。
- 事実の言明の根拠: 塩船観音寺のつつじ(寺・青梅市観光協会の紹介)、払沢の滝の四段と結氷(檜原村観光協会)、羽村取水堰1653年(羽村市・東京都水道局の玉川上水の解説)、成木川が荒川水系(入間川支流)であること(国土交通省の水系情報)——いずれも2026-09-01に検索で確認。
