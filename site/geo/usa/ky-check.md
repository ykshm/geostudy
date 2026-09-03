# ケンタッキー章の地図 検証記録(ky-check)

地図データは ky.json。作業手順は site/MAPS.md。紙面の編集用注記(text/usa/ky-check.md)とは別物で、こちらは地図(ウェブ版限定)の楽屋である。

## 経緯

- 2026-09-03 初版。章(text/usa/ky.md、PR #60)のマージ後、依頼者の指示で後工程として作成。

## places の写真(12枚、ライセンスはCommons APIのextmetadataで確認、2026-09-03)

| 地名 | Commonsファイル | 作者 / ライセンス |
|---|---|---|
| チャーチルダウンズ競馬場 | Twin Spires at Churchill Downs.jpg | JazzyJoeyD, CC BY-SA 4.0 |
| バーズタウン | Federal Hill mansion (1795) at My Old Kentucky Home State Park, Bardstown KY.jpg | Calstanhope, CC BY-SA 4.0 |
| マンモス・ケーブ | Passage, Mammoth Cave, Mammoth Cave National Park, Mammoth Cave, KY.jpg | w_lemay, CC BY-SA 2.0 |
| レキシントン | Horse farm, Lexington, Kentucky LCCN2010630483.tif | Carol M. Highsmith, パブリックドメイン |
| ロージン | Rosine General Store NRHP 03000708 Ohio County, KY.jpg | Jon Roanhaus, CC BY-SA 4.0 |
| ハーラン郡 | Coal camp children. Dixie Darby Fuel Company, Marne Mine, Lejunior... - NARA - 541323.jpg | Russell Lee, パブリックドメイン |
| ミューレンバーグ郡 | Paradise Fossil Plant.jpg | TVA, パブリックドメイン |
| ホワイツバーグ | Webb and Main in Whitesburg.jpg | Nyttend, パブリックドメイン |
| バッチャー・ホロウ | Loretta Lynn house.jpg | Dennis Adams(FHWA), パブリックドメイン |
| ルイビル | Louisville Panorama.jpg | Anindya Chakraborty, CC BY 3.0 |
| ジョージタウン | Georgetown Kentucky Toyota (2023-06-05-04-15-00 UMBRA-06, 25-cm).tiff | Umbra Lab, CC BY 4.0 |
| コービン | The Home of Kentucky Fried Chicken (53247186898).jpg | Bill McMannis, CC BY 2.0 |

- ジョージタウンはレーダー衛星(SAR)画像で、白黒の夜間撮像。工場の屋根の白い塊が畑の中に浮かぶ絵として採用し、richの一言でレーダー衛星と明記した。
- 没(拡大要件1280px未満): Main Street in Whitesburg(859px)→Webb and Mainに差し替え/Toyota visitor center(640px)→UMBRA衛星画像に差し替え/Louisville skyline night(1024px)→Panoramaに差し替え/Donamire Farm(820px)。

## snaps の写真(6枚、同日に目視選定+ライセンス確認)

| 場所 | Commonsファイル | 作者 / ライセンス | 年代 |
|---|---|---|---|
| ラビット・ハッシュ | Rabbit Hash General Store, Rabbit Hash, KY.jpg | w_lemay, CC BY-SA 2.0 | いま |
| ルイビルの下町 | Shotgun houses on S 5th St.jpg | LJOHN04, パブリックドメイン | いま |
| ハザード | Downtown Hazard, Kentucky (on Main Street).jpg | Appbirdky, CC BY-SA 4.0 | いま |
| 州フェアの投げ縄 | 2008 Kentucky State Fair Roping Show (2765926132).jpg | Heather Moreton, CC BY 2.0 | 2008年 |
| ウィグワムの宿 | Marion Post Wolcott, Indian teepee cabins for tourists south of Bardstown, Kentucky, 1940.jpg | Marion Post Wolcott(FSA), パブリックドメイン | 1940年 |
| クローバー・ギャップ炭鉱の売店 | Miners and their families gather around the community store and office. P V & K Coal Company, Clover Gap Mine... - NARA - 541327.jpg | Russell Lee, パブリックドメイン | 1946年 |

- 全18枚の500pxサムネイルURLと拡大用1280px版URLがHTTP 200を返すことを確認(2026-09-03。途中の429はウィキメディアのレート制限で、間隔を空けた再試行で全て解決)。原画像はいずれも幅1280px以上。スナップ6枚と主要places写真は目視で確認し、text/rich/実況文を実画像に合わせて書いた。
- サムネイルのハッシュパス(/thumb/X/XX/)を推測で書いた2枚(ハザード・州フェア)が404になり、APIのthumburlで訂正した——thumburlをそのまま使うのが確実(MAPS.md 5節の通り)。
- ラビット・ハッシュの「村長は犬」は同村の名物選挙(1998年から続く寄付集めの犬村長)の定型事実。ウィグワムの宿はWolcottの原題どおり「バーズタウン南」に置いた(ケーブシティに現存するウィグワム・ビレッジ2号とは別の初期店舗)。
- 昔の写真は2枚(1940・1946)で「現代中心+昔1〜2枚」の範囲。2008年の州フェアはeraに年を明記した。

## 検証(2026-09-03)

- `python3 site/build.py` 警告・エラーなし(25章)。本文の地名12個すべてリンク化(data-i 0〜11が各1回)されることを生成HTMLのgrepで確認。
- ブラウザ検証: リモート実行環境のため、MAPS.md 6節の但し書きに従い、curlでCDN(unpkgのLeaflet 1.9.4)と写真URLの到達性を確認した上で、PlaywrightのルーティングでLeafletをローカル退避コピーから供給し、地図タイル(ArcGIS/carto/OSM)と写真は1pxダミーに差し替えて実施。_site を http://127.0.0.1:8901 で配信(file:// ではない)。
- チェックリスト(デスクトップ1200pxとモバイル390pxの両方で実施、全28項目PASS、JSエラーなし):
  - [x] 地図パネルが開閉し、本文の📍地名タップで該当地点に飛んで吹き出しが開く(ハーラン郡で確認)
  - [x] チップで全地名を順に回れる(13チップ=全体+12地名、12地名すべての吹き出しと節番号表示を確認)
  - [x] `?rich` で写真・クレジット・📷スナップピン(6本)が出る。写真タップの全画面拡大は章末おまけのiframe経由で動作確認(全画面表示は親ページのmap-panel.jsが担うため、地図単体ページでは発火しない——仕様通り)
  - [x] モバイル幅でも上記が動く
  - [x] 他の章のページに影響がない(ミシシッピ章 maps/usa-ms.html?rich が従来通りピン16本・JSエラーなし)
- 座標の特記: バーズタウンは屋敷フェデラル・ヒル(37.8072, -85.4536)、ミューレンバーグ郡はパラダイス発電所跡(37.2589, -86.9803)、ジョージタウンはTMMK工場(38.2456, -84.5217)、コービンはサンダース・カフェ(36.9539, -84.1044)、バッチャー・ホロウはヴァンリア東の谷(37.7601, -82.7413)。スナップのクローバー・ギャップ売店はハーラン郡リジュニア付近の概値(36.8642, -83.1418)で、ハーラン郡の📍ピンと谷続きに見えるのは実際の位置関係の通り。ウィグワムの宿はバーズタウン南の国道31E沿いの概値(37.75, -85.47)。
