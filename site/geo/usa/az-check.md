# アリゾナ章の地図 検証記録(az-check)

地図データは az.json。作業手順は site/MAPS.md。紙面の編集用注記(text/usa/az-check.md)とは別物で、こちらは地図(ウェブ版限定)の楽屋である。

## 経緯

- 2026-08-27 初版。アリゾナ章(text/usa/az.md)のマージ後の後工程として作成。places 11箇所(本文の登場順)+snaps 5枚。
- 地名の選定: 章の筋を運ぶ地名だけを採った。グランドキャニオンは本文1節では愛称の引用内にしか出ないため、単独で現れる注3にリンクを付けた。モレンシは図2の説明文の初出で1節にリンク(図の説明文もリンク化対象)。フェニックスは1節にも現れるが、街の来歴を語る2節側に付けた。
- 座標の特記: モレンシは鉱山の現場、パーカーダムはダム地点、ヒラリバー・インディアン・コミュニティは中心集落サカトン、オーク・フラットはUS-60沿いの台地(スペリオル東)、ミード湖はフーバーダム上流のブラックキャニオン付近(図6と同じ視点側)。スナップの「フェニックス北郊」はDOCUMERICA原題が撮影地点を特定しないため、写真の構図(郊外住宅地を見下ろす)に合わせて北郊の概略位置に置いた。

## places の写真(11枚、ライセンスはCommons APIのextmetadataで確認、2026-08-27)

| 地名 | Commonsファイル | 作者 / ライセンス |
|---|---|---|
| グランドキャニオン | Grand Canyon South Rim at Sunset.jpg | Mgimelfarb, CC0 |
| モレンシ | Morenci Mine 2012.jpg | Stephanie Salisbury, CC BY 2.0(紙面の図2と同一) |
| フェニックス | Downtown Phoenix Skyline Lights.jpg | Alan Stark, CC BY-SA 2.0 |
| サンシティ | Sun City, Arizona (101300784).jpg | Ken Lund, CC BY-SA 2.0(紙面の図3と同一) |
| パーカーダム | Arizona National Guard members filling canteens at water's edge, Colorado River, near Parker, Arizona, 1934.jpg | Los Angeles Times, CC BY 4.0(1934年の「アリゾナ海軍」出動時の報道写真) |
| ツーソン | Tucson skyline.JPG | Sahmeditor, CC BY-SA 3.0 |
| ユマ | NRCSAZ02032(347)(NRCS Photo Gallery).jpg | Jeff Vanuga / USDA NRCS, パブリックドメイン(紙面の図5と同一) |
| ヒラリバー・インディアン・コミュニティ | 2014, View E, the GIla River and Olberg Bridge and Sacaton Dam - panoramio.jpg | Chris English, CC BY-SA 3.0(乾いたヒラ川の川床——本文4節の「川を抜かれた」景観そのもの) |
| チャンドラー | President Joe Biden announces CHIPS and Science Act grants to Intel ... at the Intel Ocotillo Campus in Chandler, Arizona.jpg | The White House, パブリックドメイン(人物は写らず、増設現場のクレーンとCHIPS法の看板の画) |
| オーク・フラット | EliasButler-OakFlat-2021.jpg | Elias Butler (SinaguaWiki), CC BY-SA 4.0(extmetadataのArtist欄は投稿者名SinaguaWiki。ファイル名の撮影者を併記) |
| ミード湖 | Lake Mead and its bathtub ring upstream of Hoover Dam, Black Canyon, Arizona–Nevada.jpg | Christian David, CC BY-SA 4.0(紙面の図6と同一) |

## snaps の写真(5枚、写真ファーストで目視選定+ライセンス確認、2026-08-27)

| 場所 | Commonsファイル | 作者 / ライセンス | 年代 |
|---|---|---|---|
| ツーソン・南12番通り | El Güero Canelo (48199857287).jpg | miheco, CC BY-SA 2.0 | いま |
| フラッグスタッフ | Snowy street Flagstaff January 2019.jpg | Coincidence Cafe, CC BY 2.0 | いま |
| フェニックス・ルーズベルト通り | Phoenix, AZ Roosevelt Row, Bliss, El Mac and Kofie, 2011 - panoramio.jpg | Chris English, CC BY-SA 3.0 | いま |
| フェニックス北郊 | DUST STORM RISES OVER PHOENIX ON LABOR DAY, 1972. ... - NARA - 544078.jpg | Cornelius M. Keyes / EPA(DOCUMERICA), パブリックドメイン | 1972年 |
| エロイ | Eloy District, Pinal County, Arizona. Children in a democracy. Bus carries migratory cotton pickers' ... - NARA - 522030.jpg | Dorothea Lange / FSA, パブリックドメイン | 1940年 |

- スナップ選定の没: DOCUMERICA「LABOR DAY DUST STORM VIEWED FROM CENTRAL AVENUE」544017(題名と中身が合わない——造成地の空き地の写真だった。544078に差し替え)、「Welcome to Phoenix / Population 620,000」の道路標識1972(場面は良いが昔枠は2枚までの方針)、レイクハバス・シティーの少年野球1972(同上)、クォーツサイトの空撮(RVの冬の集結が読み取れず凡庸)、サンシティのFDPIR配給センター写真群(原画像幅1024pxで拡大要件1280pxに満たない)、NRCSのレタス収穫機の接写(機械のアップで場面が読めない)。
- 全16枚の500pxサムネイルURLと、拡大用の1280px版URLの計32本がHTTP 200を返すことを確認(2026-08-27)。原画像はいずれも幅1280px以上。チャンドラーのみ、ファイル名が長すぎるためAPIのthumburlが `500px-thumbnail.jpg` 形式になる——テンプレートの拡大処理(500px→1280pxの置換)でも `1280px-thumbnail.jpg` が200を返すことを確認済み。

## 動作検証(2026-08-27)

- `python3 site/build.py` 警告・エラーなし(14章)。
- `_site/` を `python3 -m http.server` で配信し、Chromium(Playwright)で自動検証20項目すべてPASS:
  - 章ページの📍リンク11本(モレンシ/グランドキャニオン/フェニックス/サンシティ/パーカーダム/ツーソン/ユマ/ヒラリバー・インディアン・コミュニティ/チャンドラー/オーク・フラット/ミード湖)
  - パネルの開閉、📍タップで該当地点の吹き出し(節番号バッジつき)、チップ12個(全体+11)で巡回
  - `?rich` でピン16本(地名11+📷5)・チップ17個、スナップ吹き出しに写真・年代・クレジット、写真タップで1280px版の全画面拡大
  - 章末「おまけ: 地図で歩き直す」節とrich指定のiframe
  - モバイル幅(390px)での開閉とピン表示
  - 他章への影響なし(tx章のリンク10本・rich地図ピン17本のまま、地図なし章も表示正常)
- 検証環境の特記: この作業環境の外向きネットワークはCDN(unpkg.com、cartocdn、arcgisonline)とupload.wikimedia.orgへのブラウザ直アクセスを遮断するため、ブラウザ検証ではLeaflet 1.9.4をnpmの同一版で、タイルと写真をローカルスタブで差し替えて機構を検証した(生成物は無改変)。画像URL自体の疎通はHTTPクライアントで全32本200を確認済み。本番(GitHub Pages)は利用者のブラウザから直接CDNへ届く構成で、既存章と同じ経路である。
