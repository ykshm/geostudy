# フロリダ章の地図 検証記録(fl-check)

地図データは fl.json。手順は site/MAPS.md。2026-08-26 作成。

## 地名の選定

本文の筋の11地名(1節マイアミビーチ/2節セントオーガスティン・マイアミ・キーウェスト・エバーグレーズ/3節オーランド/4節セブリング/5節リトル・ハバナ/6節ココアビーチ・ケープカナベラル/7節ザ・ビレッジズ)。

- オーシャン・ドライブとブリッケルはマイアミビーチ/マイアミのピンが代表。タンパは通りすがりの言及のみで置かない。ハバナは本文に出るが「リトル・ハバナ」の部分文字列でありリンク化が衝突するため置かない(build.pyのリンク化は単純な文字列一致)。
- セブリングは本文でなく図3の説明文の初出(4節)——MAPS.md 3節2項の「図の説明文にだけ出る地名」の扱い。
- ケネディ宇宙センターはケープカナベラルのピンが代表。座標は空軍基地側(28.4889, -80.5778)。
- ザ・ビレッジズの座標は写真に合わせスパニッシュ・スプリングス広場。

## places の写真(11枚、ライセンスはCommons APIのextmetadataで確認)

| 地名 | Commonsファイル | 作者 / ライセンス |
|---|---|---|
| マイアミビーチ | Ocean Drive in the Miami Beach Art Deco Historic District.jpg(章の図2と同一) | Robbschultz69, CC BY-SA 4.0 |
| セントオーガスティン | Flagler College, St. Augustine, Florida LCCN2011631976.tif | Carol M. Highsmith(米議会図書館), PD |
| マイアミ | Miami - City Skyline from Biscayne Bay 3.jpg | P. Hughes, CC BY 4.0 |
| キーウェスト | Southernmost point buoy, NE view.jpg | Radomianin, CC BY-SA 4.0 |
| エバーグレーズ | Everglades NP Pa-Hay-Okee Trail view02.jpg | Ebyabe, CC BY-SA 4.0 |
| オーランド | Cinderella Castle, Magic Kingdom Walt Disney World (2024).jpg | Jedi94, CC BY-SA 4.0 |
| セブリング | Florida orange grove.JPG(章の図3と同一) | Mmacbeth, CC0 |
| リトル・ハバナ | Calle Ocho, Little Havana, Miami, Florida 2021 - Gallo de Calle Ocho.jpg | Sharon Hahn Darlin, CC BY 2.0 |
| ココアビーチ | Cocoa Beach Pier at Sunset.jpg | Cathylaurenzi, CC BY-SA 4.0 |
| ケープカナベラル | 45th Space Wing Supports Successful Falcon 9 SAOCOM 1B Launch 02.jpg(章の図4と同一) | 米宇宙軍(Joshua Conti), PD |
| ザ・ビレッジズ | Abendkulisse in Spanish Springs, The Villages, Florida.jpg | Tetraeder, CC BY-SA 4.0 |

- 最初に候補にしたキーウェストの標柱写真(Florida Memory, PD)は原画像600pxで幅1280px要件を満たさず、Radomianinの4000px版に差し替えた。
- セントオーガスティンは.tifのため、サムネイルはAPIのthumburl通り lossy-page1-500px-〜.tif.jpg の形。
- 全16枚(places 11+snaps 5)の500px URLがHTTP 200を返すことを確認(429のレート制限に当たった2枚は間隔を置いて200を確認)。

## snaps の写真(5枚、写真ファーストで目視選定+ライセンス確認)

| 場所 | Commonsファイル | 作者 / ライセンス | 年代 |
|---|---|---|---|
| ドミノ公園の午後 | April 7, 2015 - Little Havana, Miami, Florida - Domino Club.jpg | osseous, CC BY 2.0 | いま |
| キューバサンドの昼 | Versailles, Calle Ocho, Miami - Cuban Sandwich.jpg | Todd Van Hoosear, CC BY-SA 2.0 | いま |
| カートで買い物 | Golfcars in Sunter Landings, The Villages, Florida.jpg | Tetraeder, CC BY-SA 4.0 | いま |
| 月を待つ砂浜 | CAPE CANAVERAL, Fla (KSC-69P-0619).jpg | NASA(ケネディ宇宙センター), PD | 1969年 |
| 南のビーチのベンチ | PARK BENCHES OF THE SOUTH BEACH AREA OF MIAMI BEACH ... - NARA - 548647.jpg | Flip Schulke/EPA(DOCUMERICA), PD | 1973年 |

- 昔の2枚: アポロ11号の見物客(1969年7月16日、NASA公式のキャプションで「浜で夜明かしした群衆、推定100万人」を確認)と、DOCUMERICAのサウスビーチの隠居たち(Flip Schulke、1973年6月)。7節「老後という商品」と6節「3、2、1」の本文にそのまま対応する場面である。
- ドミノクラブの写真は人物が小さく写る引きの構図で、顔の大写しはない。ベンチの3人の写真(同シリーズ NARA 548620等)は顔が大きく写るため見送り、こちらを採用。
- キューバサンドはルイジアナ章のベニエと同型の「一皿」スナップ。座標は写真の店(カジェ・オチョ3555番地)に置いた。
- 没: ベンタニータ(小窓のコーヒー)の良い写真がCommonsに見つからず、キューバサンドで代替。ザ・ビレッジズのカート専用橋(Ebyabe)はカートが写っておらず、駐車列の写真を採用。

## ブラウザ検証(2026-08-26)

`python3 site/build.py` 警告なし(8章)。`_site/` をHTTPサーバ(localhost:8123)で開き、Playwright+Chromiumで確認:

- 章ページの📍リンク11個が生成され、タップで地図パネルが開いて該当ピンの吹き出しが出る。
- チップは「全体+11地名」(?richでは+📷5枚)。チップ移動で吹き出しと節番号表示が切り替わる。
- ?rich で写真・クレジット・📷スナップピン・年代表示・写真タップの全画面拡大が動く。
- モバイル幅(390px)でもパネルと吹き出しが動く。
- 他章(ルイジアナ)のリンク数は従来通りで影響なし。JSコンソールエラーなし。
- 備考: 検証環境の都合で、CDN(Leaflet・地図タイル)とCommonsへのブラウザ直接続はプロキシで遮断されるため、Playwrightのルート機能で同内容を中継して確認した。ページ側のHTML/JSは無改変。
