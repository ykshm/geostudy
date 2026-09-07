# 佐田岬章の地図 検証記録(sadamisaki-check)

地図データは sadamisaki.json。作業手順は site/MAPS.md。紙面の編集用注記(text/japan/sadamisaki-check.md)とは別物で、こちらは地図(ウェブ版限定)の楽屋である。作業日 2026-09-07。

## 構成

- places 9・snaps 5・extras 3。座標は国土地理院の住所検索API(msearch.gsi.go.jp)で得た大字の代表点を基本にし、施設・突端(佐田岬灯台 33.3439/132.0139、伊方原発 33.4907/132.3108、佐多岬 30.9942/130.6603、豊予海峡は中間点)は公知の位置で置いた(小数4桁)。
- 章の筋の外のピンを2本置いた——注2の「佐多岬」(鹿児島。読み違いの注意書きを地図でも見せる)と、6節の「阿蘇」(130キロの距離感は地図でしか伝わらない)。前例は津軽章の尾州・上野。
- 正野と串(3節)は、使えるライセンスの写真がCommonsに無く、places の書式(img必須)を満たせないためピンを置いていない。3節の暮らしは snaps の九町・井野浦が近い場面を補う。
- 三机の九軍神慰霊碑(extras)の事実関係——三机湾が真珠湾攻撃の特殊潜航艇の極秘訓練地だったこと、湾形が真珠湾に似ていたこと、須賀公園の慰霊碑——は山陰中央新報の記事と伊方町の観光資料で確認。亀ヶ池温泉の落雷火災(2021年)と再建(2024年2月グランドオープン)、「四国最西端の温泉」の名乗りは、伊方町公式サイトと亀ヶ池温泉公式サイトで確認。

## places の写真(9枚、ライセンスはCommons APIのextmetadataで確認、2026-09-07)

| 地名 | Commonsファイル | 作者 / ライセンス |
|---|---|---|
| 佐多岬 | Cape Sata (52018967919).jpg | Raita Futo, CC BY 2.0 |
| 八幡浜 | 真網代集落 2017.jpg | Misei sen, CC BY-SA 4.0 |
| 伊方町 | Minatoura Port.jpg | Amake, CC BY-SA 3.0 |
| 三崎港 | Misaki port - 三崎港 - panoramio.jpg | yano@mama.akari.ne.jp (panoramio), CC BY-SA 3.0 |
| 豊予海峡 | Sadamisaki peninsula.JPG | FlyMeToFullmoon, パブリックドメイン |
| 佐賀関 | Saganoseki Port-2015-01.jpg | Gohachiyasu1214, CC BY-SA 4.0 |
| 伊方原子力発電所 | Sadamisakihantou02.jpg | Dokudami, CC BY-SA 4.0 |
| 阿蘇 | Aso Caldera Panorama (53000596105).jpg | Raita Futo, CC BY 2.0 |
| 佐田岬灯台 | Sadamisaki Lighthouse.jpg | Amake, CC BY-SA 3.0 |

## snaps の写真(5枚、目視選定+ライセンス確認、2026-09-07)

| 場所 | Commonsファイル | 作者 / ライセンス | 年代 |
|---|---|---|---|
| 湊浦の春 | Ikata - Minatoura in Spring.JPG | Amake, CC BY-SA 3.0 | 2008年春 |
| 九町の夕暮れ | Kuchō, Ikata at sunset.jpg | Amake, CC BY-SA 3.0 | 2007年 |
| 尾根の一本道 | Sadamisakihantou03.jpg | Dokudami, CC BY-SA 4.0 | いま(2015年撮影) |
| 三崎港の出入り | Misaki port - 三崎港 - panoramio.jpg | yano@mama.akari.ne.jp, CC BY-SA 3.0 | いま(2013年撮影) |
| 井野浦の倉庫 | Inoura-井野浦 - panoramio.jpg | Yobito KAYANUMA, CC BY-SA 3.0 | 2011年 |

- era は撮影年の分かるものに年を明記し、2013年以降は「いま」とした。撮影年はいずれもCommonsのメタデータによる。
- 三崎港の写真は places と snaps で同じ一枚を使った(場面としても代表写真としても最良だったため。ピンの位置と文は別)。
- 選定の没: 鳥津漁港S30.jpg・鳥津漁港（現在）.jpg(印刷物の複写とみられる網点が出ており、権利の出所が確認できないため。MAPS.md 7節)、Setokazenooka-park01.jpg(原画像800pxで拡大要件1280px未満)、Sadamisaki 01/03/05.jpg(同・1280px未満)、Maana Mikan ac.jpg(店頭の袋詰めで場面が半島でない)。

## extras の写真(3枚)

| 見どころ | Commonsファイル | 作者 / ライセンス |
|---|---|---|
| 三机の九軍神慰霊碑 | Ikata 9 War Heroes monument.jpg | Amake, CC BY-SA 3.0 |
| 佐田岬亀ヶ池温泉 | 佐田岬亀ケ池温泉.jpg | キアラア, CC0 |
| 関崎 | Oita sekizaki hoyo strait.jpg | 大分帰省中, CC BY-SA 3.0 |

- 紙面で著者が推した見どころ(灯台・洞窟砲台・御籠島・はなはな・メロディー道路)とは重ねていない。

## 技術検証(2026-09-07)

- 全imgのURL(upload.wikimedia.orgの500pxサムネイル)はHTTP 200を確認。原画像の幅はすべて1280px以上。
- `python3 site/build.py` 警告・エラーなし(29章)。
- ブラウザ検証はリモート実行環境のため、MAPS.md 6節の代替手順による(タイルとwikimediaへはブラウザから届かないため、タイルを遮断してPlaywright(Chromium)で確認)。初回検証時はLeafletのCDN(unpkg)にも届かず、_siteのコピーで一時的にローカル退避して確認した。その後、地図全滅の修正(PR #71)でLeafletが site/assets/vendor/ に同梱されたため、mainを取り込んで再ビルドし、細工なしの生成物で全項目を再検証した(2026-09-07)。リポジトリのテンプレートは変更していない。
  - [x] 章ページに📍リンク9本が出て、タップで地図パネル(iframe)が開く
  - [x] ?rich でピン17本(places 9 + 📷5 + ✦3)、チップに節番号/注番号・✦・📷が正しく出る
  - [x] チップからピンへ飛び、吹き出しが開く(era「📷2011年」・実況文・クレジット表示を目視)
  - [x] モバイル幅(390px)でもピン17本と操作を確認
  - [x] 他章(津軽)の地図に影響なし(既定モードでピン10本)
  - 写真の実表示はブラウザからwikimediaに届かないため確認できず。URLの到達性はcurlの200で担保した。
