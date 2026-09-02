# ミシシッピ章の地図 検証記録(ms-check)

地図データは ms.json。作業手順は site/MAPS.md。紙面の編集用注記(text/usa/ms-check.md)とは別物で、こちらは地図(ウェブ版限定)の楽屋である。

## 経緯

- 2026-09-02 初版。章のマージ(PR #50)後の後工程として作成。
- 章の軸(録音地と生まれのずれ)に合わせ、places に州外の録音地3点(グラフトン=ウィスコンシン、サンアントニオ=テキサス、シカゴ=イリノイ)を含めた。地図が自動で広域にズームアウトし、デルタと録音地の距離がそのまま見える。

## places の写真(12枚、ライセンスはCommons APIのextmetadataで確認、2026-09-02)

| 地名 | Commonsファイル | 作者 / ライセンス |
|---|---|---|
| ストーヴァル農園 | Muddy Waters Cabin.jpg | Bobpalez, CC BY-SA 4.0 |
| クラークスデイル | Ground Zero Blues Club.jpg | Natalie Maynor, CC BY 2.0 |
| ドッカリー農場 | Dockery Farms, Sunflower County, MS.JPG | The old perfesser, CC BY-SA 3.0 |
| グラフトン | Paramount Records Blues Trail Marker.jpg | Firecruise, CC BY-SA 4.0 |
| サンアントニオ | Sheraton Gunter Hotel.jpg | intenteffect, CC BY-SA 2.0 |
| グリーンヴィル | 1927 Mississippi Flood Greenville Mississippi.jpg | NOAA所蔵, パブリックドメイン(1927) |
| パーチマン | Parchman prison convict labor 1911.jpeg | パブリックドメイン(1911) |
| シカゴ | Chess Records (2639758382).jpg | Reading Tom, CC BY 2.0 |
| メリディアン | Jimmie Rodgers Museum Highland Park.JPG | Dudemanfellabra, CC BY-SA 3.0 |
| テューペロ | Elvis Presley Birthplace, Tupelo, MS, US.jpg | Bubba73, CC BY-SA 3.0 |
| マネー | EmmettTillStoreMoneyMS.JPG | WhisperToMe, パブリックドメイン |
| インディアノーラ | BB King Museum and Delta Interpretive Center in Indianola, Mississippi showing the cotton gin.jpg | Swampyank, CC BY-SA 3.0 |

## snaps の写真(4枚、目視選定+ライセンス確認、2026-09-02)

| 場所 | Commonsファイル | 作者 / ライセンス | 年代 |
|---|---|---|---|
| メリゴールド郊外 | Po Monkeys Juke Joint.jpg | Bobpalez, PD | いま |
| クラークスデイル・サンフラワー通り | Red's Lounge exterior in Clarksdale.png | Roger Hsu, CC BY 2.0 | いま |
| マネーのガソリンスタンド | Ben Roy Service Station.jpg | Deisenbe, CC BY-SA 4.0 | いま |
| クラークスデイル郊外のジューク・ジョイント | FSA Dancing JukeJoint.jpg | Marion Post Wolcott(FSA), PD | 1939年 |

- 全16枚の500pxサムネイルURLがHTTP 200を返すことを確認(2026-09-02)。原画像はいずれも幅1280px以上(拡大表示に対応)。全16枚を目視で確認し、実況文・説明文を実画像に合わせて書いた。
- スナップ選定の没: FEMAのビロクシ漁港写真(2006年、カトリーナ後の聞き取り場面)は場面が良かったが、現代の私人の顔が大写しのため不採用。湾岸(ビロクシ)の代替は「Fishing Fleet in Biloxi」(194px・小さすぎ)しか見つからず、方針(良い写真がなければ置かない)に従い湾岸のスナップは置かなかった。ベルゾーニ(ナマズ)・リーランド(カーミット)も適切なフリー写真が見つからず見送り。1939年のジッターバグ写真はLOC由来の複数版のうち、幅12,616pxの高解像度版(FSA Dancing JukeJoint.jpg)を採用(954px版・1024px版は拡大要件を満たさないため不採用)。
- メリディアンの写真は当初「Train Monument…」(960px)を予定したが拡大要件を満たさず、1280pxの博物館全景に差し替え。グリーンヴィルは現代の街の写真が見つからず(Washington Avenue Greenville.jpg は741px)、章の図4と同じ1927年洪水の空撮(1621px・PD)を使用し、その旨を説明文に書いた。紙面図版で当初候補の1枚が油絵と判明した教訓に倣い、地図の写真も全数を目視した。

## 検証(2026-09-02)

- `python3 site/build.py` 警告・エラーなし(20章)。本文の地名12個すべてリンク化されることをビルドとブラウザで確認。
- ブラウザ検証: リモート実行環境のため、MAPS.md 6節の但し書きに従い、curlでCDN(unpkgのLeaflet)と写真URL(upload.wikimedia.org)の到達性(HTTP 200)を確認した上で、PlaywrightのルーティングでLeafletをローカル退避コピー(curlで取得したleaflet@1.9.4)から供給し、地図タイルと写真は1pxダミーに差し替えて実施。_site を http://127.0.0.1:8901 で配信(file:// ではない)。
- チェックリスト(デスクトップ1200pxとモバイル390pxの両方で実施、全31項目PASS):
  - [x] 地図パネルが開閉し、本文の📍地名タップで該当地点に飛んで吹き出しが開く(グリーンヴィルで確認)
  - [x] チップで全地名を順に回れる(13チップ)。ピンの節番号表示が正しい
  - [x] `?rich` で写真・クレジット・📷スナップピン(4本)が出る。写真タップで全画面拡大が動く
  - [x] モバイル幅でも上記が動く
  - [x] 他の章のページに影響がない(テキサス章の地図 maps/usa-tx.html?rich が従来通り動作、ピン17本・JSエラーなし)
- 座標の特記: ストーヴァル農園は案内板の立つ小屋跡(34.2623, -90.6595)、シカゴは市中心でなく南ミシガン通り2120番地のチェスのスタジオ跡(41.8543, -87.6237)、マネーはブライアント雑貨店の廃墟(33.6535, -90.2039)に置いた。
