# コロラド章の地図 検証記録(co-check)

地図データは co.json。作業手順は site/MAPS.md。紙面の編集用注記(text/usa/co-check.md)とは別物で、こちらは地図(ウェブ版限定)の楽屋である。

## 経緯

- 2026-09-03 初版。章のマージ後、依頼者の指示で後工程として作成。places 12(本文の筋の地名、登場順。節リンク11・注リンク1)+ snaps 5(現代4・1972年1)。extras は置いていない(アメリカ50州では任意)。

## places の写真(12枚、ライセンスはCommons APIのextmetadataで確認、2026-09-03)

| 地名 | Commonsファイル | 作者 / ライセンス |
|---|---|---|
| アリカリー川 | Arikaree River.JPG | Jeffrey Beall, CC BY 4.0 |
| ガーデン・オブ・ザ・ゴッズ | Garden of the Gods, with Pikes Peak in the background.JPG | CaroleHenson, CC BY-SA 4.0(章の図2と同一) |
| ロイヤルゴージ | Vista of the suspension bridge spanning the Royal Gorge... (7725171914).jpg | ボストン公共図書館所蔵の絵はがき(1930-45年頃), パブリックドメイン |
| ラガリータ・カルデラ | LaGaritaWilderness.jpg | Fred Bauder, CC BY-SA 3.0 |
| ブラックキャニオン | Painted Wall, Black Canyon Of The Gunnison.jpg | 米国立公園局/Lisa Lynch, パブリックドメイン(章の図4と同一) |
| グレートサンドデューンズ | Star Dune and Crestone Peaks (51985120756).jpg | 米国立公園局, パブリックドメイン(章の図5と同一) |
| メサベルデ | Mesa Verde National Park Cliff Palace 2006 09 12.jpg | Andreas F. Borchert, CC BY-SA 4.0(章の図6と同一) |
| クローリー郡 | Ordway, Colorado.JPG | Jeffrey Beall, CC BY 4.0 |
| リードビル | Leadville, Harrison Ave, Opera House.jpg | Pimlico27, CC BY-SA 4.0 |
| サンドクリーク | Short Grass plains of Sand Creek Massacre Site.jpg | Chris Light, CC BY-SA 4.0 |
| デンバー | Mount Blue Sky with Denver Skyline, Colorado (US).jpg | Justusco, CC BY-SA 4.0 |
| ボールダー | Flatirons Winter Sunrise edit 2.jpg | Jesse Varner(AzaToth補正), CC BY-SA 2.5 |

- ラガリータは「眺めてもただの山なみ」という本文の記述に合わせ、カルデラ一帯の高原の一枚を選んだ(候補のウィーラー地質保護区の別カット2点はライセンスがFAL=自由芸術ライセンスで、PD/CCに限る本書の基準の外なので不採用。章の図3のPD写真は原画像889pxで拡大要件1280pxを満たさず、地図では使わない)。
- ロイヤルゴージは1930年代の彩色絵はがき(PD)。注5の「1929年に架かった吊橋」と場面が合う。
- サンドクリークは草原だけの一枚を選んだ。史跡の標識の写真より、現場の何も無さのほうが章の記述に合う。
- アリカリー川の写真の撮影地点はユマ郡内(ビーチャー島付近)で、ピンの位置(州の最低地点=カンザス州境)とは川沿いに離れている。richの文はその前提で書いた。

## snaps の写真(5枚、同日に目視選定+ライセンス確認)

| 場所 | Commonsファイル | 作者 / ライセンス | 年代 |
|---|---|---|---|
| アイゼンハワートンネル | Traffic stopped at a red light at Johnson Tunnel 2019-03-27.jpg | Xnatedawgx, CC BY-SA 4.0 | いま |
| パリセード | Fruit Stand, Palisade, CO 9-24-13a (10653660613).jpg | inkknife_2000, CC BY-SA 2.0 | いま |
| デンバー・コルファックス通り | Colfax Avenue West, Denver - NARA - 544793.jpg | Bruce McAllister/EPA(ドキュメリカ), パブリックドメイン | 1972年 |
| メダノ川 | Medano Creek at the Great Sand Dunes... (48257161496).jpg | PEO ACWA, CC BY 2.0 | いま |
| リードビル・ハリソン通り | Leadville, Harrison Ave, southeast part (friday afternoon).jpg | Pimlico27, CC BY-SA 4.0 | いま |

- トンネルの一枚は、スノーモービルを牽いた車列が坑口の信号で止まる場面。6節のI-70の記述と響き合う、絵はがきにならない週末の風景として採った。
- コルファックス通り(1972年)は、西向きの通りの突き当たりにそのまま雪の山脈が立つ一枚。章の軸(山と平原の継ぎ目の町)がそのまま写っている。
- メダノ川は、砂丘の前の浅い川に人が散らばる初夏の場面。3節の「風と水の砂の循環」の当の川が、州民の海水浴場でもあることを見せる。
- スナップ選定の没: 同じドキュメリカのデンバーの一枚(NARA 544813)は川岸の不法投棄標識の写真で、環境記録ではあるが暮らしの場面ではないため不採用。バーロ(ロバ)レース、FSAのサンルイス谷(1939年)はCommonsで適切な写真が見つからず見送り。

## 検証記録(2026-09-03)

- `python site/build.py` 警告・エラーなし(26章)。JSONの `img` 全17本(places12+snaps5)が upload.wikimedia.org の500pxサムネイルで、HTTP 200をcurlで確認。原画像の幅は全点1280px以上(最小はロイヤルゴージの1500px)。
- ブラウザ検証: `_site/` をローカルHTTPサーバで開き、Playwright(Chromium)で確認。この実行環境ではブラウザが外部CDNにTLSで届かないため、MAPS.md 6節の但し書きに沿い、外部リクエストをcurl経由で充足するインターセプトで実施した(unpkgのLeaflet・タイル・写真とも実物を取得。外部543リクエスト充足・失敗0)。
  - [x] 地図パネルが開閉し、本文の📍地名タップで該当地点に飛んで吹き出しが開く(アリカリー川→「注1」バッジつき吹き出し)
  - [x] チップで全地名を順に回れる(チップ13=全体+12地名)。ピンの節/注番号表示が正しい(注,1,1,2,3,3,4,4,5,5,5,6——アリカリー川のみ注リンク)
  - [x] `?rich` でピン17本(places12+📷スナップ5)、チップ18、写真・クレジット表示を確認。スナップの吹き出し(アイゼンハワートンネル・era「いま」・写真・クレジット)も開いた
  - [x] 章末おまけのiframe経由で写真タップ→親ページの全画面表示(gs-lightbox)が開く(パリセードの一枚で確認)
  - [x] モバイル幅(375px)でもリンク→吹き出しが動く(アリカリー川)
  - [x] 他の章のページに影響がない(ut.htmlの📍リンクとパネル動作を確認)
- Wikimediaのレート制限(429)が今回も強く、API検索・サムネイル取得とも15〜120秒の待ちとリトライを挟んで通した。

## 座標の根拠

- アリカリー川は州の最低地点(ユマ郡北東端、カンザス州境付近 40.0022, -102.0524)に概置。CO/NE/KSの三州境点のすぐ近くである。
- ラガリータ・カルデラは陥没域のほぼ中央(37.75, -106.93)に概置——縁も中心も地表では判別できない地形のため。
- メサベルデはクリフパレスの現地、ブラックキャニオンは国立公園の南リム(チャズムビュー周辺)、グレートサンドデューンズは砂丘主部、ロイヤルゴージは吊橋。
- クローリー郡は郡庁所在地オードウェイ、サンドクリークは国定史跡、アイゼンハワートンネルは東坑口、メダノ川は砂丘前の遊水部、コルファックス通りは議事堂東方の撮影方向に合わせて概置。
