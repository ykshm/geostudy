# カムチャツカ地方章の地図 検証記録(kamchatka-check)

地図データは kamchatka.json。作業手順は site/MAPS.md。紙面の編集用注記(text/russia/kamchatka-check.md)とは別物で、こちらは地図(ウェブ版限定)の楽屋である。

## 経緯

- 2026-09-05 初版。章のマージ後、依頼者の指示で後工程として作成。ロシアシリーズ最初の地図(site/geo/russia/ を新設)。places 10(本文の筋の地名、登場順。節リンク9・注リンク1)+ snaps 5(現代4・1904年1)。extras は置いていない(第4シリーズの決まりに定めが無いため、アメリカ50州と同じく任意と扱い、初回は見送り。以後の扱いは依頼者の判断に委ねる)。
- 「クラ試験場」は本文の筋の地名だが、閉鎖区域で使える写真がCommonsに無く、placesの必須項目(img)を満たせないため見送った。代わりに同じ節のアバチャ湾を採った。「パウジェトカ」「ビリュチンスク」も写真の要件(下記)を満たせず見送り、地熱はムトノフスキー火山のピンが受け持つ。

## places の写真(10枚、ライセンスはCommons APIのextmetadataで確認、2026-09-05)

| 地名 | Commonsファイル | 作者 / ライセンス |
|---|---|---|
| クリル・カムチャツカ海溝 | Mapping Kamchatka Earthquake Displacement (154776 - kamchatka aria 20250802 lrg).jpg | NASA地球観測所, パブリックドメイン |
| クリュチェフスカヤ山 | Ključevskaja za východu slunce.jpg | Tamten, パブリックドメイン(章の図2と同一) |
| セベロクリリスク | Severo-Kurilsk.jpg | Eugene Kaspersky, CC BY-SA 4.0 |
| ベズイミアニ | Bezymianny, Kamen, and Kluychevskaya Sopka volcanoes in Kamchatka, Russia.jpg | SentinelHub(Copernicus Sentinelデータ), CC BY 2.0 |
| トルバチク火山 | Радуга над вулканическими конусами.jpg | Ted.ns, CC BY-SA 4.0(章の図3と同一) |
| 間欠泉の谷 | Valley of Geysers (Kamchatka, 2020)-1.jpg | Rubin16, CC BY-SA 4.0(章の図4と同一) |
| ムトノフスキー火山 | Фумаролы вулкана Мутновский.jpg | Nimuel23, CC BY-SA 4.0 |
| クリル湖 | Salmon and Bear (7765066002).jpg | Harald Deischinger, CC BY 2.0(章の図5と同一) |
| アバチャ湾 | Tri Brata(15340620491).jpg | kuhnmi, CC BY 2.0 |
| ペトロパブロフスク・カムチャツキー | Kamchatka Petropavlovsk-Kamchatsky and its Volcanoes (24212090170).jpg | kuhnmi, CC BY 2.0(章の図6と同一) |

- 海溝は撮影できる被写体ではないため、NASAの2025年地震の地殻変位図(南部ほど赤い)を当てた。richの文はその前提で書いた。
- ベズイミアニの単独の地上写真はCommonsでは幅1280px未満のものしかなく(Bezymyannyi volcano.jpg=1024px)、雲海から群峰が頭を出す衛星写真を採った。噴気の尾を引く峰がベズイミアニであることは画像の説明と山の位置関係で確認した。
- 見送った候補: 1952 Severo-Kurilsk earthquake.jpg(CC0だが原画像787pxで拡大要件1280pxを満たさない)/Viktor Chirkov in Vilyuchinsk 01・02.jpg(CC BY 4.0だが550px)/Street in Paratunka.jpg(CC BY 4.0だが768px)。

## snaps の写真(5枚、同日に目視選定+ライセンス確認)

| 場所 | Commonsファイル | 作者 / ライセンス | 年代 |
|---|---|---|---|
| ハラクティルスキー海岸 | Surfing on the Halaktyr beach of Kamchatka Peninsula.jpg | tanysolovey, CC BY-SA 2.0 | いま |
| クリュチのサケ梁 | DEMIDOV(1904) p272 SALMON CAUGHT IN TRAP AT KLUCHI (14595813020).jpg | E. P. デミドフ『A Shooting Trip to Kamchatka』(1904年刊・著者1943年没), パブリックドメイン | 1904年 |
| ハラクティルカ飛行場 | Russia, Kamcatka, Petropavlovsk-Kamchatskiy - Halaktyrka airport (Petropavlovsk-Kamchatsky) WMID5366347.jpg | jahromez, CC BY-SA 3.0 | いま |
| ミシェンナヤの丘から | Petropavlovsk-Kamchatsky, 2025.jpg | Nikita Zhuravlev, CC BY-SA 4.0 | いま |
| パラトゥンカ | Kamchatka 2010 683.jpg | Einar Fredriksen, CC BY-SA 2.0 | いま |

- サーフィンの一枚は真上からのドローン写真で、黒い砂の海と青いボードの対比が5節(黒砂の海岸・赤潮でサーファーが目を痛めた海)と響き合う。
- 1904年のデミドフの狩猟旅行記の写真は、5節のサケの暮らしの昔の一枚として採った(昔を1〜2枚の方針)。撮影地クリュチは1節のクリュチェフスカヤ山の麓の村で、ピンは村に置いた。
- ミシェンナヤの丘の一枚は、団地の連なりと「うちの火山」が一枚に収まる現在の生活の眺め。6節の耐震の話を実況文に添えた。
- パラトゥンカは温泉プールの写真ではなく裏通りの生活道路の一枚(撮影地はCommonsのCategory:Paratunka)。絵はがきにならない場面として採った。
- スナップ選定の没: セベロクリリスクの目抜き通り(214 1426 Sev Kur main street wiki.jpg)は1152pxで拡大要件を満たさず見送り。市場・ヘリ発着の場面はCommonsで適切な写真が見つからず見送り。

## 検証記録(2026-09-05)

- `python3 site/build.py` 警告・エラーなし(27章)。JSONの `img` 全15本(places10+snaps5)が upload.wikimedia.org の500pxサムネイルで、HTTP 200をcurlで確認。原画像の幅は全点1280px以上(最小はデミドフの1516px)。
- ブラウザ検証: `_site/` をローカルHTTPサーバで開き、Playwright(Chromium、環境備え付けの /opt/pw-browsers/chromium)で確認。MAPS.md 6節の但し書きに沿い、外部リクエスト(unpkgのLeaflet・地図タイル・写真)はcurl経由で充足するインターセプトで実施した(外部1,017リクエスト充足・失敗0)。
  - [x] 地図パネルが開閉し、本文の📍地名タップで該当地点に飛んで吹き出しが開く(クリル・カムチャツカ海溝)
  - [x] チップで全地名を順に回れる(チップ11=全体+10地名)。ピンの節/注番号表示が正しい(1,1,2,3,3,注,4,5,6,6——間欠泉の谷のみ注リンク)
  - [x] `?rich` でピン15本(places10+📷スナップ5)、チップ16、写真・クレジット表示を確認。スナップの吹き出し(ハラクティルスキー海岸・era「いま」・写真・クレジット)も開いた
  - [x] 章末おまけのiframe経由で写真タップ→親ページの全画面表示(gs-photo-lightbox)が開く
  - [x] モバイル幅(375px)でもリンク→吹き出しが動く(クリル・カムチャツカ海溝)
  - [x] 他の章のページに影響がない(usa/co.htmlの📍リンク12本の健在を確認)
- WikimediaのAPIはレート制限が強く、検索・メタデータ・サムネイル取得とも呼び出し間に40〜95秒の待ちとリトライを挟んで通した(一括のtitles指定で呼び出し回数自体も減らした)。

## 座標の根拠

- クリル・カムチャツカ海溝はペトロパブロフスク沖の海溝軸付近(52.0, 160.8)に概置——線状の地形のため、章が語る2025年の震源域の沖合を選んだ。
- クリュチェフスカヤ山・ベズイミアニ・トルバチクは各火山の山頂(スミソニアンGVPの座標)。間欠泉の谷はゲイゼルナヤ川の谷、クリル湖は湖心、ムトノフスキーは山体。
- セベロクリリスクは町の中心、アバチャ湾は湾口付近(三兄弟の岩の側)、ペトロパブロフスクは市街中心。
- スナップ: ハラクティルスキー海岸は浜の中央部、クリュチは村、ハラクティルカ飛行場は市街東方の飛行場(位置はWikimapiaの記載に基づく概置)、ミシェンナヤの丘は展望点、パラトゥンカは村の中心に概置。
