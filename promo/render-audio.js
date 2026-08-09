// ゲーム本体のBGMエンジンをそのまま使い、紹介動画用の音声をWAVに書き出す
const puppeteer = require("puppeteer-core");
const fs = require("fs"), path = require("path");

const CHROME = "C:/Program Files/Google/Chrome/Application/chrome.exe";
const GAME = "file:///" + path.resolve(__dirname, "..", "index.html").replace(/\\/g, "/");
const OUT = path.join(__dirname, "bgm.wav");

// 何秒目にどの曲へ切り替えるか。録画側が書き出した進行に合わせる
let M = { battleSec: 9.0, finishSec: 36, totalSec: 43.6 };
try { M = JSON.parse(fs.readFileSync(path.join(__dirname, "meta.json"), "utf8")); } catch (e) {}
const CUES = [[0, "home"], [M.battleSec, "battle"], [M.finishSec, "win"]];
const SEC = Math.ceil(M.totalSec) + 1;
console.log("曲の切り替え:", JSON.stringify(CUES), "/", SEC, "秒");

(async () => {
  const browser = await puppeteer.launch({
    executablePath: CHROME, headless: "new",
    args: ["--autoplay-policy=no-user-gesture-required", "--disable-gpu"]
  });
  const page = await browser.newPage();
  await page.goto(GAME, { waitUntil: "networkidle0" });

  const b64 = await page.evaluate(async ({ SEC, CUES }) => {
    const SR = 44100;
    const off = new OfflineAudioContext(2, SR * SEC, SR);
    // ゲーム側のグローバルを差し替えて、そのままの音作りでレンダリングする
    AC = off;
    MASTER = off.createGain(); MASTER.connect(off.destination);
    NOISEBUF = off.createBuffer(1, SR * 0.3, SR);
    { const d = NOISEBUF.getChannelData(0); for (let i = 0; i < d.length; i++) d[i] = Math.random() * 2 - 1; }
    BGM.master = null; BGM.buses = null; BGM.conv = null;
    bgmInit();

    // currentTime を偽装して、実機と同じ bgmSchedule をそのまま回す
    let fake = 0;
    Object.defineProperty(off, "currentTime", { get: () => fake, configurable: true });
    BGM.on = true; BGM.started = true; BGM.scene = "home"; BGM.t = 0; BGM.mi = 0; BGM.bar = 0;

    let ci = 0;
    for (fake = 0; fake < SEC; fake += 0.25) {
      while (ci < CUES.length && fake >= CUES[ci][0]) { bgmScene(CUES[ci][1]); ci++; }
      bgmSchedule();
    }

    const buf = await off.startRendering();
    // 16bit PCM の WAV に詰める
    const n = buf.length, ch = 2, bytes = n * ch * 2;
    const ab = new ArrayBuffer(44 + bytes), v = new DataView(ab);
    const ascii = (o, s) => { for (let i = 0; i < s.length; i++) v.setUint8(o + i, s.charCodeAt(i)); };
    ascii(0, "RIFF"); v.setUint32(4, 36 + bytes, true); ascii(8, "WAVEfmt ");
    v.setUint32(16, 16, true); v.setUint16(20, 1, true); v.setUint16(22, ch, true);
    v.setUint32(24, SR, true); v.setUint32(28, SR * ch * 2, true);
    v.setUint16(32, ch * 2, true); v.setUint16(34, 16, true);
    ascii(36, "data"); v.setUint32(40, bytes, true);
    const L = buf.getChannelData(0), R = buf.getChannelData(1);
    let o = 44;
    for (let i = 0; i < n; i++) {
      for (const d of [L, R]) {
        let x = Math.max(-1, Math.min(1, d[i]));
        v.setInt16(o, x < 0 ? x * 0x8000 : x * 0x7fff, true); o += 2;
      }
    }
    let bin = "", u8 = new Uint8Array(ab);
    for (let i = 0; i < u8.length; i += 8192) bin += String.fromCharCode.apply(null, u8.subarray(i, i + 8192));
    return btoa(bin);
  }, { SEC, CUES });

  fs.writeFileSync(OUT, Buffer.from(b64, "base64"));
  console.log("書き出し:", OUT, (fs.statSync(OUT).size / 1024 / 1024).toFixed(2), "MB");
  await browser.close();
})();
