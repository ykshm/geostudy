# テネシー章の地図 検証記録(tn-check)

地図データは tn.json。手順は site/MAPS.md。2026-08-30 作成。

## 地名の選定

本文の筋の12地名(1節メンフィス/2節クウォヒ・リンチバーグ/3節ブリストル/4節ナッシュビル/注9ライマン公会堂/5節ビール・ストリート・サン・スタジオ・ロレイン・モーテル/6節オークリッジ・ノリス・ダム/注22メンフィス国際空港)。章が東の山から西の川へ走る筋なので、東西に散るよう選んだ。ブロードウェイとミュージック・ロウはナッシュビルのピンが代表(市中心部にピンが密集するのを避けた)。スタックスはサン・スタジオが「録音の街」を代表。テネシー川は線なのでノリス・ダムが代表。ブリストルの座標はステート・ストリート(州境の通り)に置いた。オークリッジは市街に置き、写真(K-25空撮)はクリンチ川沿いの工場地帯である旨をrichの文で明示。

- ナッシュビルの初出は2節だが、章の中でこの街が主役になる4節(本文「歌い手がナッシュビルに集まり」)にリンクを付けた。メンフィスは1節(初出)。
- 「サン・スタジオ」の文字列は5節では図4の行にのみ現れる(本文はスタジオを指す语で言い換え)。図の説明文の地名も節指定でリンク化される仕様(MAPS.md 3節)に依る。ビルド後のHTMLで12地名全てのリンク化を確認済み。

## places の写真(12枚、ライセンスはCommons APIのextmetadataで確認、全て目視検査)

| 地名 | Commonsファイル | 作者 / ライセンス |
|---|---|---|
| メンフィス | Memphis, TN skyline along the Mississippi River.jpg | Quintin Soloviev, CC BY 4.0 |
| クウォヒ | Kuwohi (also known as Clingmans Dome) Observation Tower - 1.jpg | APK, CC BY 4.0 |
| リンチバーグ | Jack Daniel Distillery Lynchburg TN 001.JPG | Ben Jacobson, CC BY 2.5 |
| ブリストル | Bristol VA TN sign.jpg | Springfulutopia, CC BY-SA 4.0 |
| ナッシュビル | Broadway (Nashville) lights.jpg(章の図3と同一) | dconvertini, CC BY-SA 2.0 |
| ライマン公会堂 | Ryman Auditorium.jpg | Daniel Schwen, CC BY-SA 4.0 |
| ビール・ストリート | Beale Street Memphis TN.jpg | Nwdoty, CC BY-SA 4.0 |
| サン・スタジオ | Sun Records Studio, Memphis, Tennessee LCCN2010630851.tif(夜景) | Carol M. Highsmith, PD |
| ロレイン・モーテル | The Lorraine Motel, site of the Martin Luther King assassination and the National Civil Rights Museum..jpg | DavGreg, CC BY-SA 3.0 |
| オークリッジ | 1945-K-25-Plant-Aerial-Oak-Ridge-Tennessee.jpg | Ed Westcott(米エネルギー省), PD |
| ノリス・ダム | TVAs Norris hydroelectric dam (4403313816).jpg(章の図5と同一) | TVA Web Team, CC BY 2.0 |
| メンフィス国際空港 | FedEx Express Line Up (9300354100).jpg | Aeroprints.com, CC BY-SA 3.0 |

- 原画像の幅は全て1280px以上を確認(最小はロレインの2592px)。当初候補の「Nashville Skyline at Twilight.jpg」(927px)と「Memphis Beale Street.jpg」(1054px)は幅不足で不採用、ナッシュビルは章の図3と同じブロードウェイ夜景に差し替えた。
- サン・スタジオは章の図4(David Jones, 昼景, 1024px)が幅不足のため、地図はハイスミスの夜景(6494px, PD)を採用。.tifのサムネイルはAPIのthumburl(lossy-page1-500px-)をそのまま使用。
- クウォヒの「晴れれば160キロ先まで見えるという」はNPSの解説(100マイル超)に依る伝聞形。

## snaps の写真(5枚、写真ファーストで選定+ライセンス確認)

| 場所 | Commonsファイル | 作者 / ライセンス | 年代 |
|---|---|---|---|
| 紫の壁のホンキートンク | Tootsies Orchid Lounge - Nashville.jpg | Kathleen Conklin, CC BY 2.0 | いま |
| ホテルのロビーの鴨 | 20150521 The Peabody Hotel lobby and ducks (6).JPG | TonyTheTiger, CC BY-SA 4.0 | いま |
| ダム工事の昼休み | "A group of several hundred workers at Norris Dam construction campsite during noon hour." - NARA - 532733.jpg | Lewis Hine(米国立公文書館), PD | 1933年 |
| リンチバーグの広場 | Lynchburg tennessee square.jpg | nola.agent, CC BY 2.0 | いま |
| 国立公園の門前町 | Gatlinburg, Tennessee, viewed from the Gatlinburg SkyPark - 3.jpg | APK, CC BY 4.0 | いま |

- トゥーツィーズの「裏口がライマンの楽屋口の向かい」は同店・ライマン双方の沿革の周知の事実。ピーボディの鴨の行進は1933年から・毎日11時(ホテル公式)。ノリスの写真はルイス・ハインが1933年11月に撮影したTVA記録写真(NARA 532733)。
- スナップ選定の没: DOCUMERICAの炭鉱会社ピクニック(NARA 556529)は私人の顔の大写しのため不採用/Corky'sのネオン(場面が看板のみで弱い)/ネイランド・スタジアム(試合日でない外観で場面が読めない、市松模様の空撮は720pxで幅不足)。
- ピーボディはロビー全景(赤い制服のダックマスターと噴水と人垣)の一枚を採用し、鴨のアップ(Roger Schultz版)は場面が読めないため不採用。

## 検証

- `python3 site/build.py` 警告・エラーなし(16章)。
- `_site/` をHTTPサーバで開き、ヘッドレスChromiumで確認(2026-08-30)。CDN(unpkg)とタイルは実行環境のプロキシで遮断されるため、LeafletのJS/CSSはローカルに取得したものを、タイルとCommons画像はダミーにルーティングして機能を検証した(画像URL自体は全てHTTP 200と中身を別途確認済み):
  - 章ページに📍リンク12個。タップで地図パネルが開き、該当ピンに飛んで吹き出しが開く(ブリストルで確認、節番号「3節」表示も正しい)
  - チップ13個(全地名+先頭)で巡回可。注リンクの地名(ライマン公会堂=注9、空港=注22)のバッジ表示も正しい
  - 素の地図はピン12個、`?rich` でピン17個(places 12+snaps 5)。richの吹き出しに写真とクレジットが出る
  - モバイル幅(390px)でもパネル・吹き出しが動作(サン・スタジオで確認)
  - la.html など他章のリンク数・表示に影響なし。JSエラーなし
- 全画像URL(500pxサムネイル)はダウンロードで200と中身を確認。座標は各地点(ブリストルは州境の通り、リンチバーグは蒸留所、ノリスはダム堤体)に照合。
