# ノースカロライナ章の地図 検証記録(nc-check)

地図データは nc.json。作業手順は site/MAPS.md。紙面の編集用注記(text/usa/nc-check.md)とは別物で、こちらは地図(ウェブ版限定)の楽屋である。

## 経緯

- 2026-09-03 初版。章のマージ(PR #58)後の後工程として、同じセッションで作成。
- 章の軸(葉の遺産相続)に合わせ、places は煙草の来歴(キャズウェル郡・ウィルソン)、相続人の現在(ダーラム・ウィンストン・セーラム・シャーロット・クレイトン)、畑の後継(デュプリン郡・タールヒール村・シラーシティ)、地形の両端(アウターバンクス・ミッチェル山)と山の現在(アッシュビル)で12点。州内で完結する。
- プリンスヴィル(本文6節)は places でなく snaps(1999年のフロイド)で拾った。タールヒール村は良い現地写真がCommonsに無く、章の図4と同じラグーン写真(州東部)を「同じ一枚」と明記して使用。

## places の写真(12枚、ライセンスはCommons APIのextmetadataで確認、2026-09-03)

| 地名 | Commonsファイル | 作者 / ライセンス |
|---|---|---|
| ダーラム | American Tobacco Campus, Durham, NC (49160923068) cropped.jpg | Warren LeMay, CC0 |
| ウィンストン・セーラム | Winston-Salem skyline.jpg | Indy beetle, CC0 |
| シャーロット | Uptown Charlotte 2018 taking by DJI Phantom 4 pro - Perspective Corrected Edit.jpg | Precisionviews(補正: Cmao20), CC BY-SA 4.0 |
| アウターバンクス | Memorial from Flight Path, Wright Brothers National Memorial… (14443959961).jpg | Ken Lund, CC BY-SA 2.0 |
| ミッチェル山 | Mount Mitchell Summit Trail (March 2023).jpg | DiscoA340, CC BY-SA 4.0 |
| キャズウェル郡 | Caswell County Courthouse.jpg | Natalie Maynor, CC BY 2.0 |
| ウィルソン | ConDev8614A Tobacco auction in Wilson tobacco warehouse, 1951 (8476207944).jpg | ノースカロライナ州立公文書館, no known restrictions(1951年の州政府広報写真) |
| クレイトン | East Main Street, Clayton, North Carolina.jpg | Indy beetle, CC0 |
| デュプリン郡 | Courthouse square in Kenansville, North Carolina.jpg | Indy beetle, CC0 |
| タールヒール村 | NRCSNC00011 - North Carolina (5131)(NRCS Photo Gallery).tif | Bob Nichols(USDA NRCS), パブリックドメイン。章の図4と同じ写真。TIFのためサムネイルはAPIのthumburl(lossless-page1-500px-〜.tif.png)を使用 |
| シラーシティ | Mountaire Farms facility in Siler City, North Carolina.jpg | Indy beetle, CC0 |
| アッシュビル | Downtown Asheville, North Carolina 02.jpg | Harrison Keely, CC BY 4.0 |

## snaps の写真(5枚、写真ファーストで選定+ライセンス確認、2026-09-03)

| 場所 | Commonsファイル | 作者 / ライセンス | 年代 |
|---|---|---|---|
| ハーネット郡の煙草畑 | Tobacco field in Harnett County.jpg | Gerry Dincher, CC BY-SA 2.0 | いま |
| ダーラムの球場 | Durham Bulls Athletic Park Skyline.jpg | Sisipherr, CC BY-SA 4.0 | いま |
| ウィルソンの風車公園 | Whirligig Park, Wilson, North Carolina 08.jpg | Beyond My Ken, CC BY-SA 4.0 | いま |
| プリンスヴィル | FEMA - 1309 - Photograph by Dave Saville taken on 09-28-1999 in North Carolina.jpg | Dave Saville(FEMA), パブリックドメイン | 1999年 |
| アッシュ郡のツリー畑 | Christmas tree farm in Ashe County.jpg | Indy beetle, CC0 | いま |

- 全17枚の500pxサムネイルURLと、拡大用1280px版のURLがHTTP 200を返すことを確認(2026-09-03。数回の429はウィキメディアのレート制限で、間隔を空けた再試行で全て200)。原画像はいずれも幅1280px以上。全数を目視で確認し、text/rich/実況文を実画像に合わせて書いた。
- ウィルソンの1951年競り写真は州立公文書館のFlickr Commons由来で、ライセンス表示は「No restrictions」(著作権主張なし)。PD相当としてcreditにその旨を明記した。
- 没: シラーシティの市街写真(Siler101.jpg=1000px、Hadley.jpg=500px)は拡大要件(1280px)を満たさず、鶏肉工場の写真(CC0・3481px)に差し替え——章の筋にはむしろ合う。ミシシッピ章の教訓に倣い全数目視。デュプリンの豚舎そのものの写真はCommonsに適切なものが無く、ラグーン写真をタールヒール村側で使った。
- スナップの補足: ダーラムの球場の実況文(本塁打で雄牛の看板の目が光り鼻から煙)は球場の名物仕掛けの定型事実。風車公園はVollis Simpson(農機具修理業、2013年没)の作品群を市が公園化したもの(2017年開園)。

## 検証(2026-09-03)

- `python3 site/build.py` 警告・エラーなし(24章)。本文の地名12個すべてリンク化(data-i 0〜11が各1回)されることをビルド出力で確認。
- ブラウザ検証: リモート実行環境のため、MAPS.md 6節の但し書きに従い、curlでCDN(unpkgのLeaflet 1.9.4)と写真URLの到達性(HTTP 200)を確認した上で、PlaywrightのルーティングでLeafletをローカル退避コピーから供給し、地図タイル(carto/OSM/ArcGIS)と写真は1pxダミーに差し替えて実施。_site を http://127.0.0.1:8901 で配信(file:// ではない)。
- チェックリスト(デスクトップ1200pxとモバイル390pxの両方で実施、全22項目PASS、JSエラーなし):
  - [x] 地図パネルが開閉し、本文の📍地名タップで該当地点に飛んで吹き出しが開く(キャズウェル郡で確認)
  - [x] チップで全地名を順に回れる(13チップ=全体+12地名、12地名すべての吹き出しを確認)。ピンの節番号表示が正しい
  - [x] `?rich` で写真・クレジット・📷スナップピン(5本)が出る。写真タップで全画面拡大が動く
  - [x] モバイル幅でも上記が動く
  - [x] 他の章のページに影響がない(ミシシッピ章の地図 maps/usa-ms.html?rich が従来通り、ピン16本・JSエラーなし)
- 座標の特記: ダーラムはアメリカン・タバコ・キャンパス(35.9937, -78.9040)、アウターバンクスはライト兄弟記念碑(36.0183, -75.6678)、キャズウェル郡は郡都ヤンシービル、デュプリン郡は郡都ケナンズビル、シラーシティは町の中心(マウンテア工場は町の東)。スナップのダーラム球場(35.9919, -78.9046)はATCの隣で、ダーラムの📍ピンと重なって見えるのは実際の位置関係の通り。
