# アイオワ章の地図 検証記録(ia-check)

地図データは ia.json。作業手順は site/MAPS.md。紙面の編集用注記(text/usa/ia-check.md)とは別物で、こちらは地図(ウェブ版限定)の楽屋である。

## 経緯

- 2026-08-26 初版。章のマージ(PR #26)直後、同じセッションで後工程として作成。places 9地点+snaps 5枚。
- 地名の選定: 本文の筋を運ぶ地名だけを登場順に。デモイン・ローブとポットホール(地帯の名で点にならない)、シカゴ(州外の文脈)、ジョーンズ郡・マハスカ郡(図の撮影地としてのみ登場)は見送り。メキシコ湾のデッドゾーンは、ピンを置くと地図の枠が州から大きく外れるため見送り。
- 座標の特記: レスヒルズは南北に長い丘陵のため中部(プレパレーション・キャニオン州立公園付近)に置いた。タマ郡はメスクワキ・セトルメントの位置。デモインの党員集会のスナップは撮影地(投票区61、グリーンウッド小学校)の近似座標。マーシャルタウンは市街中心の近似。
- クレスコの注番号: 執筆後の注繰り下げで人脈の注は注11(初稿の注10のままJSONを書いてビルド警告→修正。ビルドの警告検査が効いた)。

## places の写真(9枚、ライセンスはCommons APIのextmetadataで確認、2026-08-26)

| 地名 | Commonsファイル | 作者 / ライセンス |
|---|---|---|
| レスヒルズ | Loess Hills I-80 Iowa 632.jpg | Chris Light, CC BY-SA 4.0 |
| タマ郡 | Tama, IA - August 9, 2014 - Members of the Meskwaki Nation dance at the Tribe 100th Annual Pow Wow ... - DPLA - 417c894520173d5dd61af322188a3c45.jpg | Steve Zumwalt/FEMA, PD |
| デモイン | Skyline downtown Des Moines.jpg | BarbaraLN, CC BY-SA 2.0 |
| クレスコ | Cresco, Iowa.jpg | Wikideas1, CC0 |
| デニソン | Dension iowa.jpg | Billwhittaker, CC BY-SA 3.0 |
| ストームレイク | Victory Arch at Buena Vista University in Storm Lake.jpg | City of Storm Lake, CC BY-SA 4.0 |
| ポストビル | Postville, Iowa business district.JPG | TheCatalyst31, CC0 |
| ウェストバーリントン | Ethanol plant.jpg | 米農務省農業研究局(PD-USGov-USDA-ARS) |
| ニール・スミス国立野生生物保護区 | Bison on Neal Smith Refuge (5471657484).jpg | USFWS, PD |

- タマ郡のパウワウ写真はファイル名が長く、サムネイルURLが `…/500px-thumbnail.jpg` の短縮形になる(APIのthumburlをそのまま採用)。1280px版(`…/1280px-thumbnail.jpg`)もHTTP 200を確認。
- ウェストバーリントンは紙面の図5と同じ工場(Big River Resources)の別カット(非クロップ版)。

## snaps の写真(5枚、目視選定+ライセンス確認、2026-08-26)

| 場所 | Commonsファイル | 作者 / ライセンス | 年代 |
|---|---|---|---|
| デモインの党員集会 | Precinct 61 (24405397629).jpg | Phil Roeder, CC BY 2.0 | 2016年 |
| ステートフェア | Iowa State Fair (6048880109).jpg | Phil Roeder, CC BY 2.0 | いま |
| ハイアワサ | RAGBRAI in Hiawatha 2015.jpg | Crcjfly, CC BY-SA 3.0 | いま |
| ファーナルド | Fernald Iowa.jpg | Carl Wycoff, CC BY 2.0 | いま |
| マーシャルタウン | Auctioning off the prize baby beeves, Central Iowa 4-H Club fair, Marshalltown, Iowa.tif | Arthur Rothstein/FSA, PD | 1939年 |

- 全14枚の500pxサムネイルURLがHTTP 200を返すことを確認(2026-08-26)。原画像はいずれも幅1280px以上。マーシャルタウンは.tif由来のため `lossy-page1-500px-…` 形式(1280px版も200を確認)。
- スナップ選定の没: Hull の穀物エレベーター(原画像幅1148pxで拡大要件を満たさない→ファーナルドに差し替え)、ストームレイクの大文字絵はがき1949(幅1000pxで同上)、Precinct 61 の別カット(人物の顔が大きい)、ニューウルムのデタッセリング(DOCUMERICAの好画だがミネソタ州)、農場差し押さえ競売のNARA写真(撮影地が特定できずピンを置けない)。
- マーシャルタウンの4-H競売は米議会図書館FSAコレクションの1939年撮影(ロスシュタインのアイオワ取材)。年代は `era` に明記。

## ブラウザ検証(2026-08-26、_site をHTTPサーバで配信、ヘッドレスChromiumで確認)

- 地図パネルの開閉、本文の📍地名タップで該当地点へ飛び吹き出しが開く(デスクトップ1280px幅・モバイル390px幅の両方で確認)。
- チップ10個(全体+9地名)で全地名を巡回できる。ピンのバッジ(節番号/注)の表示が正しいことをスクリーンショットで確認。
- `?rich` で写真・クレジット・📷スナップピン5本が出る。写真タップで全画面拡大(ライトボックス)が動く。
- 他章への影響なし(tx: 10ピン描画、hi ほか各章のビルド出力に警告なし)。
- python site/build.py 警告・エラーなし(9章)。
- 検証環境の注記: この実行環境はブラウザの直接外部通信が egress プロキシに遮られるため、検証時は Playwright のルート機能で外部HTTPS資源をプロキシ経由(TLS検証あり)で取得して差し込んだ。URLの実在・ライセンスはAPIとHTTP 200確認で担保。本番(GitHub Pages)は読者のブラウザが直接取得する。
