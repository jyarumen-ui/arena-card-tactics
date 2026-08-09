// 実際の画面をクリック操作しながら自動プレイし、紹介動画用のフレームを書き出す
const puppeteer = require("puppeteer-core");
const fs = require("fs"), path = require("path");

const CHROME = "C:/Program Files/Google/Chrome/Application/chrome.exe";
const GAME = "file:///" + path.resolve(__dirname, "..", "index.html").replace(/\\/g, "/");
const DIR = path.join(__dirname, "frames");

const sleep = ms => new Promise(r => setTimeout(r, ms));

(async () => {
  fs.rmSync(DIR, { recursive: true, force: true });
  fs.mkdirSync(DIR, { recursive: true });

  const browser = await puppeteer.launch({
    executablePath: CHROME, headless: "new",
    defaultViewport: { width: 1280, height: 720, deviceScaleFactor: 1 },
    args: ["--autoplay-policy=no-user-gesture-required", "--force-device-scale-factor=1",
           "--hide-scrollbars", "--disable-gpu"]
  });
  const page = await browser.newPage();
  page.on("pageerror", e => console.log("!! ページ例外:", e.message));
  await page.goto(GAME, { waitUntil: "networkidle0" });
  // 初回起動の画面から始めたいので、保存データを消す
  await page.evaluate(() => { try { localStorage.clear(); } catch (e) {} });
  await page.reload({ waitUntil: "networkidle0" });
  await sleep(1200);

  // 操作中の位置がわかるように、疑似カーソルを描く
  await page.evaluate(() => {
    const c = document.createElement("div");
    c.id = "_cur";
    c.style.cssText = "position:fixed;z-index:9999;width:22px;height:22px;pointer-events:none;" +
      "left:-40px;top:-40px;transition:left .28s cubic-bezier(.3,.9,.4,1),top .28s cubic-bezier(.3,.9,.4,1);" +
      "background:radial-gradient(circle at 34% 30%, #fff 0 26%, rgba(255,255,255,.85) 40%, rgba(255,220,140,.35) 62%, transparent 74%);" +
      "border-radius:50%;filter:drop-shadow(0 2px 5px rgba(0,0,0,.8));";
    document.body.appendChild(c);
    const r = document.createElement("style");
    r.textContent = "@keyframes _tap{from{transform:scale(1);opacity:.9}to{transform:scale(2.6);opacity:0}}" +
      "._ring{position:fixed;z-index:9998;width:26px;height:26px;border:2px solid #ffe9a0;border-radius:50%;" +
      "pointer-events:none;animation:_tap .45s ease-out forwards}";
    document.head.appendChild(r);
    window._moveCur = (x, y) => {
      const e = document.getElementById("_cur");
      e.style.left = (x - 11) + "px"; e.style.top = (y - 11) + "px";
    };
    window._tap = (x, y) => {
      const d = document.createElement("div");
      d.className = "_ring"; d.style.left = (x - 13) + "px"; d.style.top = (y - 13) + "px";
      document.body.appendChild(d); setTimeout(() => d.remove(), 500);
    };
  });

  // 指定した要素へカーソルを動かしてから押す
  async function tap(sel, opt) {
    opt = opt || {};
    const box = await page.evaluate(s => {
      const el = document.querySelector(s);
      if (!el) return null;
      const r = el.getBoundingClientRect();
      return { x: r.left + r.width / 2, y: r.top + r.height / 2 };
    }, sel);
    if (!box) { console.log("見つからない:", sel); return false; }
    await page.evaluate(([x, y]) => window._moveCur(x, y), [box.x, box.y]);
    await sleep(opt.pre === undefined ? 210 : opt.pre);
    await page.evaluate(([x, y]) => window._tap(x, y), [box.x, box.y]);
    await page.evaluate(s => { const e = document.querySelector(s); if (e) e.click(); }, sel);
    await sleep(opt.post === undefined ? 150 : opt.post);
    return true;
  }
  // テキストで探して押す
  async function tapText(sel, text, opt) {
    const id = await page.evaluate(([s, t]) => {
      const el = [...document.querySelectorAll(s)].find(e => e.textContent.includes(t));
      if (!el) return null;
      el.setAttribute("data-promo", "1");
      return true;
    }, [sel, text]);
    if (!id) { console.log("見つからない:", sel, text); return false; }
    const ok = await tap("[data-promo]", opt);
    await page.evaluate(() => document.querySelectorAll("[data-promo]").forEach(e => e.removeAttribute("data-promo")));
    return ok;
  }

  // ---- 録画開始 ----
  const client = await page.target().createCDPSession();
  const list = [];
  let n = 0;
  client.on("Page.screencastFrame", async ({ data, metadata, sessionId }) => {
    const f = path.join(DIR, String(n).padStart(5, "0") + ".jpg");
    fs.writeFileSync(f, Buffer.from(data, "base64"));
    list.push({ f, t: metadata.timestamp });
    n++;
    try { await client.send("Page.screencastFrameAck", { sessionId }); } catch (e) {}
  });
  await client.send("Page.startScreencast", { format: "jpeg", quality: 92, everyNthFrame: 1 });
  const t0 = Date.now();
  const at = async sec => { const w = t0 + sec * 1000 - Date.now(); if (w > 0) await sleep(w); };

  // ---- 台本 ----
  await at(2.2);
  await tapText(".menuCard", "チュートリアルなし");          // タイトル → ホーム
  await at(5.0);
  await tap('[data-go="battle"]');                            // ホーム → バトル
  await at(6.2);
  await tapText(".menuCard", "AI・弱い");                     // 難易度
  await page.evaluate(() => {
    const orig = window.startGame;
    window.startGame = (p, e, o) => orig(p, e || "mage", o);   // 相手はメイガス固定
  });
  await at(7.4);
  await tapText("#clsRow .clsCard", "ソードマスター");        // リーダー選択
  await at(8.9);
  await tap("#mullBtn");                                      // マリガンを終えて開始
  const started = await page.evaluate(() => !!S);
  if (!started) { console.log("!! 対戦が始まっていない"); }

  // ---- 対戦（手札から出す → 攻撃 → ターン終了 を繰り返す）----
  const myTurn = () => page.evaluate(() => !busy && S && S.p.hp > 0 && S.e.hp > 0);
  const over = () => page.evaluate(() => !S || S.p.hp <= 0 || S.e.hp <= 0);

  for (let turn = 0; turn < 14; turn++) {
    if (Date.now() - t0 > 27000) break;
    // 相手の手番が終わるのを待つ
    for (let i = 0; i < 60 && !(await myTurn()); i++) await sleep(200);
    if (await over()) break;
    await page.evaluate(() => {
      if (!S) return;
      [S.p, S.e].forEach(pl => { pl.mpMax = Math.min(10, pl.mpMax + 1); });
      S.p.mp = S.p.mpMax; render();
    });

    // 出せるカードを順に出す
    for (let k = 0; k < 5; k++) {
      const ok = await page.evaluate(() => {
        const c = document.querySelector("#handArea .card.playable");
        if (!c) return null;
        c.setAttribute("data-promo", "1"); return true;
      });
      if (!ok) break;
      await tap("[data-promo]", { pre: 200, post: 140 });
      await page.evaluate(() => document.querySelectorAll("[data-promo]").forEach(e => e.removeAttribute("data-promo")));
      // 置ける場所 or 対象があれば選ぶ
      const placed = await page.evaluate(() => {
        const s = document.querySelector("#gridP .slot.placeable") ||
                  document.querySelector(".targetable") ||
                  document.querySelector("#pedE");
        if (!s) return null;
        s.setAttribute("data-promo", "1"); return true;
      });
      if (placed) {
        await tap("[data-promo]", { pre: 190, post: 240 });
        await page.evaluate(() => document.querySelectorAll("[data-promo]").forEach(e => e.removeAttribute("data-promo")));
      }
      if (Date.now() - t0 > 27000) break;
    }

    // 動けるユニットで攻撃する（盤面を残したいので1体だけ）
    for (let k = 0; k < 1; k++) {
      const ok = await page.evaluate(() => {
        const u = document.querySelector("#gridP .unit.ready");
        if (!u) return null;
        u.setAttribute("data-promo", "1"); return true;
      });
      if (!ok) break;
      await tap("[data-promo]", { pre: 190, post: 160 });
      await page.evaluate(() => document.querySelectorAll("[data-promo]").forEach(e => e.removeAttribute("data-promo")));
      const tgt = await page.evaluate(() => {
        const t = document.querySelector("#gridE .unit.targetable") ||
                  document.querySelector("#pedE.targetable") || document.querySelector("#pedE");
        if (!t) return null;
        t.setAttribute("data-promo", "1"); return true;
      });
      if (tgt) {
        await tap("[data-promo]", { pre: 180, post: 420 });
        await page.evaluate(() => document.querySelectorAll("[data-promo]").forEach(e => e.removeAttribute("data-promo")));
      }
      if (await over()) break;
      if (Date.now() - t0 > 27500) break;
    }
    if (await over()) break;
    const st = await page.evaluate(() => S ? (S.turn + "T 自" + S.p.hp + " 敵" + S.e.hp + " 盤" + S.p.board.filter(Boolean).length) : "-");
    console.log("  ", ((Date.now() - t0) / 1000).toFixed(1) + "s", st);
    await tap("#endBtn", { pre: 200, post: 220 });
  }

  // 最後にとどめを刺して、勝利画面まで見せる
  if (!(await over())) {
    for (let i = 0; i < 40 && !(await myTurn()); i++) await sleep(200);
    await page.evaluate(() => {
      if (!S) return;
      S.e.hp = 3;
      S.e.board = [null, null, null, null, null, null];          // 壁をどける
      if (S.p.board.every(u => !u)) {                            // 盤面が空なら1体立てる
        const c = POOL.find(x => x.t === "unit" && x.a >= 4 && !x.kw);
        if (c) summon("p", { ...c }, 1);
      }
      S.p.board.forEach(u => { if (u) { u.ready = true; u.acted = false; u.sealed = false; u.a = Math.max(u.a, 4); } });
      busy = false; S.sel = null; render();
    });
    await sleep(500);
    for (let k = 0; k < 3 && !(await over()); k++) {
      const ok = await page.evaluate(() => {
        const u = document.querySelector("#gridP .unit.ready");
        if (!u) return null; u.setAttribute("data-promo", "1"); return true;
      });
      if (!ok) break;
      await tap("[data-promo]", { pre: 220, post: 180 });
      await page.evaluate(() => document.querySelectorAll("[data-promo]").forEach(e => e.removeAttribute("data-promo")));
      await tap("#pedE", { pre: 220, post: 700 });
    }
  }
  const finishSec = (Date.now() - t0) / 1000;
  console.log("   決着:", await page.evaluate(() => S ? ("自" + S.p.hp + " 敵" + S.e.hp) : "画面遷移済み"),
              "/", finishSec.toFixed(1) + "秒");
  // 音楽をこの動画の進行に合わせるため、切り替えどころを書き出す
  fs.writeFileSync(path.join(__dirname, "meta.json"),
    JSON.stringify({ battleSec: 9.0, finishSec: +finishSec.toFixed(2), totalSec: +(finishSec + 7).toFixed(2) }, null, 2));

  // 勝敗画面の余韻
  await sleep(7000);
  await client.send("Page.stopScreencast");
  await sleep(300);

  // フレームの表示時間を書き出す（可変フレームレートのまま繋ぐ）
  const lines = [];
  for (let i = 0; i < list.length; i++) {
    const d = (i < list.length - 1 ? list[i + 1].t - list[i].t : 0.12);
    lines.push("file '" + path.basename(list[i].f) + "'");
    lines.push("duration " + Math.max(0.016, d).toFixed(4));
  }
  if (list.length) lines.push("file '" + path.basename(list[list.length - 1].f) + "'");
  fs.writeFileSync(path.join(DIR, "list.txt"), lines.join("\n"));
  console.log("フレーム:", list.length, "枚 / 収録", ((Date.now() - t0) / 1000).toFixed(1), "秒");

  const res = await page.evaluate(() => S ? { p: S.p.hp, e: S.e.hp } : "終了済み");
  console.log("結果:", JSON.stringify(res));
  await browser.close();
})();
