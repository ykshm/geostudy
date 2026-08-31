# ニューヨーク章の地図 検証記録(ny-check)

地図データは ny.json。作業手順は site/MAPS.md。紙面の編集用注記(text/usa/ny-check.md)とは別物で、こちらは地図(ウェブ版限定)の楽屋である。

## 経緯

- 2026-08-26 初版。章(text/usa/ny.md)のマージ後の後工程として作成。places 12 + snaps 7。

## places の写真(12枚、ライセンスはCommons APIのextmetadataで確認、2026-08-26)

| 地名 | Commonsファイル | 作者 / ライセンス |
|---|---|---|
| ナイアガラの滝 | American and Bridal Veil Falls winter.jpg | The Cosmonaut, CC BY-SA 2.5 |
| オールバニ | 2019 New York State Capitol northwest facade, Albany, New York.jpg | Beyond My Ken, CC BY-SA 4.0 |
| モホーク川の谷 | View of the canal, at the Little Falls Mohawk River.jpg | William Guy Wall, パブリックドメイン(19世紀前半の版画) |
| 自由の女神 | Statue of Liberty frontal 2.jpg | パブリックドメイン(撮影者による提供) |
| ウォール街 | New York Stock Exchange August 2017 02.jpg | Arild Vågen, CC BY-SA 4.0 |
| エリス島 | Main building, Ellis Island NY.jpg | David Brossard, CC BY-SA 2.0 |
| ロウアー・イーストサイド | 97 Orchard Street Front.jpg | Fletcher6, CC BY-SA 3.0 |
| クイーンズ区 | Jackson Hts Roosevelt Av td (2019-08-21) 11 - 74th Street IRT.jpg | Tdorante10, CC BY-SA 4.0 |
| エンパイア・ステート・ビル | View of Empire State Building from Rockefeller Center New York City dllu.jpg | Dllu, CC BY-SA 4.0 |
| セントラルパーク | Manhattan, Central Park (5351029043).jpg | Bill Abbott, CC BY-SA 2.0 |
| バッファロー | Buffalo December 2024 44 (Buffalo City Hall).jpg | Michael Barera, CC BY-SA 4.0 |
| シラキュース | Syracuse, New York skyline.jpg | Quintin Soloviev, CC BY 4.0 |

- リンク先の節/注: バッファローは本文2節にも出るが、話の本体である6節にリンクを付けた(リンク化は指定の節の初出1回)。クイーンズは本文の「クイーンズ区」の表記に一字一句合わせた。
- 座標の特記: モホーク川の谷はリトルフォールズ(壁の切れ目の当の場所)。ロウアー・イーストサイドはオーチャード通り97番地(テネメント博物館)。クイーンズ区は74丁目駅(ジャクソンハイツ)。

## snaps の写真(7枚、同日に目視選定+ライセンス確認)

| 場所 | Commonsファイル | 作者 / ライセンス | 年代 |
|---|---|---|---|
| ジャクソンハイツ | Roosevelt-avenue-queens-nyc cars driving-under-elevated-railway-line 1980s.jpg | RickDikeman提供, CC0 | 1980年代 |
| モット通り | Mott Street, Chinatown, New York-L1002097.jpg | Frank Schulenburg, CC BY-SA 4.0 | いま |
| ジャマイカ(クイーンズ) | Shah's halal food cart 20181010 111456.jpg | CaptJayRuffins, CC BY-SA 4.0 | いま |
| ブライトンビーチ | Brighton Cell Phones.jpg | Eden, Janine and Jim, CC BY 2.0 | いま |
| バッファロー・ウェストサイド | Car buried under snow, West Ferry Street, Buffalo, New York - 20220118.jpg | Andre Carrotflower, CC BY-SA 4.0 | いま |
| アムステルダム | Laundromat in Amsterdam, New York.jpg | CapitalRegion, CC BY-SA 4.0 | いま |
| ブッシュウィック | INNER CITY RESIDENTS OF BROOKLYN ... - NARA - 555927.jpg | Danny Lyon / EPA(DOCUMERICA), パブリックドメイン | 1974年 |

- 座標の根拠: ジャマイカ・バッファロー雪・モット通り・ブライトンビーチはCommonsのファイル座標。アムステルダムは説明文の「Lark St と E Main St の角」から。ブッシュウィックはブッシュウィック・アベニュー沿いの概略位置(原典に正確な座標なし)。ジャクソンハイツは高架下のルーズベルト・アベニュー(82丁目付近の概略)。
- スナップ選定の没: Jackson Heights 1.jpg(場面は良いがCC BY 2.5で作者表記の情報がCommonsに無く、表示要件を満たせない)、Flushing Main Street.jpg(LIRRホームの写真で場面が弱い)、ブライトンビーチの海岸通りパノラマ(人が少なく場面が弱い)、ロックポートの閘門(生活の場面というより土木の名所)、バッテリーパークの子どもたち1973(昔枠は2枚までの方針でブッシュウィックを優先)、74丁目駅の駅名標(凡庸)。

## 検証(2026-08-26)

- python site/build.py: 警告・エラーなし(10章)。12地名すべてリンク化された(未リンクの地名はビルドが警告する仕組み)。
- 全19枚の500pxサムネイルURLは、取得(HTTP 200)と目視で確認。原画像はいずれも幅1280px以上(拡大表示に対応)。URLはAPIのthumburlをそのまま使用。
- _site/ をHTTPサーバで開き、Chromium(Playwright)で確認:
  - 本文の📍地名タップでパネルが開き、該当地点の吹き出しが開く(エンパイア・ステート・ビルで確認。ピンに節番号のバッジ)
  - チップで地名を回れる(6節バッファローへの遷移と吹き出しを確認)
  - ?rich で📷スナップピン7本と写真・年代チップ・クレジットの吹き出し、写真タップの全画面拡大が動く
  - モバイル幅(390px)でもパネル・吹き出しが動く(エリス島で確認)
  - 他章に影響なし(テキサス章の地名リンク10個と地図が従来通り)
  - 特記: この検証環境はネットワークが代理サーバ経由でヘッドレスブラウザから外部CDNに届かないため、Leaflet本体・地図タイル・写真はローカルに差し替えて機能を検証した(実URLの生死は上記の通りcurlで確認済み)。実環境での見た目の最終確認はPages反映後に行える。
