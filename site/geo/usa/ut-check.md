# ユタ章の地図 検証記録(ut-check)

地図データは ut.json。作業手順は site/MAPS.md。紙面の編集用注記(text/usa/ut-check.md)とは別物で、こちらは地図(ウェブ版限定)の楽屋である。

## 経緯

- 2026-09-03 初版。章のマージ後、依頼者の指示で後工程として作成。places 12(本文の筋の地名、登場順。節リンク11・注リンク1)+ snaps 5(現代4・1972年1)。extras は置いていない(アメリカ50州では任意)。

## places の写真(12枚、ライセンスはCommons APIのextmetadataで確認、2026-09-03)

| 地名 | Commonsファイル | 作者 / ライセンス |
|---|---|---|
| ソルトレークシティ | Salt Lake City skyline (2020) from Ensign Peak.jpg | Iansmh98, CC BY-SA 4.0 |
| マグナ | Magna, Utah (2018).jpg | Nicolas Henderson, CC BY 2.0 |
| アルタ | Alta Little Cottonwood Canyon.JPG | Baileypalblue, パブリックドメイン |
| レッドロック峠 | RedRockPassIdaho071710.JPG | Wilson44691, パブリックドメイン |
| ボンネビル・ソルトフラッツ | Bonneville Salt Flats (17235453660).jpg | 米土地管理局, パブリックドメイン |
| グレートソルト湖 | 2012.10.01.103755 Great Salt Lake Antelope Island Utah.jpg | Hermann Luyken, CC0 |
| スパイラル・ジェッティ | Spiral jetty winter 2020.jpg | Sanjuro noname, CC BY-SA 4.0 |
| グースネックス | Goosenecks State Park, March 2019.jpg | Steven Baltakatei Sandoval, CC BY-SA 4.0(章の図5と同一) |
| アーチーズ国立公園 | USA 10400 Arches National Park Luca Galuzzi 2007.jpg | Luca Galuzzi, CC BY-SA 2.5 |
| パウエル湖 | Lac Powell 2016 (from plane) view on the bathtub ring (1).JPG | Pierre André, CC BY-SA 4.0 |
| プロモントリー | East and West Shaking hands at the laying of last rail Union Pacific Railroad - Restoration.jpg | Andrew J. Russell, パブリックドメイン |
| ビンガムキャニオン銅山 | 2019 Bingham Canyon Mine 04.jpg | Farragutful, CC BY-SA 4.0(章の図6と同一) |

- スパイラル・ジェッティは2020年冬の低水位時の一枚を選び、「干上がった湖底の水位計」という本文の記述と場面を一致させた。
- パウエル湖は、岩壁の白い縁取り(バスタブリング)で低水位が読める空撮を選んだ。
- ボンネビル・ソルトフラッツの候補にあったスピードウェイの空撮(Ken Lund, CC BY-SA 2.0)は、機窓越しのピンボケで場面が読めず不採用。乾いた塩面の多角形が読める章の図3(BLM)は原画像幅754pxで拡大要件(1280px)を満たさないため、地図では同じBLMの2500px版(薄く水の張った夕暮れ)を使った。

## snaps の写真(5枚、同日に目視選定+ライセンス確認)

| 場所 | Commonsファイル | 作者 / ライセンス | 年代 |
|---|---|---|---|
| モンロー | Pioneer Day Parade, Monroe, Utah (9365988601).jpg | Ken Lund, CC BY-SA 2.0 | いま |
| モアブ | Moab, Utah, main street, January 2019.jpg | Steven Baltakatei Sandoval, CC BY-SA 4.0 | いま |
| ソルトレークシティ・ダウンタウン | Green line Trax at Gallivan Plaza.jpg | Garrett, CC BY 2.0 | いま |
| アルタ | Alta ski lessons - Feb 21, 2011.jpg | Scott Catron, CC BY-SA 2.0 | いま |
| 南ユタの砂漠 | FARM WORKERS TAKING SHELTER DURING A DUST STORM IN SOUTHERN UTAH... - NARA - 553819.jpg | Terry Eiler(EPA・ドキュメリカ), パブリックドメイン | 1972年 |

- モンローのパイオニアデーの一枚は、本文6節・注20(7月24日)と響き合うため選んだ。同じ組の別カットは沿道の人物の顔が近く、馬の行列のカットにした。
- 1972年の砂嵐の写真は、章4節の「塵」の主題と響き合う。NARAの記録は「southern Utah」より細かい地名が無く、ピンは撮影地域(ナバホ領周辺)のメキシカンハット付近に概置した。
- ソルトレークシティのTRAXの実況文の「道幅40メートル」は、章6節・注21(シオンの区画)の数字に合わせた。
- スナップ選定の没: パイオニアデー別カット(私人の顔が近い)、ナバホの羊飼い(人物中心になりすぎる)、モアブのメインストリート1972(現代版のほうが場面が良い)、ユタ州フェアの海軍広報写真(場面が演出的)、Mt. Carmelの農場(Highsmith、.tifサムネイルの取得が不安定で見送り)。

## 検証記録(2026-09-03)

- `python site/build.py` 警告・エラーなし(23章)。JSONの `img` 全17本(places12+snaps5)が upload.wikimedia.org の500pxサムネイルで、HTTP 200をcurlで確認。原画像の幅は全点1280px以上(ソルトフラッツは2500px版を採用して充足)。
- ブラウザ検証: `_site/` をローカルHTTPサーバで開き、Playwright(Chromium)で確認。この実行環境ではブラウザが外部CDNにTLSで届かないため、MAPS.md 6節の但し書きに沿い、外部リクエストをcurl経由で充足するインターセプトで実施した(unpkgのLeaflet・タイル・写真とも実物を取得。外部710リクエスト充足・失敗0)。
  - [x] 地図パネルが開閉し、本文の📍地名タップで該当地点に飛んで吹き出しが開く(レッドロック峠→「3節」バッジつき吹き出し)
  - [x] チップで全地名を順に回れる(チップ13=全体+12地名)。ピンの節番号表示が正しい(1,2,注,3,3,4,4,5,5,5,6,6——アルタのみ注リンク)
  - [x] `?rich` でピン17本(places12+📷スナップ5)、チップ18、写真・クレジット表示、写真タップで全画面拡大(1280px版への差し替え)が動く
  - [x] モバイル幅(375px)でもリンク→吹き出しが動く(ソルトレークシティ・1節バッジ)
  - [x] 他の章のページに影響がない(wy.htmlのパネル動作を確認)
- Wikimediaのレート制限(429)が強く、API検索・サムネイル取得とも30〜120秒の待ちとリトライを挟んで通した。

## 座標の根拠

- レッドロック峠はアイダホ州バノック郡の峠の現地(42.3556, -112.0444。米国道91号が越える)。
- ボンネビル・ソルトフラッツはスピードウェイ付近、スパイラル・ジェッティはロゼルポイントの現地、グースネックスは州立公園の展望台、アーチーズはデリケートアーチの現地、プロモントリーはゴールデンスパイク国定歴史公園、ビンガムキャニオンは鉱山のピット。
- パウエル湖はダム上流の湖面(アリゾナ州側)に概置——章が語るのは水位とダムの取水口であるため。
- スナップの「南ユタの砂漠」はメキシカンハット付近に概置(上記)。他は市街中心(モンロー、モアブ、ギャリバンプラザ)またはスキー場の麓(アルタ)。
