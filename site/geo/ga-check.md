# ジョージア章の地図 検証記録(ga-check)

地図データは ga.json。作業手順は site/MAPS.md。紙面の編集用注記(text/usa/ga-check.md)とは別物で、こちらは地図(ウェブ版限定)の楽屋である。

## 経緯

- 2026-08-27 初版。章(text/usa/ga.md)のマージ後の後工程として作成。places 11 + snaps 8。

## places の写真(11枚、ライセンスはCommons APIのextmetadataで確認、2026-08-27)

| 地名 | Commonsファイル | 作者 / ライセンス |
|---|---|---|
| アトランタ | View of the midtown Atlanta skyline looking out over Piedmont Park's Lake Clara Meer.jpg | Marc Merlin, CC BY-SA 4.0 |
| ハーツフィールド・ジャクソン・アトランタ国際空港 | Atlanta Hartsfield-Jackson Airport Concourse A aerial (49054916886).jpg | formulanone, CC BY-SA 2.0(紙面の図3と同じ写真をURL参照で再利用) |
| サバナ | Port of Savannah - 2021.jpg | Jerry Glaser/米税関・国境警備局(CBP), パブリックドメイン |
| ゲインズビル | Downtown Gainesville, Georgia.jpg | ATLJonJon, CC BY 4.0 |
| プレーンズ | Main Street - Plains - Georgia - USA (34325680216).jpg | Adam Jones, CC BY-SA 2.0 |
| ドルトン | Whitfield County Crown Mill.jpg | GamblinMonkey, パブリックドメイン(作者放棄) |
| フォート・マクファーソン | TylerPerryStud.jpg | OneofaKind25, CC BY-SA 4.0 |
| ボーグル原子力発電所 | 2025-03-11 - Waynesboro, Georgia, USA - Plant Vogtle.jpg | Kai NeSmith, CC BY 4.0 |
| メタプラント | Hyundai Ioniq 5.jpg | TTTNIS, CC0 |
| オーバーン通り | Tomb of Martin Luther King - The King Center - Atlanta - Georgia - USA (34134019562).jpg | Adam Jones, CC BY-SA 2.0 |
| ストーンマウンテン | Stone Mountain, the carving, and the Train.jpeg | Pilotguy251, CC BY-SA 4.0 |

- リンク先の節/注: アトランタは1節にも出るが、話の本体である2節にリンク(リンク化は指定の節の初出1回)。サバナは注6(港の話の本体。3節の「サバナ近郊」や5節の「サバナ川」ではなく)。メタプラントは注15の「メタプラント」の表記に一致させた(「」内でも文字列一致でリンク化されることをビルドで確認)。
- 座標の特記: サバナはガーデンシティ・ターミナル(章が語る当の場所)。ドルトンはクラウン・ミル(ファイルの座標)。メタプラントはブライアン郡エラベルの工場の概略位置。オーバーン通りはキング・センター。フォート・マクファーソンは旧基地(現タイラー・ペリー・スタジオ)。
- 写真の特記: ボーグルは、章の図5(NRCの夕景、原画像1015px)が拡大表示の要件(原画像1280px以上)を満たさないため、別の写真(2025年撮影、4640px)を採用。メタプラントは工場の写真がCommonsに皆無のため、同工場で生産される車種アイオニック5の写真(撮影地は日本の展示会場)で代用し、richの一言にその旨を明記。ゲインズビルは「鶏の都」記念碑の写真がCommonsに無く(複数の言い回しで検索)、1280px以上を満たす唯一のダウンタウン写真を採用。

## snaps の写真(8枚、場面の良さで選定+ライセンス確認、2026-08-27)

| 場所 | Commonsファイル | 作者 / ライセンス | 年代 |
|---|---|---|---|
| ジャスパー | A Waffle House restaurant in Jasper, Georgia, US.jpg | Harrison Keely, CC BY 4.0 | いま |
| ノースアベニュー(アトランタ) | The Varsity interior seating in Atlanta, GA.jpg | WClarke, CC BY-SA 4.0 | いま |
| マリエッタ | The Big Chicken 2021, Marietta, GA, US.jpg | Jud McCranie, CC BY-SA 4.0 | いま |
| ブフォード・ハイウェイ | Buford Highway, Georgia June 2016.jpg | Thomson200, CC0 | いま |
| ダウンタウン・アトランタ | PASSENGERS IN ATLANTA ... MARTA BUS DURING RUSH HOUR - NARA - 556787.jpg | Jim Pickerell/EPA(DOCUMERICA), パブリックドメイン | 1974年 |
| グリーン郡 | Jack Delano, Going to town on Saturday afternoon, Greene County, Georgia, 1941.jpg | Jack Delano/FSA(米議会図書館), パブリックドメイン | 1941年 |
| トマスビル | Harden's Taxidermy, Thomasville, Georgia.jpg | The Bushranger, CC BY-SA 4.0 | いま |
| サバナの川辺 | Street Scene with Container Ship Passing - Savannah - Georgia - USA (34476689065).jpg | Adam Jones, CC BY-SA 2.0 | いま |

- 選定の方針: 現代6+昔2(1941年のFSAコダクローム=綿の国の週末、1974年のDOCUMERICA=地下鉄開業前のMARTAバス。どちらも章の3節・6節の筋に響く)。ワッフルハウス(ジョージア発祥のチェーン)、ビッグチキン、ブフォード・ハイウェイ、剥製屋と、絵はがきにならない生活の場面を優先。顔が大写しの写真は避けた(1941年は後ろ姿、1974年は群衆)。
- 座標の根拠: ジャスパー・マリエッタ・トマスビル・ヴァーシティはCommonsのファイル座標。ブフォード・ハイウェイはドラビル付近の概略。1974年MARTAバスはダウンタウンの概略。グリーン郡は郡の概略中心。サバナの川辺はリバーフロントの遊歩道。
- 選定の没: Buford Highway Farmer's Market(4256pxでライセンス可だが人物の顔が大写しのため除外)、ゆで落花生の鍋(座標はサバナ近郊だが説明文が「サウスカロライナの店」のため州の帰属が曖昧で除外)、DOCUMERICAの二階建てバス(1974年枠はラッシュのバス停の場面を優先)、サバナのチッペワ広場の輪タク(サバナは川辺の場面を優先)、MARTAディケーター駅の白黒長時間露光(モノクロで並びから浮くため)、ゲインズビルの鶏記念碑(Commonsに写真なし)。

## 検証(2026-08-27)

- python site/build.py: 警告・エラーなし(11章)。11地名すべてリンク化(未リンクの地名はビルドが警告する仕組み)。
- 全19枚の500pxサムネイルURLは取得(HTTP 200)を確認(数件は429のため十数秒おいて再試行の上で200)。原画像はいずれも幅1280px以上(拡大表示対応)。URLはAPIのthumburl(クエリ文字列を除いた形)。
- _site/ をHTTPサーバで開き、Chromium(Playwright)で確認:
  - 本文の📍地名タップでパネルが開き、該当地点の吹き出しが開く(ボーグル原子力発電所で確認。ピンに節番号バッジ「5節」)
  - チップ12個(全地名+一覧)で地名を回れる(空港への遷移と吹き出しを確認)
  - ?rich でマーカー19本(places 11+snaps 8)。📷スナップの吹き出しに年代チップ・実況文・クレジット(サバナの川辺で確認)。吹き出し内に写真要素があることを確認
  - モバイル幅(390px)でもパネル・吹き出しが動く(オーバーン通りで確認)
  - 他章に影響なし(テキサス章の地名リンク10個が従来通り)。ページエラーなし
  - 特記: この検証環境はヘッドレスブラウザから外部CDNに直接届かないため(ny章の検証時と同じ制約)、Leaflet本体のみローカルに差し替えて機能を検証した(タイル・写真の実URLの生死は上記の通り確認済み)。_site/は検証後にビルドし直してあり、差し替えは成果物に残っていない。実環境での見た目の最終確認はPages反映後に行える。
