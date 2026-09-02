# カリフォルニア章の地図 検証記録(ca-check)

地図データは ca.json。作業手順は site/MAPS.md。紙面の編集用注記(text/usa/ca-check.md)とは別物で、こちらは地図(ウェブ版限定)の楽屋である。

## 経緯

- 2026-09-02 初版。章のマージ直後に、依頼者の指示で後工程として作成。places 12(本文の筋の地名、登場順)+ snaps 5(現代3・1972年1・1936年1)。extras は置いていない(アメリカ50州では任意)。

## places の写真(12枚、ライセンスはCommons APIのextmetadataで確認、2026-09-02)

| 地名 | Commonsファイル | 作者 / ライセンス |
|---|---|---|
| セントラルバレー | Tule Fog California - 2005.jpg | NASA(Jeff Schmaltz), パブリックドメイン |
| サンフランシスコ | San Francisco with approaching fog.jpg | Brocken Inaglory, CC BY-SA 3.0 |
| エンジェル島 | Angel Island detention barracks.JPG | Hispalois, CC BY-SA 4.0 |
| マンザナー | Manzanar school children 00153u.jpg | Ansel Adams(米議会図書館), パブリックドメイン |
| ロサンゼルス | Downtown Los Angeles and 110 freeway.jpg | Camiloarenivar, CC BY-SA 4.0 |
| レイクウッド | Neighborhood in Lakewood California.jpg | Puddles eyes, CC BY-SA 4.0 |
| ワッツ地区 | Watts towers from below.jpg | Isabelle Acatauassú Alves Almeida, CC BY 2.0 |
| パロアルト | HP garage front.JPG | BrokenSphere, CC BY-SA 3.0 |
| マウンテンビュー | Google Campus, Mountain View, CA.jpg | Austin McKinley, CC BY 3.0 |
| デラノ | Roy L. Reuther Hall at Forty Acres (39b9b2b0-…).jpg | NPS Photo, パブリックドメイン |
| パシフィック・パリセーズ | 2025 Palisades Fire Seen From Palisades Drive.jpg | Ariam23, CC BY 4.0 |
| アルタデナ | Destroyed home and vehicle caused by the Eaton Fire, 2025.jpg | カリフォルニア州の公開記録写真, パブリックドメイン(章の図6と同一) |

- ワッツ地区の当初候補(Highsmithwattstowers.jpg)は原画像幅827pxで拡大要件(1280px以上)を満たさず不採用、CC BY 2.0の別カットに差し替えた。

## snaps の写真(5枚、同日に目視選定+ライセンス確認)

| 場所 | Commonsファイル | 作者 / ライセンス | 年代 |
|---|---|---|---|
| ウェストウッドの交差点 | Food truck Tacos Super Gallito (Westwood Bld X Santa Monica Bld).jpg | Alexis Doine, CC0 | いま |
| ダウンタウンの陸橋 | Homeless encampment in Downtown Los Angeles over the freeway DSF8315.jpg | Levi Clancy, CC0 | いま |
| ナパの朝市 | Napa Farmers Market - April 2023 - Sarah Stierch.jpg | Missvain, CC BY 4.0 | いま |
| ロサンゼルスの高速道路 | LOW-HANGING SMOG - NARA - 542682.jpg | Gene Daniels(EPA・DOCUMERICA), パブリックドメイン | 1972年 |
| ブライスの路肩 | Dorothea Lange, Drought refugees from Oklahoma camping by the roadside, Blythe, California, 1936.jpg | Dorothea Lange(FSA), パブリックドメイン | 1936年 |

- 1972年の煙霧の写真はNARAの記録に撮影地の詳細がなく(「1972年、ロサンゼルス郡」)、ピンはダウンタウン近くの高速道路上に概置した。ブライスの一家は本文6節の「オーキー」と州境検問の筋に対応する(章の図5「移民の母」と同じラング・同年の撮影だが、場面は別)。
- スナップ選定の没: LAファーマーズ・マーケットの看板(Highsmith。場面でなく看板)、ヴェニスビーチの炊き出し(陸橋のテント列と主題が重複)、イン・アンド・アウトのメニュー看板(場面が弱い)。

## 検証(2026-09-02)

1. `python3 site/build.py` 警告・エラーなし(21章。JSONの書式検査を兼ねる)。
2. 全17枚の500pxサムネイルURLがHTTP 200を返すことを確認(取得はUser-Agent「geostudy-image-collection/1.0 (+https://github.com/ykshm/geostudy)」)。原画像はいずれも幅1280px以上。
3. ブラウザ検証: リモート実行環境のため、ブラウザだけがunpkg(Leaflet)にTLSで届かない事象を確認(MAPS.md 6節の想定どおり)。curlでunpkg・OSMタイル・Commons画像の到達性(200)を別途確認した上で、_site内のLeafletをローカル退避コピーに差し替え、外部リクエストを遮断してPlaywright(Chromium)で検証した。リポジトリ側のテンプレートは無改変(差し替えは検証用の_siteのみ。_siteは再ビルドで復元済み)。
   - [x] 地図パネルが開閉し、本文の📍地名タップで該当地点に飛んで吹き出しが開く(アルタデナ=7節を確認)
   - [x] チップ(全体+12)で全地名を順に回れる。ピン・吹き出しの節番号表示が12地点すべて正しい
   - [x] `?rich`(章末おまけ)で写真・クレジット・📷スナップチップ5件が出る。写真タップで全画面拡大(ライトボックス)が開く
   - [x] モバイル幅(390px)でも📍リンクからパネルが開き吹き出しが出る
   - [x] 他の章のページに影響がない(ミシシッピ章で📍リンク12件と地図動作、JSエラーなしを確認)
   - ページのJSエラーなし(カリフォルニア章・デスクトップ/モバイルとも)
