/*
 * geostudy 地図パネル
 * 記事HTMLの末尾に1行入れるだけ:
 *   <script src="map-panel.js" data-map="../maps/tx-map.html"></script>
 *
 * ・右下の「地図」ボタンで表示ON/OFF
 * ・スマホ: 画面上半分 / PC: 画面右半分（本文は自動で退避）
 * ・本文中の <a class="geo" data-i="0">スピンドルトップ</a> をタップすると
 *   パネルが開いてその地点へ飛ぶ（data-i は地図のPLACES配列の番号）
 * ・開閉状態は記憶され、次の章へ移動しても維持される
 */
(function () {
  var script = document.currentScript;
  var src = script && script.dataset.map;
  if (!src) { console.warn("map-panel: data-map 属性がありません"); return; }

  var css = [
    "#gs-map-btn{position:fixed;right:16px;bottom:16px;z-index:10001;",
    " border:none;border-radius:999px;padding:11px 18px;font-size:14px;",
    " background:#2F4B7C;color:#fff;box-shadow:0 2px 8px rgba(0,0,0,.3);",
    " cursor:pointer;font-family:inherit;}",
    "#gs-map-panel{position:fixed;z-index:10000;background:#fff;",
    " box-shadow:0 0 12px rgba(0,0,0,.25);transition:transform .3s ease;}",
    "#gs-map-frame{width:100%;height:100%;border:0;display:block;}",
    "body{transition:padding-top .3s ease,margin-right .3s ease;}",
    "@media (max-width:768px){",
    " #gs-map-panel{top:0;left:0;right:0;height:50vh;transform:translateY(-101%);}",
    " html.gs-map-open #gs-map-panel{transform:none;}",
    " html.gs-map-open body{padding-top:51vh !important;}}",
    "@media (min-width:769px){",
    " #gs-map-panel{top:0;right:0;bottom:0;width:50%;transform:translateX(101%);}",
    " html.gs-map-open #gs-map-panel{transform:none;}",
    " html.gs-map-open body{margin-right:50% !important;}}",
    "#gs-photo-lightbox{position:fixed;inset:0;z-index:10002;",
    " background:rgba(0,0,0,.92);display:none;align-items:center;",
    " justify-content:center;flex-direction:column;cursor:zoom-out;}",
    "#gs-photo-lightbox.open{display:flex;}",
    "#gs-photo-lightbox img{max-width:96vw;max-height:86vh;object-fit:contain;",
    " box-shadow:0 4px 24px rgba(0,0,0,.6);}",
    "#gs-photo-lightbox .gs-lb-caption{color:#ddd;font-size:12px;",
    " margin-top:10px;padding:0 16px;text-align:center;max-width:92vw;",
    " line-height:1.6;font-family:inherit;}",
    "#gs-photo-lightbox .gs-lb-close{position:absolute;top:12px;right:16px;",
    " color:#fff;font-size:26px;line-height:1;opacity:.8;}",
  ].join("");
  var style = document.createElement("style");
  style.textContent = css;
  document.head.appendChild(style);

  var panel = document.createElement("div");
  panel.id = "gs-map-panel";
  var btn = document.createElement("button");
  btn.id = "gs-map-btn";
  btn.textContent = "地図";
  document.body.appendChild(panel);
  document.body.appendChild(btn);

  var iframe = null;
  var ready = false;
  var open = false;

  // 地図(パネル/章末おまけのiframe)から写真タップを受けて全画面表示する
  var box = document.createElement("div");
  box.id = "gs-photo-lightbox";
  box.innerHTML = '<span class="gs-lb-close">✕</span><img alt="">' +
                  '<div class="gs-lb-caption"></div>';
  document.body.appendChild(box);
  function closeBox() { box.classList.remove("open"); }
  box.addEventListener("click", closeBox);
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape") closeBox();
  });
  window.addEventListener("message", function (e) {
    var d = e.data || {};
    if (d.geostudy !== "photo" || typeof d.src !== "string") return;
    if (!/^https:\/\/upload\.wikimedia\.org\//.test(d.src)) return;
    box.querySelector("img").src = d.src;
    box.querySelector(".gs-lb-caption").textContent =
      typeof d.caption === "string" ? d.caption : "";
    box.classList.add("open");
  });

  function ensureIframe() {
    if (iframe) return;
    iframe = document.createElement("iframe");
    iframe.id = "gs-map-frame";
    iframe.src = src;
    panel.appendChild(iframe);
  }
  window.addEventListener("message", function (e) {
    if ((e.data || {}).geostudy === "ready") ready = true;
  });

  function setOpen(v) {
    open = v;
    if (v) ensureIframe();
    document.documentElement.classList.toggle("gs-map-open", v);
    btn.textContent = v ? "✕ 地図を閉じる" : "地図";
    try { localStorage.setItem("gsMapOpen", v ? "1" : "0"); } catch (_) {}
  }
  btn.addEventListener("click", function () { setOpen(!open); });

  // 本文中の地名リンク → パネルを開いて該当地点へ
  document.addEventListener("click", function (e) {
    var a = e.target.closest && e.target.closest("a.geo");
    if (!a) return;
    e.preventDefault();
    if (!open) setOpen(true);
    var i = parseInt(a.dataset.i, 10);
    var send = function () {
      iframe.contentWindow.postMessage({ geostudy: "focus", i: i }, "*");
    };
    if (ready) send(); else setTimeout(send, 900);
  });

  // 前回開いていたら開いた状態で始める
  var was = "0";
  try { was = localStorage.getItem("gsMapOpen") || "0"; } catch (_) {}
  if (was === "1") setOpen(true);
})();
