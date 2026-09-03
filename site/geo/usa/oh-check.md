# オハイオ章の地図 検証記録(oh-check)

地図データは oh.json。作業手順は site/MAPS.md。紙面の編集用注記(text/usa/oh-check.md)とは別物で、こちらは地図(ウェブ版限定)の楽屋である。

## 経緯

- 2026-09-03 初版。章のマージ後、依頼者の指示で後工程として作成。places 12(本文の筋の地名、登場順。注リンク1・節リンク11)+ snaps 5(現代3・1973年1・1938年1)。extras は置いていない(アメリカ50州では任意)。

## places の写真(12枚、ライセンスはCommons APIのextmetadataで確認、2026-09-03)

| 地名 | Commonsファイル | 作者 / ライセンス |
|---|---|---|
| ニューアーク | Octagon Earthwork2016.jpg | A21sauce, CC BY-SA 4.0 |
| アクロン | Downtown skyline panorama as seen from Ohio & Erie Canalway, Akron, Ohio - 20200530.jpg | Andre Carrotflower, CC BY-SA 4.0 |
| トレド | Toledo, Ohio Skyline, July 2022.jpg | MrJacon000, CC BY-SA 4.0 |
| デイトン | Dayton Skyline - Sunset September 2022.jpg | Blervis, CC BY 4.0 |
| ハフマン・プレーリー | Huffman Prairie.jpg | Ismael Laos, CC BY-SA 4.0 |
| シンシナティ | Cincinnati Skyline from Roebling Bridge, Covington, KY.jpg | w_lemay, CC BY-SA 2.0 |
| エヴァンデール | CFM56 below the wing of a Lufthansa A320.jpg | Olivier Cleynen, CC BY 4.0(章の図5と同一) |
| クリーブランド | Cuyahoga river and downtown cleveland.jpg | GandZ, CC BY-SA 3.0 |
| ヤングスタウン | Youngstown, Ohio Central Square West Federal Street.jpg | Jack Pearce, CC BY-SA 2.0 |
| ロードスタウン | Lordstown Assembly front, June 2024.jpg | Mr. Matté, CC BY-SA 4.0 |
| コロンバス | View of Downtown Columbus Ohio OH from North Bank Park Pavillion on Scioto River.jpg | Rfgagel, パブリックドメイン(章の図7と同一) |
| ニューオールバニー | New Albany City Hall 1.jpg | Sixflashphoto, CC BY-SA 4.0 |

- エヴァンデールは工場自体の使える写真がCommonsに無く、この工場が最終組立の中心を担うCFM56の写真(章の図5)を充てた。候補にあったXA100の写真はパブリックドメイン表示の根拠が怪しく(GE Aviation撮影)、不採用。
- ヤングスタウンの当初候補(旧デムジー製鉄所跡の再開発記録写真)は場面が読めず(日付透かし入りのシート山)、市街のフェデラル通りに差し替えた。

## snaps の写真(5枚、同日に目視選定+ライセンス確認)

| 場所 | Commonsファイル | 作者 / ライセンス | 年代 |
|---|---|---|---|
| ウェストサイド・マーケット(クリーブランド) | West Side Market - Cleveland - 12.jpg | APK, CC BY 4.0 | いま |
| シンシナティの昼食 | Skyline Chili Coneys.jpg | Navin75, CC BY-SA 2.0 | いま |
| サークルビルの収穫祭 | Circleville Pumpkin Show 02.jpg | Ɱ, CC BY-SA 4.0 | いま |
| 製鉄所のそばの通り(クリーブランド) | SMOKE FROM REPUBLIC STEEL BLANKETS THE NEIGHBORHOOD - NARA - 550187.jpg | Frank John Aleksandrowicz(EPA・ドキュメリカ), パブリックドメイン | 1973年 |
| ワージントンの路上 | Getting crank out of car to get the motor started, Worthington, Ohio, 1938 crop.jpg | Ben Shahn(FSA), パブリックドメイン | 1938年 |

- 1938年のワージントンの一枚は、車のクランク始動の場面で、本文4節(セルモーターの発明)と響き合うため選んだ。人物は後ろ姿で顔は写らない。
- 1973年のリパブリック製鉄の煙の写真は、NARAの記録に街区の詳細がなく、ピンは製鉄所寄りの住宅地に概置した。シンシナティの昼食のピンも、チェーンの特定店舗ではなくダウンタウンに概置。
- スナップ選定の没: ニューオールバニーの朝市(私人の顔が近い)、アーミッシュ・カントリー・バイウェイ(道だけで場面が弱い)、ロードスタウン最後のクルーズ(展示室の写真で場面が弱い)、ウェストサイド・マーケットの別カット(牛の剥製の仰角で場面が読めない)、オハイオ州フェアのミッドウェイ(古い絵はがき写真で年代が曖昧)。

## 検証記録(2026-09-03)

- `python site/build.py` 警告・エラーなし(22章)。JSONの `img` 全17本(places12+snaps5)が upload.wikimedia.org の500pxサムネイルで、HTTP 200をcurlで確認。原画像の幅は全点1280px以上。
- ブラウザ検証: `_site/` をローカルHTTPサーバで開き、Playwright(Chromium)で確認。この実行環境ではブラウザが外部CDNにTLSで届かないため、MAPS.md 6節の但し書きに沿いつつ、今回はLeafletの差し替えではなく、外部リクエストをcurl経由で充足するインターセプトで実施した(unpkg・タイル・写真とも実物を取得。外部233リクエスト充足・失敗0)。
  - [x] 地図パネルが開閉し、本文の📍地名タップで該当地点に飛んで吹き出しが開く(ハフマン・プレーリー→「4節」バッジつき吹き出し)
  - [x] チップで全地名を順に回れる(チップ13=全体+12地名)。ピンの節番号表示が正しい(トレド=3、デイトン=4 ほか目視)
  - [x] `?rich` でピン17本(places12+📷スナップ5)、写真・クレジット表示、写真タップで全画面拡大が動く
  - [x] モバイル幅(375px)でもリンク→吹き出しが動く(ニューアーク・注3バッジ)
  - [x] 他の章のページに影響がない(pa.htmlの表示を確認)
- 検証時のベースタイルに「API KEY REQUIRED」の透かしが出るのは、中継取得にRefererが付かないことによるCARTO側の応答で、テンプレート共通・今回の変更とは無関係(本番のPagesでは既刊章と同条件)。
- 座標の根拠: ニューアークは八角形土塁の現地(40.0529, -82.4442)、ハフマン・プレーリーは飛行場史跡、エヴァンデールはGE工場、ロードスタウンは旧GM工場(向かいが電池工場)。他は市街中心。
