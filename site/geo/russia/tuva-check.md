# トゥヴァ章 地図の検証記録(楽屋)

作成日: 2026-09-10。対象: site/geo/russia/tuva.json(places 10・snaps 予定5前後、extras 無し=ロシアシリーズの先行章と同じ)。

## places の選定

本文の筋を運ぶ地名10箇所を登場順に採った。サンフランシスコとパサデナは章の伝送の軸(短波の受信地、ファインマンの問いの発地)を担うため米国側の地名として採り、`side: "us"` で色を分けた(テンプレートに .pin.us / .chip.us を追加。既存の mx/ca/hk と同じ配色で、他章への影響は無い)。ベロツァールスクはキジルと同一地点のため立てない。クラギノは複合語(キジル=クラギノ鉄道)の中にしか現れず、単独の文字列一致が取れないため、炭田側のエレゲストで代表させた。

- 座標の根拠: 市街はその中心。サヤン山脈・タンヌ・オラ山脈は稜線上の代表点(サヤンはR257の峠周辺、タンヌ・オラはモンゴル国境北側の稜線)。トジュは中心集落トーラ・ヘム。エレゲストはエレゲスト川沿いの集落(炭田の名の由来地)。トゥランは市街。

## 写真のライセンス確認(Commons API extmetadata、2026-09-10。全点800px版をダウンロードして被写体を目視確認)

places:
- サンフランシスコ = File:San Francisco from Twin Peaks September 2013 panorama 5.jpg(King of Hearts, CC BY-SA 3.0、9600px)
- サヤン山脈 = File:Lake Raduzhnoye and Sleeping Sayan, Ergaki Range, Sayan Mountains, Russia.jpg(Vyacheslav Argenberg, CC BY 4.0、6000px)。エルガキは峠のクラスノヤルスク側だが、キジルへの道が越える西サヤンの山群として採用し、richにその旨を書いた
- タンヌ・オラ山脈 = File:Счастье не за горами, счастье в горах!.jpg(Zamunu45, CC BY-SA 4.0、3888px)。説明文「Овюрский район РТ. Перевал」=オヴュール地区の峠
- トジュ = File:Озеро Азас, Тоджинского района Тувы.jpg(Zamunu45, CC BY-SA 4.0、3888px)
- モスクワ = File:Moscow Kremlin from Kamenny bridge.jpg(Минеева Ю. (Julmin) / Surendil, CC BY-SA 1.0、2048px)
- キジル = File:Вид на обелиск Центр Азии.jpg(Zamunu45, CC BY-SA 4.0、3888px)
- パサデナ = File:Caltech Entrance.jpg(Canon.vs.nikon, CC BY-SA 3.0、2000px)
- チャダン = File:Храм Устуу-Хурээ.jpg(Knsovna, CC BY-SA 4.0、3456px)
- エレゲスト = File:Bahnstrecke Elegest–Kyzyl–Kuragino.png(Pechristener / ベース地図 Uwe Dedering, CC BY-SA 2.0、3342px)。エレゲストの現地写真はCommonsでは小さい1点(491px)しか無く、実現していない計画路線図を「線は地図の上にだけある」の一枚として採用した
- トゥラン = File:Долина Царей.jpg(Zamunu45, CC BY-SA 4.0、3888px)

snaps(写真ファーストで選定。5枚=現代3・2004年2・1984年1のうち昔は1枚):
- ユルタと二つの旗 = File:Tuva, Russia 31.jpg(stepa, CC BY 2.0、2048px、2004-08-14撮影。説明「Кызыл, Наадым」)
- フレシュを待つ観客席 = File:Tuva, Russia 36.jpg(stepa, CC BY 2.0、2048px、同上「Кызыл, Наадым, хуреш」)
- 龍の噴水 = File:У фонтана в Центре Азии.jpg(Agilight, CC BY-SA 4.0、3264px、2016-08-17)
- タンヌ・オラの野営 = File:Tuva 1984 Andrey Puzachenko.jpg(Ivtorov, CC BY-SA 4.0、2916px、1984-08。説明「А.Ю. Пузаченко в экспедиции в Туве, хребет Танну-Ола」)
- 舞台の上のフレシュ = File:Борьба Хуреш.jpg(Zamunu45, CC BY-SA 4.0、5184px、2016-06-27。劇場の舞台上の取組で、実況文もそのように書いた)

不採用の主なもの: File:Tuva, Russia 35.jpg(祭りの人混みの僧2人。良い場面だが現代の私人の顔が大写しのため見送り)、File:Elegest ugol.jpg(491pxで寸法不足)、File:Горы Саяны.jpg(説明文がブリヤートのアルシャン=東サヤンで、章のサヤンと場所が合わない)、File:Wrestling competition in Tos Bulak.jpg(989pxで寸法不足)。

- 全imgのURL(500pxサムネイル、upload.wikimedia.org)と拡大用1280px版のHTTP 200を確認(2026-09-10)。一部は初回429(サムネイルのレート制限)で、間隔を空けた再試行で全点200を確認。
- 原画像の幅は全点1280px以上。

## 検証(2026-09-10)

1. `python3 site/build.py` 警告・エラーなし(35章)。
2. `_site/` を localhost:8123 のHTTPサーバで開き、Playwright(同梱Chromium)で確認。リモート実行環境のため、ブラウザから外部(地図タイル・Commonsの写真)へはTLSが通らず、MAPS.md 6節の但し書きに従い、タイル・写真URLの到達性はcurlで別途確認した上で、外部要求を遮断してUIを検証した:
   - [x] 章ページの📍地名リンク10件が生成され、タップで地図パネルが開き、該当地点の吹き出しが開く(キジル=3節の吹き出しで確認)
   - [x] チップで地名を回れる(placesチップ+スナップチップ+現在地チップの計16)。ピンとチップの節番号表示が正しい(サヤン/タンヌ・オラ=1、キジル/モスクワ=3、チャダン/エレゲスト=6など)。米国側(サンフランシスコ・パサデナ)はテンプレートに追加した .us の赤系配色で表示
   - [x] `?rich` でピン15(places10+📷スナップ5)、吹き出しに写真のimgタグとクレジット行(「写真: stepa, CC BY 2.0」等)が出る
   - [x] モバイル幅(390px)でもピン・チップ・吹き出しが動く
   - [x] 他の章に影響なし(sakha=📍9件、tn=📍12件が従来通り生成。テンプレート変更は .us クラスの追加のみで、既存章は使用していない)
3. 収集の実務メモ: Commons APIのレート制限(429)が強く、候補探しはMediaSearch、メタデータはまとめて1回のAPI照会+90〜150秒間隔の再試行、URL到達性確認も45秒間隔で行った。
