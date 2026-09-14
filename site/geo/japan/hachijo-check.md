# 八丈島章 地図データ 検証記録(楽屋)

作成日: 2026-09-14。site/MAPS.md の手順による。テンプレート(site/maps/template.html)と map-panel.js には手を入れていない。正本(text/japan/hachijo.md)にも手を入れていない。

## ビルドと動作確認

- `python3 site/build.py` 警告・エラーなし(42章)。
- `_site/` を `python3 -m http.server` で配信し、Playwright+同梱Chromiumで確認した。リモートの実行環境のため、ブラウザからの外部アクセス(地図タイル・Commonsの写真)は遮断して検証し、タイルと写真URLの到達性は curl の HEADリクエストで別途確認した(下記)。
  - [x] 本文の📍地名リンクが12個、各地名とも指定の節で1回だけリンク化される
  - [x] 「地図」ボタンでパネル(iframe)が開閉する
  - [x] 📍タップで該当地点に飛び、吹き出しが開く(八丈富士で確認)
  - [x] チップで全地名を回れる(先頭の「全体」チップはテンプレートの仕様。地名12+全体で13、?richでは snaps 5・extras 4 が加わり22)。ピンの節番号表示あり
  - [x] `?rich` で写真・クレジット・📷スナップピン・✦extrasピンが出る。吹き出しに `popup-photo` のimg要素とクレジットを確認
  - [x] モバイル幅(400px)でもパネルとチップが動く
  - [x] 他の章(佐田岬・多摩・テキサス)のページに影響なし(HTTP 200・JSエラーなし)
  - 写真タップの全画面拡大はテンプレート側の既存機構(map-panel.js のライトボックス)で、本作業ではテンプレート無変更のため既存章と同挙動。外部画像遮断下のため目視は省略し、画像URLの到達性確認で代えた。
- 画像URL: JSON中の全imgについて、500px と拡大用1280px の両方が HTTP 200 を返すことを確認(2026-09-14)。原画像はすべて幅1280px以上。

## 座標の根拠

- 大賀郷・樫立・中之郷・末吉・底土(神湊)・八重根港・裏見ヶ滝: 国土地理院 住所検索API(msearch.gsi.go.jp)。
- 三宅島・御蔵島・新島: 日本語版Wikipediaの座標。
- 八丈富士山頂: 33.1392, 139.7622(地理院標高APIで849.5m を確認)。三原山: 33.0925, 139.8150(標高APIの格子探索で局所最高677m の地点。山頂701mの至近)。
- 藍ヶ江港: 33.0515, 139.8245(中之郷南方の海岸。標高APIで海岸直近であることを確認した概算)。
- 竹芝桟橋: 35.6547, 139.7625(竹芝客船ターミナル。一般に流通する座標)。
- 大里の玉石垣: 33.0988, 139.7817(OpenStreetMap/Nominatimの登録地物「大里の玉石垣」)。ふるさと村も同一街区(33.0979, 139.7824)で整合。
- 宇喜多秀家の墓・青ヶ島島民の墓・メットウ井戸・中之郷の玉石垣・あしたば荘・三根の道・服部屋敷: Commonsファイルに記録された撮影地点(camera座標)。
- 八形山フリージア畑(大賀郷のrich写真): 33.1195, 139.7744(NAVITIMEの施設座標。住所は大賀郷4336)。

## 文言の根拠(特記)

- 八丈小島「1969年に住民全員が島を離れた」「沖合7.5キロ」: 日本語版Wikipedia「八丈小島」ほか(全国初の全島一括離島。2026-09-14取得)。
- メットウ井戸: 明治13年(1880年)掘削、メットウ=海産巻貝の島方言、上水道整備(昭和30年)まで使用、都指定史跡。出典: 日本語版Wikipedia「八重根のメットウ井戸」、東京都地域資源「八重根のメットウ井戸」(2026-09-14取得)。
- 青ヶ島島民の墓: 天明5年(1785年)の大噴火による八丈島への避難と、名主・佐々木次郎太夫らによる還住(全島帰還)が1824年=噴火からおよそ40年後であることは、日本語版Wikipedia「青ヶ島」による(2026-09-14取得)。当初「半世紀」と書いたが確認して40年に訂正した。墓地が大賀郷にあることはCommonsファイルの説明(撮影者さかおり)。
- 大里の玉石垣「陣屋」「流人が運んで積んだと伝わる」: GO TOKYO「陣屋跡(大里玉石垣)」、八丈島観光協会系の案内(伝承として。2026-09-14取得)。
- 中之郷「明和の飢饉で733人が餓死した」: 日本語版Wikipedia「八丈島」(本文注11と同じ)。
- 大賀郷「陣屋が置かれた」: GO TOKYO「陣屋跡(大里玉石垣)」。甘藷由来碑は本文注12の通り。
- 登龍峠のrich文の眼下の港・家並み: 写真の画面内容と地形図で確認(神湊・三根方向)。

## 採用した写真(すべてWikimedia Commons。ライセンスはAPIのextmetadataで2026-09-14確認)

places:
- 竹芝桟橋(+snap「竹芝の夜積み」) = Tachibana Maru at Takeshiba Pier.jpg(Syced, CC0。4032px。2022-07撮影)
- 三宅島 = Miyakejima Airport Aerial photograph.jpg(国土画像情報(国土交通省)、出典明記条件。2997px)
- 御蔵島 = Mikura-jima.jpg(Izawa Ryu, CC BY-SA 4.0。1368px)
- 八丈富士 = Inside Nishi-yama caldera.jpg(Izawa Ryu, CC BY-SA 4.0。6180px)
- 三原山 = Hachijōjima as viewed from Noboryu peak.jpg(hirohiro akabane, CC BY-SA 2.0。3248px)
- 八丈小島 = Hachijojimaview-fromosakahill-2018-5-7.jpg(Nesnad, CC BY-SA 4.0。8696px)
- 中之郷 = Nakanogo, Hachijo, Tokyo 100-1623, Japan - panoramio.jpg(Daibo Taku, CC BY 3.0。1600px。2012-06)
- 新島 = Niijima island aerial shoot.jpg(ブルーノ・プラス, CC BY-SA 4.0。2935px)
- 大賀郷 = Hachijojima freesia festival 2007-03-21.jpg(Geomr, CC BY-SA 3.0。2592px)
- 藍ヶ江 = Kusaya for sale - hachijojima - 2018 5 5.jpg(Nesnad, CC BY 4.0。2290px)
- 樫立 = Trace of Hattori residence. Historic site of Hachijojima.jpg(さかおり, CC BY-SA 4.0。6000px)
- 末吉 = Sueyoshi, Hachijo, Tokyo 100-1622, Japan - panoramio.jpg(Daibo Taku, CC BY 3.0。1600px)

snaps:
- 空から神湊 = Kaminato fishing port in Hachijojima.jpg(さかおり, CC BY-SA 4.0。6000px。2017-11)
- 三根の道ばた = Mitsune, Hachijo, Tokyo 100-1511, Japan - panoramio (13).jpg(Daibo Taku, CC BY 3.0。1600px。2012-06)
- あしたば荘の看板 = Nakanogo, Hachijo, Tokyo 100-1623, Japan - panoramio (2).jpg(Daibo Taku, CC BY 3.0。1600px。2012-06)
- 八重根の防波堤 = Yaene Port, Hachijo Island 01.jpg(さかおり, CC BY-SA 4.0。6000px。2017-11)

extras:
- 宇喜多秀家の墓 = Ukita Hideie's grave in Hachijojima 01.jpg(さかおり, CC BY-SA 4.0。6000px)
- 青ヶ島島民の墓 = Cemetery of Aogashima islanders from 18th to 19th century in Hachijojima.jpg(さかおり, CC BY-SA 4.0。6000px)
- 八重根のメットウ井戸 = Yaene spiral well B.jpg(さかおり, CC BY-SA 4.0。6000px)
- 大里の玉石垣 = Hachijojima tamaishigaki 2007-03-20.jpg(Geomr, CC BY-SA 3.0。2592px。ファイル説明は「流人が築いた玉石垣」。撮影地点の記録は無いため、ピンはOSM登録の大里の玉石垣に置き、実況文は写真に写る垣の描写にとどめた)

見送った写真: HachijoFuji.JPG・KUSAYA Workshop.JPG・大坂トンネル/地熱博物館/三原山登山道(いずれも原画像が幅1280px未満)、裏見ヶ滝2026(台風後の倒木の写真で見どころの実況に不向き)、八丈島 2017(島内の衣料品売り場。好適だが撮影地点が特定できず)、黒砂砂丘(座標を確証できず)。

## 補足

- くさや写真は章の図版(text/japan/img/)と同一のCommons由来だが、地図側はCommonsの500pxサムネイルへの直リンクであり、リポジトリには置いていない。
- extras は紙面(著者・梶谷縫)が拾わなかった見どころから、章の筋(流人・飢饉・水)と響き合うものを裏方の目で選んだ。著者の注との重複なし。
