# テキサス章の地図 検証記録(tx-check)

地図データは tx.json。作業手順は site/MAPS.md。紙面の編集用注記(text/usa/tx-check.md)とは別物で、こちらは地図(ウェブ版限定)の楽屋である。

## 経緯

- 2026-08-25 初版。claude.ai上で依頼者と検討した設計(地図パネル+地名リンク+章末おまけ)をデプロイ指示書に基づき実装。
- 同日、依頼者のフィードバックで(1)ストリートビューのリンクを削除、(2)「暮らしのスナップ」ピン(写真ファースト・観光地でない生活の場面・現代中心+昔1〜2枚)を追加、(3)写真タップの全画面拡大を追加。
- 同日、地図をテンプレート(site/maps/template.html)+章別JSON(tx.json)の構成に移行。挙動不変をブラウザ自動テスト38項目で確認。

## places の写真(10枚、ライセンスはCommons APIのextmetadataで確認、2026-08-25)

| 地名 | Commonsファイル | 作者 / ライセンス |
|---|---|---|
| スピンドルトップ | Lucas gusher.jpg | パブリックドメイン(1901) |
| ヒューストン | Downtown Houston, TX Skyline - 2018.jpg | David Daniel Turner, CC BY 4.0 |
| ロスコー | Roscoe Wind Farm in West Texas.jpg | Matthew T Rader, CC BY-SA 4.0 |
| サンアントニオ | River Walk Reflections.jpg | Corey Leopold, CC BY 2.0 |
| アマリロ | Cadillac Ranch in Texas.jpg | DiscoA340, CC BY-SA 4.0 |
| エルパソ | El Paso Ciudad Juarez (16605799972).jpg | Kurt Bauschardt, CC BY-SA 2.0 |
| シウダーフアレス | Paso Del Norte POE El Paso Texas (27794615593).jpg | U.S. CBP, パブリックドメイン |
| オースティン | Downtown Austin Skyline - Ann W. Richards Congress Avenue Bridge (54987518915).jpg | ajay_suresh, CC BY 4.0 |
| ロックハート | Kreuz market, lockhart texas www.kreuzmarket.com - panoramio.jpg | Dameon Hudson, CC BY 3.0 |
| ダラス | Dallas Skyline at Dusk.jpg | Matthew T Rader, CC BY-SA 4.0 |

## snaps の写真(7枚、同日に目視選定+ライセンス確認)

| 場所 | Commonsファイル | 作者 / ライセンス | 年代 |
|---|---|---|---|
| マグレガー | Creative display of the local high school's football team schedule ... LCCN2015630949.tif | Carol M. Highsmith, PD | いま |
| ウェスト | West June 2016 16 (The Best Donut and Kolache Shop).jpg | Michael Barera, CC BY-SA 4.0 | いま |
| バーネット | Dairy Queen, Burnet, TX IMG 2000.JPG | Billy Hathorn, CC BY-SA 3.0 | いま |
| ダラス・オーククリフ | Oak Cliff September 2016 28 (Taqueria Pedrito and Las Ranitas).jpg | Michael Barera, CC BY-SA 4.0 | いま |
| ルイーズ | A grain elevator in the town of Louise, Texas LCCN2014631059.tif | Carol M. Highsmith, PD | いま |
| ヒューストン航路 | FREIGHTER MOVES SLOWLY UP THE HOUSTON SHIP CHANNEL AS GIRLS FISH FROM THE SHORE... - NARA - 550941.jpg | Blair Pittman / EPA(DOCUMERICA), PD | 1972年 |
| エルパソ下町 | FIFTH AND MESA IN THE SECOND WARD. EL PASO'S "BARRIO" - NARA - 545356.jpg | Danny Lyon / EPA(DOCUMERICA), PD | 1972年 |

- 全17枚の500pxサムネイルURLがHTTP 200を返すことを確認(2026-08-25)。原画像はいずれも幅1280px以上(拡大表示に対応)。
- スナップ選定の没: Upshot-Knothole系のNTS写真(章の図4と重複)、Desert Rock演習の兵士写真(人物中心)、フリオ川の若者たち1972(昔枠は2枚までの方針)、Vidor のDQ(バーネットの方が場面が良い)、Jacksonville の屋台公園(ウェストのコラーチ屋の方が場面が良い)。
