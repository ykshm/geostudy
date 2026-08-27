# ペンシルベニア章の地図 検証記録(pa-check)

地図データは pa.json。作業手順は site/MAPS.md。紙面の編集用注記(text/usa/pa-check.md)とは別物で、こちらは地図(ウェブ版限定)の楽屋である。

## 経緯

- 2026-08-27 初版。places 12(章の本文順)+ snaps 6。テンプレート・既存章は無改変。

## places の写真(12枚、ライセンスはCommons APIのextmetadataで確認、2026-08-27)

| 地名 | Commonsファイル | 作者 / ライセンス |
|---|---|---|
| フィラデルフィア | Philadelphia skyline 20240528.jpg | 颐园居, CC BY-SA 4.0 |
| ハリスバーグ | State Street from State Capitol Steps, Harrisburg, PA.jpg | w_lemay, CC BY-SA 2.0 |
| スクラントン | Electric City Mural.JPG | Christopher Seliga, CC BY-SA 3.0 |
| セントラリア | Centralia wafting.png | Mredden, CC BY-SA 3.0 |
| タイタスビル | Drake Well, June 2012.jpg | Niagara, CC BY-SA 3.0 |
| ピッツバーグ | Point from Mount Washington, 2015-10-26, 01.jpg | Cbaile19, CC0(章の図7と同じ) |
| ホームステッド | HomesteadSteelWorksSmokestacksEarlyMorningFromEast.jpg | DanielPenfield, CC BY-SA 4.0 |
| アルトゥーナ | Horseshoe Curve, Altoona Pennsylvania - Trains visible along the tracks.jpg | Rputnick, CC BY-SA 4.0 |
| ジョンズタウン | Johnstown Inclined Plane side view.jpg | Niagara, CC BY-SA 3.0 |
| スリーマイル島 | Three Mile Island Nuclear Generating Station.jpg | Z22, CC BY-SA 3.0(章の図6と同じ) |
| ブラドック | Edgar Thomson Steel Works, Braddock Avenue, and Turtle Creek.jpg | Myrichiehaynes, CC BY-SA 4.0 |
| ホーマーシティ | Homer City Generating Station.jpg | Jaro Nemčok, CC BY-SA 3.0(解体前の撮影である旨をrichに明記) |

- セントラリアのみ節でなく注8にリンク(本文の初出が注のため)。ホームステッドのリンクは本文の「ホームステッド製鋼所」の文字列に載る。
- ジョンズタウンのケーブルカー(インクラインド・プレーン)は1889年の洪水後、丘の上の新市街ウェストモントへの足として1891年に架けられたもの——richの一行はこの経緯に基づく。

## snaps の写真(6枚、写真ファーストで目視選定+ライセンス確認、2026-08-27)

| 場所 | Commonsファイル | 作者 / ライセンス | 年代 |
|---|---|---|---|
| ランカスター郡の道 | Horse and buggy on the road in "Amish Country," Lancaster County, Pennsylvania LCCN2011635714.tif | Carol M. Highsmith, PD | いま |
| フィラデルフィア・9番街市場 | Part of the 9th Street Italian Market, the nation's oldest working outdoor market, Philadelphia, Pennsylvania LCCN2011633564.tif | Carol M. Highsmith, PD | いま |
| 南フィラデルフィアの角 | Pat's King of Steaks (Philadelphia, Pennsylvania) 001.jpg | Leonard J. DeFrancisci, CC BY-SA 3.0 | いま |
| ピッツバーグ・ストリップ地区 | Strip District Pittsburgh Saturday Market.jpg | Jim Reynolds, CC BY 2.0 | いま |
| シェナンドー | View of Shenandoah, PA.JPG | Shuvaev, CC BY-SA 4.0 | いま |
| ピッツバーグの丘 | Rows of frame houses in a hilly area of Pittsburgh, with the smoke-shrouded city in the background, ca. 1940 - NARA - 518066.jpg | NARA, PD | 1940年ごろ |

- 全18枚の500pxサムネイルURLがHTTP 200を返すことを確認(2026-08-27。取得はAPIのthumburlをそのまま使用、.tifは lossy-page1 形)。原画像はいずれも幅1280px以上(拡大表示に対応)。
- スナップ選定の没: パンクサトーニーのグラウンドホッグデー(2022年の一式、CC BY 2.0)——場面は良いが、どのカットも取扱人の顔の大写しで方針(私人の顔の大写しは避ける)に合わず不採用。シェナンドー・ハイツの住宅1枚(場面が凡庸)。1938年のシェルドン・ディックのFSA写真群(場面は抜群だが原画像の幅が1280px未満で拡大要件を満たさない)。
- 座標の特記: 「ピッツバーグの丘」(NARA, ca.1940)は撮影地点の記録がなく、市南側の斜面住宅地の代表点を置いた(実況文は写真の中身のみを語り、地点を断定しない)。「ランカスター郡の道」も同様に郡東部の農村部の代表点。

## ブラウザ検証(2026-08-27、Playwright + ローカルHTTPサーバ)

自動テスト23項目すべて合格(チップ巡回2項目は初回実行で地図の移動アニメーション完了前に読んでいたための誤検知で、待ちを延ばして合格を確認)。サンドボックスのブラウザから外部に出られないため、unpkg(Leaflet)・地図タイル・Commons画像はローカルに取得した実物で差し替えて供給した(サイト側のコードは無改変で検証)。

- [x] 章ページに📍リンク12個。タップで地図パネルが開き、該当地点の吹き出しが開く(注8リンクのセントラリアを含む)
- [x] チップ13個(全体+12)で全地名を巡回。ピンの節番号表示が正しい(セントラリアは「注8」表示)
- [x] `?rich`(章末おまけ)で写真・クレジット・📷スナップピン6個。写真タップで全画面拡大(1280px版への差し替え)が開閉する
- [x] モバイル幅(375px)でもパネル・リンク・吹き出しが動く
- [x] 他章に影響なし(tx: リンク10個・パネル・吹き出し従来通り。トップページに13章)
- [x] `python site/build.py` 警告なし(JSONの書式検査を兼ねる)
