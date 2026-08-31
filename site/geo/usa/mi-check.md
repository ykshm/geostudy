# ミシガン章の地図 検証記録(mi-check)

地図データは mi.json。作業手順は site/MAPS.md。紙面の編集用注記(text/usa/mi-check.md)とは別物で、こちらは地図(ウェブ版限定)の楽屋である。

## 経緯

- 2026-08-26 初版。places 13(章の本文順)+ snaps 6。
- テンプレート(site/maps/template.html)に小さな一般化を1点: 米国外ピンの色分けが `mx` 決め打ちだったのを、`ca`(カナダ)にも効くようにした(`.pin.mx, .pin.ca` に同色を適用、チップのclassは `p.side` をそのまま使用)。既存章(tx の `mx`)の挙動は不変なことをブラウザ検証で確認。

## places の写真(13枚、ライセンスはCommons APIのextmetadataで確認、2026-08-26)

| 地名 | Commonsファイル | 作者 / ライセンス |
|---|---|---|
| マキノー海峡 | Mackinac Bridge from the air3.jpg | Justin Billau, CC BY 2.0(章の図2と同じ) |
| キウィーノー半島 | Quincy Mine No. 2 Shaft-Rockhouse.jpg | Diane Dahlstrom, CC BY-SA 4.0 |
| マーケット | Upper Harbor aka Presque Isle ore dock, Marquette, MI - 2016 - 1.jpg | The ed17, CC BY-SA 4.0 |
| スーの閘門 | Freighter travelling through the Soo Locks (14658981350).jpg | NOAA GLERL, CC BY-SA 2.0(章の図3と同じ) |
| デトロイト | Detroit Skyline (Nov2021).jpg | Lrgjr72, CC BY-SA 4.0 |
| ランシング | Michigan State Capitol, Capitol Avenue, Lansing, MI - 54383125191.jpg | w_lemay, CC BY-SA 2.0 |
| ハイランドパーク | Ford Highland Park Manufacturing Plant, Highland Park, Michigan - 20201213.jpg | Andre Carrotflower, CC BY-SA 4.0 |
| フリント | Vehicle City Arches.jpg | Alberryii, CC BY-SA 4.0 |
| バトルクリーク | Battle Creek, Michigan (2008).jpg | battlecreekcvb, CC BY 2.0 |
| ヒッツヴィルU.S.A. | Detroit December 2025 18 (Hitsville U.S.A.).jpg | Michael Barera, CC BY-SA 4.0(章の図5と同じ) |
| ミシガン・セントラル駅 | Detroit December 2025 06 (Michigan Central Station).jpg | Michael Barera, CC BY-SA 4.0(章の図6と同じ) |
| マーシャル | Brooks Memorial Fountain - Forsythe 2.jpg | Forssa01, CC BY 4.0 |
| ウィンザー | Windsor skyline from the Detroit Riverfront.jpg | パブリックドメイン |

## snaps の写真(6枚、写真ファーストで目視選定+ライセンス確認、2026-08-26)

| 場所 | Commonsファイル | 作者 / ライセンス | 年代 |
|---|---|---|---|
| イースタン・マーケット | Detroit May 2023 03 (Eastern Market).jpg | Michael Barera, CC BY-SA 4.0 | いま |
| ダウンタウンの二軒 | Detroit December 2015 34 (Lafayette Coney Island and American Coney Island).jpg | Michael Barera, CC BY-SA 4.0 | いま |
| ハムトラミック | Jos Campau at Norwalk - Hamtramck MI.JPG | Andrew Jameson, CC BY-SA 3.0 | いま |
| ホートン湖 | Ice Fishing Shanties on Houghton Lake, Michigan during Tip-Up Town Weekend (6778351105).jpg | Joe Ross, CC BY-SA 2.0 | いま |
| カルメット | CALUMET MICHIGAN DSC01842.JPG | Catatonique, CC BY-SA 3.0 | いま |
| ウッドワード大通り | Woodward Ave Detroit 1942.jpg | Arthur S. Siegel(OWI), パブリックドメイン | 1942年 |

- 全点、原画像の幅1280px以上を確認(最小はカルメットの1280px)。URLはすべて500px標準サムネイル(APIのthumburlから取得)で、HTTP 200を全数確認。
- 見送り: パスティの店・チェリー農園・ウィローラン工場(1943)は、条件に合う良い写真がCommonsに見つからず、スナップを置かなかった(MAPS.md 7節の方針通り)。

## 座標・記述の特記

- キウィーノー半島はクインシー鉱山(写真の場所)、マーシャルはブルックス記念噴水、ヒッツヴィルは西グランド大通り2648番地、ウッドワード大通りのスナップは撮影方向のミッドタウン付近に置いた。
- ウィンザーは `side: "ca"`(今回一般化した色分け)。

## ブラウザ検証(2026-08-26、Playwright + ローカルHTTPサーバ)

自動テスト24項目すべて合格。サンドボックスの都合で unpkg(Leaflet)・タイル・Commons画像はローカルに取得した実物で差し替えて供給した(サイト側のコードは無改変で検証)。

- [x] 章ページに📍リンク13個。タップで地図パネルが開き、該当地点の吹き出しが開く
- [x] チップ14個(全体+13)で全地名を巡回、ピンの節番号表示が正しい(エラーなし)
- [x] ウィンザーのピンに `.ca` が付き、対外色(赤系)で描画される
- [x] `?rich` で写真・クレジット・📷スナップピン6個。写真タップで全画面拡大(1280px版への差し替え)が動く
- [x] モバイル幅(390px)でもパネルとリンクが動く
- [x] 他章に影響なし(tx: リンク10個・パネル・`mx` ピンの色が従来通り、トップページ7章)
