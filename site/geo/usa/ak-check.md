# アラスカ章の地図 検証記録(ak-check)

地図データは ak.json。作業手順は site/MAPS.md。紙面の編集用注記(text/usa/ak-check.md)とは別物で、こちらは地図(ウェブ版限定)の楽屋である。

## 経緯

- 2026-08-27 初版。章(text/usa/ak.md)のマージ後の後工程として作成。places 12 + snaps 5。

## places の写真(12枚、ライセンスはCommons APIのextmetadataで確認、2026-08-27)

| 地名 | Commonsファイル | 作者 / ライセンス |
|---|---|---|
| ジュノー | Downtown Center Juneau 09.jpg | Gillfoto, CC BY-SA 4.0 |
| デナリ | Denali and Wonder Lake from Air (7065238243).jpg | Jacob W. Frank/米国立公園局, パブリックドメイン |
| アンカレジ | Anchorage and Chugach Mountains.jpg | Frank Kovalchek, CC BY 2.0 |
| バルディーズ | Valdez, Alaska Harbor Panorama.jpg | Srvora, CC BY-SA 3.0 |
| ノバラプタ | Valley of Ten Thousand Smokes from Overlook Cabin.jpg | R. McGimsey/米地質調査所, パブリックドメイン(紙面の図3と同じ写真をURL参照で再利用) |
| コディアック島 | Fishing boat entering Kodiak harbor.jpg | James Brooks, CC BY 2.0 |
| コロンビア氷河 | Alaska's Iconic Columbia Glacier Still Retreats (153291 - oli 20190621 lrg).jpg | NASA地球観測所, パブリックドメイン(紙面の図4と同じ画像) |
| ベーリンジア | Ice and Clouds in the Bering Strait.jpg | NASA, パブリックドメイン |
| ニュートック村 | Newtok - Alaska - August 2019 - 4.jpg | 米上院ムルコウスキー議員事務所, パブリックドメイン |
| ドリューポイント | Collapsed permafrost (9356).jpg | Benjamin Jones/米地質調査所, パブリックドメイン(紙面の図6と同じ写真) |
| プルドーベイ | Deadhorse Alaska aerial view.jpg | 米海軍, パブリックドメイン |
| ヤクタット | Glaciar Hubbard, Alaska, Estados Unidos, 2017-08-20, DD 02.jpg | Diego Delso, CC BY-SA 4.0 |

- リンク先の節: ジュノー・デナリは1節(プロフィール表はリンク対象外のため、本文初出の節)。アンカレジは注1にも出るが話の本体の2節に。ドリューポイントは本文でなく図6の説明文(5節内)に出る表記で、節指定でリンク化されることをビルドと実表示で確認。ニュートックは本文表記「ニュートック村」に一致させた。
- 座標の特記: ノバラプタは噴出口(58.27, -155.16)。コロンビア氷河は氷河本体(61.216, -146.895)。ベーリンジアは実在の一点が無いため、ベーリング海峡の中央(65.80, -168.90)に置いた(textで「いまは海の底の陸橋」と断っている)。ドリューポイントは70.88, -153.90(USGS撮影地)。プルドーベイは油田地帯の概略位置(70.29, -148.67)。ヤクタットは町の位置で、richの写真は湾奥のハバード氷河。
- 写真の特記: ニュートック村の写真は、村そのものではなく川向こうの移転先ミャルタービクの新築群(2019年、建設中)——richの一言にその旨を明記。ムルコウスキー議員視察時の随行撮影(上院事務所公開=連邦政府職務著作でPD)。人物が大写しの別カット(同シリーズ2, 3)は不採用。プルドーベイの高解像度写真はCommonsに乏しく(FWS空撮は504px、1976年のVSM写真は加工が強い)、米海軍の冬の空撮(1866px)を採用。

## snaps の写真(5枚、場面の良さで選定+ライセンス確認、2026-08-27)

| スナップ | Commonsファイル | 作者 / ライセンス |
|---|---|---|
| アイディタロッドの出走式(いま) | Iditarod Ceremonial start in Anchorage, Alaska.jpg | Frank Kovalchek, CC BY 2.0 |
| レイクフッドの水上機基地(いま) | Lake Hood Seaplane Base, Anchorage, Alaska, International Airport.jpg | Laura Alier, CC BY 4.0 |
| ウトキアグヴィクの通り(いま) | Barrow Alaska.jpg | Andrei Taranchenko, CC BY 2.0 |
| ニュートックの学校(1974年) | Newtok 1974 018 (7344054266).jpg | Ernie Tyler, CC BY 2.0 |
| タナナバレー州祭の巨大野菜(いま) | Monster vegetable display at the Tanana Valley State Fair 2010.jpg | Liz(Flickr), CC BY 2.0 |

- 選定メモ: 写真ファーストで拾った。犬ぞり(出走を待てない犬の顔)、水上機(道路の無い州の日常の足)、最北の町の砂利道(絵はがきにならない生活道路)、1974年のニュートックの学校(全村移転の半世紀前の日常。撮影者は当時の滞在者で、実況文は「昔を1〜2枚」の枠)、フェアバンクスの夏祭りの巨大野菜(白夜の産物)。現代4+昔1。現代の私人の顔が大写しの写真は無い。
- 実況文の根拠: アイディタロッドの出走式は3月第一土曜にアンカレジ4番街で開催、全行程約1,000マイル(約1,600キロ)。レイクフッドは世界最繁忙の水上機基地(アラスカ州DOT)。ウトキアグヴィクの極夜は11月下旬から1月下旬(約65日)。タナナバレー州祭の写真の説明に「400ポンド超のカボチャ」とあり180キロ超と記載。

## 技術検証(2026-08-27)

- 全17枚の img URL(500pxサムネイル)と、タップ拡大用の1280px版URLの計34本が HTTP 200 を返すことを確認(コロンビア氷河は原画像がちょうど1280pxで、1280px版URLも200を確認済み)。
- `python3 site/build.py` 警告・エラーなし(12章)。
- `_site/` をローカルHTTPサーバで開き、Chromium(Playwright)で確認:
  - [x] 本文の📍地名(12件全て生成)をタップ → 地図パネルが開き、該当地点(例: ドリューポイント)に飛んで吹き出しが開く
  - [x] チップで全12地名を順に回れる。チップとピンの節番号表示が正しい(1節×2, 2節×2, 3節×2, 4節×2, 5節×2, 6節×2)
  - [x] `?rich` でピン17(places 12+📷スナップ5)、吹き出しに写真とクレジットが出る
  - [x] モバイル幅(390px)でもピン17と操作を確認
  - [x] 他の章に影響なし(wy.htmlの📍リンク7件が従来通り)
- 検証環境の注記: この実行環境ではChromiumが外部CDNに直接出られないため、leaflet.js/css・地図タイル・写真はローカルに用意した実物で差し替えて検証した(タイル画像はOSMの403応答画像が写るが、これは検証用スタブの見た目であり、実際の閲覧ではタイルは読者のブラウザが直接取得する)。写真タップの全画面拡大は、テンプレート共通機構(500px→1280pxの差し替え)のURLが全点200であることをもって確認とした。
