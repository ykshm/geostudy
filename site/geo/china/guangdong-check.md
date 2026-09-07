# 広東章の地図 検証記録(guangdong-check)

地図データは guangdong.json。作業手順は site/MAPS.md。紙面の編集用注記(text/china/guangdong-check.md)とは別物で、こちらは地図(ウェブ版限定)の楽屋である。

## 経緯

- 2026-09-07 初版。中国33省区シリーズで最初の章別地図。places 12(本文の登場順)+ snaps 5 + extras 4。
- 域外(別章の題材)のピン用に、テンプレートの `.pin.mx, .pin.ca` の配色へ `.hk` を追加した(全章共通の1行。香港・マカオを持つ中国シリーズで今後も使う)。

## places の写真(12枚、ライセンスはCommons APIのextmetadataで確認、2026-09-07)

| 地名 | Commonsファイル | 作者 / ライセンス |
|---|---|---|
| 広州 | 海心沙島和廣州塔 Haixinsha Island and Guangzhou TV Tower - panoramio.jpg | Bohao Zhao, CC BY 3.0 |
| 虎門 | Humen Bridge-edit.jpg | Hinnne, CC BY-SA 2.0 |
| 台山 | Moy's Grand Courtyard.jpg(端芬鎮・梅家大院) | kenth31, CC BY 2.0 |
| 開平 | Kaiping Diaolou in Zili Village - 20181028-1.jpg(章の図4と同じ) | DragonSamYU, CC BY-SA 4.0 |
| 香港 | Hong Kong Night Skyline.jpg | Base64, CC BY-SA 3.0 |
| 深圳 | Civic Centre and Futian CBD, Shenzhen - 20251227, views from Lianhuashan Park.jpg | Pathfinbird, CC BY-SA 4.0 |
| 東莞 | SongshanLakeXbotPark.jpg(松山湖のロボット産業基地) | Raysonho, CC0 |
| 汕頭 | Xiaogongyuan.jpg(小公園の騎楼街) | Sgnpkd, CC BY-SA 4.0 |
| 蛇口 | Sea World in Shekou Shenzhen2021.jpg | Charlie fong, CC BY-SA 4.0 |
| 龍華 | 富士康深圳园区.jpg | Lhzss8, CC BY-SA 4.0 |
| 華強北 | Entrance of Huaqiangbei, 2017.jpg | 千里走单骑, CC BY-SA 3.0 |
| 中山 | GD 廣東 ZS 中山市 … SunWen West Road Pedestrian Zone February 2025 R12S 14.jpg | SaiShenGeee Em 6620, CC0 |

- 香港には `side: "hk"` を付けた(別章の題材である旨は text にも明記)。
- 深圳のリンクは4節初出の「深圳河」の中の「深圳」に張られる(文字列一致の仕様)。市のピンなので意味は通ると判断した。

## snaps の写真(5枚、目視選定+ライセンス確認、2026-09-07)

| 場所 | Commonsファイル | 作者 / ライセンス | 年代 |
|---|---|---|---|
| 広州・車陂 | GD 廣東 … 車陂街道 Chebei 三十三道自選快餐 … R12S 06.jpg | JAIWy uOMW 800 wovi, CC0 | いま |
| 広州・泮溪酒家 | GD 廣東 … 泮溪酒家 Pan Xi Restaurant 點心 dim sum June 2025 R12S 30.jpg | MeiOLA 2290 WMENSZ, CC0 | いま |
| 広州・蓮香樓 | GZ 廣州 … 蓮香樓 Lian Xiang Lou Restaurant June 2025 R12S 19.jpg | MeiOLA 2290 WMENSZ, CC0 | いま |
| 深圳・南頭古城 | 南头古城南门2022.jpg | Iswzo, CC BY-SA 4.0 | いま |
| 広州・商店街 | Sheung-mun-tai street in Canton, A. Chan, 1870.jpg | 阿真(A Chan), パブリックドメイン | 1870年 |

- 車陂のサムネイルURLはファイル名が長いためMediaWikiが `/500px-thumbnail.jpg` 形式を返す。APIのthumburlをそのまま採用し、500px/1280pxの両方が200を返すことを確認した。
- 選定の没: 東莞のニトリ店頭(場面はふだんだが日本チェーンの看板が主役になりすぎる)、台山市街のpanoramio 2点(場面が読めない)、広州タワー夕景の1枚(画面隅に「500px」の透かし)、丹霞山の東屋の1枚(肝心の赤い崖がほぼ写らない→別カットに差し替え)。

## extras の写真(4枚、ライセンス確認、2026-09-07)

| 見どころ | Commonsファイル | 作者 / ライセンス |
|---|---|---|
| 丹霞山 | 39145-Danxiashan (48989068302).jpg | xiquinhosilva, CC BY 2.0 |
| 広済橋 | Chaozhou Guangji Bridge 20191211.jpg | Akira CA, CC BY-SA 3.0 |
| 陳家祠 | Chen Clan Ancestral Hall 2025.06 01.jpg | Shujianyang, CC BY-SA 4.0 |
| 清暉園 | Foshan Shunde Qinghui Yuan 2024-05-11 16.06.40.jpg | 古海岸遗址, CC BY-SA 4.0 |

- 著者が注で推した見どころ(南越王墓・沙面・小公園など)とは重ねず、紙面に出ない4件を選んだ。丹霞山は「丹霞地形」の語源、広済橋は浮橋、陳家祠は屋根の陶塑、清暉園は「厨出鳳城」の順徳、といずれも章の筋(地形・川・宗族・食)に響くもの。

## 検証(2026-09-07)

- `python3 site/build.py` 警告・エラーなし。places の12リンクすべてが章ページに張られたことを生成HTMLで確認(data-i 0〜11)。
- 全21枚の500pxサムネイルURLと、タップ拡大用の1280px版URLの計42本がHTTP 200を返すことを確認。原画像はいずれも幅1280px以上。
- `_site/` をHTTPサーバ(127.0.0.1:8901)で開き、Playwright+同梱Chromiumでブラウザ検証。リモート実行環境のブラウザからは外部に届かないため、MAPS.md 6節の但し書きに従い、タイルと写真は遮断して検証し、到達性は別途curlで確認した(arcgisonline・openstreetmap・cartocdn の3ホストとも200)。結果は23項目すべて合格:
  - 地図パネルの開閉、本文の📍タップで該当地点へ飛び吹き出しが開く(広州で確認)
  - チップ13個(全体+12地名)で全地名を回れる。ピンの節番号表示が正しい(深圳=4節で確認)。香港ピンは域外の配色
  - `?rich` で写真・クレジット・📷スナップピン5個・✦補遺ピン4個が出る。吹き出しの写真は500pxサムネで、拡大は1280px版に差し替わる設計(URL両方の200を確認)
  - モバイル幅(390px)でパネルの開閉が動く
  - 他の章(usa/oh)のリンクと地図ページに影響なし。コンソールエラーなし
