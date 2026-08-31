# 津軽章の地図 検証記録(tsugaru-check)

地図データは tsugaru.json。作業手順は site/MAPS.md。紙面の編集用注記(text/japan/tsugaru-check.md)とは別物で、こちらは地図(ウェブ版限定)の楽屋である。

## 経緯

- 2026-08-31 初版。臥遊風土記の最初の章別地図。series.md 11節が予告していた第三の層 extras(補遺の見どころ)をこの作業で整備した——template.html に✦のピンとチップ(おまけモード限定)、build.py に extras の書式検査と章末おまけの説明文、MAPS.md に書式と選定基準を追加。extras の無い既存章(usa)には✦は出ない(挙動不変)。
- places 10・snaps 5・extras 5。座標は地理院地図・OpenStreetMapで確認した市街・施設の位置(小数4桁)。

## places の写真(10枚、ライセンスはCommons APIのextmetadataで確認、2026-08-31)

| 地名 | Commonsファイル | 作者 / ライセンス |
|---|---|---|
| 岩木山 | Iwakisan Winter 201,801 IMG 6746 stitchx7.jpg | あおもりくま, CC BY-SA 4.0 |
| 尾州 | Masumida Shrine Haiden.jpg | Bariston, CC BY-SA 4.0 |
| 上野 | Ueno Station at night 20191130.jpg | 掬茶, CC BY-SA 4.0 |
| 大鰐町 | JR East Ōwani-Onsen Station building and Konan Railway Ōwani Station building in Owani Town, Aomori Pref.jpg | Mister0124, CC BY-SA 4.0 |
| 五所川原 | 140914 Goshogawara Station Goshogawara Aomori pref Japan02s3.jpg | 663highland, CC BY 2.5 |
| 弘前 | Fuyu-ni-saku-sakura in Hirosaki Castle 2020.jpg | 掬茶, CC BY-SA 4.0 |
| 青森市三内 | 140913 Sannai-Maruyama site Aomori Japan01bs6bs6.jpg | 663highland, CC BY 2.5 |
| 旧金木町 | Shayōkan the birthhouse of Osamu Dazai.jpg | 掬茶, CC BY-SA 4.0 |
| 秋田市 | Senshu Park uchibori.jpg | 掬茶, CC BY-SA 3.0 |
| にかほ市 | Kisakata to Tyôkaisan1.jpg | らんで, CC BY 4.0 |

- 弘前の当初候補「Hirosaki Castle and Mount Iwaki - Apr 14, 2024.jpg」は原画像1024pxで拡大要件(幅1280px以上)を満たさず差し替え。

## snaps の写真(5枚、目視選定+ライセンス確認、2026-08-31)

| 場所 | Commonsファイル | 作者 / ライセンス | 年代 |
|---|---|---|---|
| 五所川原駅の改札 | 五所川原駅構内の改札風景.jpg | Googugugu, CC BY-SA 4.0 | いま |
| 中央弘前駅 | Konan Railway 7033F at Chuo-Hirosaki 20250112.jpg | 掬茶, CC BY-SA 4.0 | いま |
| 青森・新町通り | View Shinmachi street from Hakko street, Aomori 01 - Jan 16, 2013.jpg | Konstantin Leonov, CC BY 2.0 | いま |
| 立佞武多の夜 | Tachineputa Float.jpg | Occidentale, CC BY 4.0 | いま |
| 弘前のりんご園 | Malus domestica Fuji Apple Hirosaki Aomori Japan 20161016a.jpg | あおもりくま, CC BY-SA 4.0 | いま |

- 中央弘前の車体の帯は、こぎん刺し柄のラッピングと断定できる資料が見つからなかったため、実況文は「菱模様の帯」という見た目の記述に留めた。
- りんご園の写真は撮影園地が特定できないため、ピンは弘前市りんご公園の位置に置いた(実況文は場面の記述のみで園名は書いていない)。
- 選定の没: Hirosaki Snow Festival - panoramio.jpg(雪燈籠まつり。取得検証が通らず見送り)、Tsugaru Line Daruma stove 19920222.jpg(ストーブ列車の車内。著者が注14で推した見どころと重複するため)。

## extras の写真(5枚、目視選定+ライセンス確認、2026-08-31)

| 場所 | Commonsファイル | 作者 / ライセンス |
|---|---|---|
| 木造駅 | 木造駅遮光器土偶駅舎 01.jpg | Yoit, CC0 |
| 木村産業研究所 | Exterior of Kimura Industrial Laboratory.jpg | Tnk4a, CC BY-SA 4.0 |
| 田舎館村の田んぼアート | Japan- Aomori Inakadate tambo art 2015 3.jpg | yari hotaka, CC BY 2.0 |
| 黒石こみせ通り | Nakamachi district in Kuroishi City.jpg | 掬茶, CC BY-SA 4.0 |
| 鶴の舞橋 | Tsuruno-maihashi.jpg | MaedaAkihiko, CC BY-SA 4.0 |

- extras の実況文の事実の根拠(いずれも2026-08-31確認): 木造駅=高さ17mの遮光器土偶駅舎(1992年、ふるさと創生事業)・列車到着時に目が光る(つがる市観光資料・複数の記事)/木村産業研究所=前川國男の処女作・1932年・27歳・現在は弘前こぎん研究所が入居(弘前市の文化遺産サイトHIROSAKI Heritage、まるごと青森)/田んぼアート=1993年開始・色の違う複数品種の稲で描く(田舎館村公式、Wikipedia)/こみせ=藩政時代からの雪よけの木造アーケード(黒石市観光資料)/鶴の舞橋=1994年完成・全長300m・青森ヒバ・「日本一長い木造三連太鼓橋」は鶴田町など公称のため「という」で伝聞に(鶴田町観光サイト、nippon.com)。
- 著者が紙面で推した見どころ(こぎん研究所の見学=注4、ストーブ列車・地吹雪体験=注14、ファッション甲子園=注19)との重複を避けた。木村産業研究所は建物(前川建築)としての紹介で、注4のこぎん刺しの推しとは別の目とした。
- 立佞武多(高さ約23m・毎年8月4〜8日・綱を曳く運行)は五所川原市観光協会・Wikipediaで確認。

## 技術検証(2026-08-31)

- 全20枚の500pxサムネイルURLがHTTP 200を返すことを確認。原画像はいずれも幅1280px以上(拡大表示に対応)。
- `python site/build.py` 警告・エラーなし(18章)。
- ブラウザ検証(MAPS.md 6節): `_site/` をローカルHTTPサーバで開き、Chromium(Playwright)で自動確認22項目すべて合格——(1)章ページの地図パネル開閉、📍地名リンク10個、📍タップで該当地点の吹き出し(2)チップで全地名を巡回、節番号表示(1節/2節/3節×3/4節/注9/注14/注16×2)が正しい(3)?richで✦チップ5・📷チップ5・写真・クレジット・補遺バッジ・写真タップの全画面拡大(4)モバイル幅(390px)でチップ21個と✦吹き出し(5)他章への影響なし——テキサスrichに✦は出ず📷7個のまま、ミシガン章ページ正常。
- 検証環境の制約: このコンテナのChromiumは外部CDN(unpkg・タイルサーバ)へのTLS接続が不安定なため、Leaflet本体はローカルに退避したコピーを差し込み、タイルは遮断して検証した(コード側の挙動検証としては等価)。unpkgのleaflet.js/cssと全写真URLはcurlでHTTP 200を確認済みで、公開環境では通常どおり読み込まれる。
