# マサチューセッツ章の地図 検証記録(ma-check)

地図データは ma.json。作業手順は site/MAPS.md。紙面の編集用注記(text/usa/ma-check.md)とは別物で、こちらは地図(ウェブ版限定)の楽屋である。

## 経緯

- 2026-08-30 初版。章(text/usa/ma.md)のマージ後の後工程として作成。places 12(うち注ピン3: スプリングフィールド=注2、クワビン貯水池=注8、ロウエル=注17)、snaps 6。

## places の写真(12枚、ライセンスはCommons APIのextmetadataで確認、2026-08-30)

| 地名 | Commonsファイル | 作者 / ライセンス |
|---|---|---|
| ケープコッド | Marconi Beach.jpg | \|vv@ldzen\|, CC BY 2.0 |
| スプリングフィールド | Naismith Memorial Basketball Hall of Fame (Springfield, MA).jpg | Quintin Soloviev, CC BY 4.0 |
| プリマス | Mayflower at Twilight - Plymouth, Massachusetts, USA - August 13, 2015 01.jpg | Giorgio Galeotti, CC BY 4.0 |
| バックベイ | Commonwealth Avenue Mall, Boston MA.jpg | John Phelan, CC BY 4.0 |
| クワビン貯水池 | Quabbin Reservoir, Massachusetts.jpg | Solarapex, CC BY 2.5 |
| ノースエンド | North Bennett Street, looking north towards Salem Street, North End, Boston (8272168865).jpg | Boston City Archives(1920年ごろ・市計画委員会撮影), CC BY 2.0 |
| ドーチェスター | Triple-decker porches on Rosseter Street, Dorchester, July 2013.JPG | Pi.1415926535, CC BY-SA 4.0(章の図3と同じ写真) |
| ウェストエンド | The West End Branch Library in Boston.jpg | Internet Archive Book Images(1910年代の移民向け手引き書の図版), 制限なし |
| ロウエル | Boott Cotton Mills complex, Lowell, Massachusetts LCCN2011631235.tif | Carol M. Highsmith, パブリックドメイン(.tifのためAPIのthumburl「lossy-page1-500px-…」形式を使用) |
| ローレンス | The Duck Bridge & Ayer Mill Lawrence, Massachusetts.jpg | PerriAndMe, CC BY-SA 4.0 |
| ケンドール・スクエア | Kendall Square neighborhood, Cambridge, Massachusetts.jpg | Kenneth C. Zirkel, CC BY 4.0 |
| ミルトン | Mattapan Trolley 3260 near Milton Oct 2024 1.jpg | 4300streetcar, CC BY 4.0 |

## snaps の写真(6枚、同日に目視選定+ライセンス確認)

| 場所 | Commonsファイル | 作者 / ライセンス | 年代 |
|---|---|---|---|
| ネプチューン通り(イーストボストン) | NEAR LOGAN AIRPORT-AIRPLANE COMING IN FOR A LANDING OVER NEPTUNE ROAD HOMES - NARA - 548448.jpg | Michael Philip Manheim / EPA(DOCUMERICA), PD | 1973年 |
| ヘイマーケット | Haymarket Boston vendors and customers.JPG | Daniel Brody, CC BY-SA 4.0 | いま |
| パイリン・プラザ(ロウエル) | Pailin Plaza; Lowell, MA; 2011-12-08.JPG | Emw, CC BY-SA 3.0 | いま |
| ケープコッドの街角 | Dunkin' Donuts storefront.jpg | Connor Williams, CC BY 2.0 | いま |
| プロビンスタウン | Commercial Street, looking west, Provincetown, Mass (70263).jpg | Tichnor Bros. Inc.(ボストン公共図書館蔵の絵はがき), PD | 1930〜40年代 |
| エヴェレット | MBTA route 110 bus turning off Chelsea Street in Everett MA June 2026.jpg | 4300streetcar, CC BY 4.0 | いま |

- 全18枚の500pxサムネイルURLがHTTP 200を返し、実体をダウンロードして目視確認(2026-08-30)。原画像はいずれも幅1280px以上(拡大表示に対応)。
- 座標の特記: 「ケープコッドの街角」のダンキンは、Commonsの記載が「Cape Cod, Massachusetts」までで町が特定できないため、ピンは半島の中心の町ハイアニスに概置した(実況文も町名を断定しない書き方)。ケープコッドの地名ピンは写真の撮影地マルコーニ・ビーチ(ウェルフリート)に置いた。ミルトンはマタパン線ミルトン駅(ロウアーミルズ)に置いた——MBTAコミュニティーズ法の文脈のため。
- スナップ選定の没: 2017 Ciclovia(ローレンス、原画像640pxで拡大要件を満たさず)、Commercial Street panoramio(プロビンスタウン現代、1024pxで同上)、Salem Street North End(1063pxで同上)、「アルストンのクリスマス」の路上家具写真(Commonsに適品なし)。
- ブラウザ確認(2026-08-30、_siteをHTTPサーバで配信しChromium+Playwrightで確認): 章ページに📍リンク12個が付き、タップで地図パネルが開閉して該当地点に飛び吹き出しが開く/チップ(全体+18)で順に回れ、ピンの節・注番号表示が正しい/?richで写真・クレジット・📷スナップピン6本が出る/素の地図はピン12本でスナップなし/モバイル幅(390px)でも動作/他章(ny.html)への影響なし/JSエラーなし。注記: この実行環境のプロキシはブラウザからのCDN・タイル・Commonsへの接続を遮断するため、Leafletのみローカル複製に差し替えた生成物で動作を確認し(正本・テンプレートは無改変)、確認後にビルドし直して差し替えを破棄した。写真の表示自体は上記のURL取得(HTTP 200+目視)で確認している。
