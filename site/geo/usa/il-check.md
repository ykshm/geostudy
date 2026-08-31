# イリノイ章の地図 検証記録(il-check)

地図データは il.json。作業手順は site/MAPS.md。紙面の編集用注記(text/usa/il-check.md)とは別物で、こちらは地図(ウェブ版限定)の楽屋である。

## 経緯

- 2026-08-31 初版。章(text/usa/il.md)のマージ後の後工程として作成。places 12 + snaps 5。

## places の写真(12枚、ライセンスはCommons APIのextmetadataで確認、2026-08-31)

| 地名 | Commonsファイル | 作者 / ライセンス |
|---|---|---|
| スプリングフィールド | Old Illinois State Capitol, Adams Street, Springfield, IL.jpg | w_lemay, CC BY-SA 2.0 |
| シカゴ川 | Chicago River toward Michigan Avenue at blue hour.jpg | NorbertNagel, CC BY-SA 4.0 |
| ユニオン・ストックヤード | Chicago Union Stockyard Gate.jpg | Zol87, CC BY-SA 2.0 |
| プルマン | Hotel Florence, Pullman National Monument.jpg | Matthew Dillon, CC BY 2.0 |
| ノース・ローンデール | North Lawndale Sunset.jpg | Jonathan Lee, CC BY 2.0 |
| カブリニ=グリーン | Cabrini-Green (8038096318).jpg | edwardhblake, CC BY 2.0 |
| ジャクソン・パーク | Museum of Science and Industry - Hyde Park Neighborhood - Chicago - Illinois - USA.jpg | Adam Jones, CC BY 2.0 |
| ハル・ハウス | Jane Addams Hull House Museum - Exterior 1 (7541050386).jpg | Chicago Architecture Today, CC BY 2.0 |
| ピルゼン | 20160329 103 18th St. @ Loomis St. (32181520506).jpg | David Wilson, CC BY 2.0 |
| リトル・ビレッジ | La Villita.jpg | Peter Fitzgerald, CC BY-SA 4.0 |
| イングルウッド | Englewood Chicago 1.JPG | MrHarman, CC BY-SA 4.0 |
| ケーロ | Commercial Street Cairo Illinois Closed.jpg | hickory hardscrabble, CC BY 2.0 |

- リンク先の節/注: ケーロだけ本文でなく注34(ダウンステートの注)にリンク。他は本文の初出の節。シカゴ自体は章全体の舞台なのでピンにしない。サウス・ワークス(量子パーク、注35)はCommonsに使える写真が見つからず、ピンを見送った。
- 座標の特記: シカゴ川はミシガン・アベニュー橋(写真の地点)。ユニオン・ストックヤードは現存する正門(エクスチェンジ・アベニュー)。プルマンはホテル・フローレンス。ジャクソン・パークは公園中央(万博跡とオバマセンターの中間)。イングルウッドは63丁目×ホルステッド(写真の交差点)。ケーロはコマーシャル・アベニュー。
- 目視の記録: 全12枚を500pxサムネイルで実見し、richの文を実写に合わせた(旧州議事堂は柵越しの正面、シカゴ川はリグレー・ビルの時計塔入り、ストックヤードは牛の頭の彫刻のある門、ノース・ローンデールは雪のケジー駅にピンクラインが入る構図、カブリニは壁面のアップ、科学産業博物館はカリアティード柱廊と緑の丸屋根、ラ・ビジータは門と旗と露店、イングルウッドは高架駅が奥に写る交差点、ケーロは廃業した商店の並び)。当初候補のうち、科学産業博物館の遠景(exterior 02)とハル・ハウスの案内板メインの一枚は構図が弱く差し替えた。

## snaps の写真(5枚、同日に目視選定+ライセンス確認)

| 場所 | Commonsファイル | 作者 / ライセンス |
|---|---|---|
| 63丁目通り(1973年) | BLACKS USING BUS TRANSPORTATION ON 63RD STREET IN CHICAGO DURING 1973 … - NARA - 556203.jpg | John H. White(DOCUMERICA), パブリックドメイン |
| マクスウェル通り(1987年) | Maxwell Street, Chicago, November 1987; photographer, Jeff Wassmann.jpg | Jeff Wassmann, CC BY-SA 4.0 |
| サーマック通り(2006年) | Paletas in Time of War (247290405).jpg | Señor Codo, CC BY-SA 2.0 |
| デヴォン通り | Devon Street (117977640).jpg | Erstwhile.Human, CC BY-SA 2.0 |
| ミルフォード | Milford Illinois Village Hall and Elevator.jpg | Dual Freq, CC BY 2.5 |

- 写真ファーストで選定。昔の枠はDOCUMERICA(1973年・ジョン・H・ホワイトの黒人シカゴ連作)から1枚と、1987年のマクスウェル通りの青空市(古着のコート越しにシアーズ・タワー)。パレタ売りは2006年(壁画イベントの脇を通る実働の屋台)で、年を明記した。デヴォン通りは南アジア系商店街の看板の列、ミルフォードはダウンステートの「役場と穀物エレベーター」の型。
- 候補にして落としたもの: 35丁目の浜の家族(1973年・遊具の写真で浜が写らない)、Moreno's Liquors(リトル・ビレッジのピンと場所が重複)、デヴォンの旧劇場のテラコッタ装飾(建築のアップで生活の場面でない)、After The Parade(パレタ売りと主題が重複)。
- 原画像の幅は全点1280px以上(最小はミルフォードの1563px)。

## 技術メモ

- `img` は全点 upload.wikimedia.org の500pxサムネイルURL。全URLのHTTP 200を取得時に確認(2026-08-31)。
- Commonsのサムネイル許容幅は現在 20/40/60/120/250/330/500/960/1280/1920/3840 のみ(mediawiki.org「Common thumbnail sizes」)。500pxは許容幅に含まれ、拡大用の1280px版も同様に通ることを確認した。
- `python3 site/build.py` 警告・エラーなし(17章)。地名12個すべてリンク化(未リンク警告なし)。
- ブラウザ検証はPlaywright(chromium)+ローカルHTTPサーバで実施し、以下を確認——章ページに📍リンク12個と章末おまけ節、📍タップでパネルが開き該当地点の吹き出しが開く(パネル内マーカー12本・閉じるボタン)、`?rich` でピン17本(places 12+snaps 5)・チップの節番号表示・写真とクレジット入りポップアップ、モバイル幅(390px)でもピン17本、他章(ny)への影響なし。
- 検証環境の特記: このセッションの下書き環境ではChromiumの外部HTTPSがエージェントプロキシと相性が悪く(接続リセット。curlは同じURLで200)、検証時はLeaflet(curlで取得した実物)と各写真(取得済みの500px実物)をPlaywrightのルーティングでローカル供給し、地図タイルのみダミー画像で代替した。写真URL自体のHTTP 200と実物の中身は取得時に別途確認済み。Pages上の実環境ではCDN・タイルとも通常配信である。
