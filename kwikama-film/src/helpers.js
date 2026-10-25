/* ---- shared helpers (inlined into every act by tools/build.mjs) ---- */
const K = 1400 / 1440;            // page px -> screen px
const SCR = { x: 260, y: 94 };    // screen top-left inside .cam at scale 1
function sp(sx, sy) { return { X: SCR.x + sx * K, Y: SCR.y + sy * K }; }
// camera vars that put page point (sx, sy) of the Mac screen at frame point (fx, fy) with scale S
function camAt(sx, sy, S, fx, fy, extra) {
  const p = sp(sx, sy); fx = fx === undefined ? 960 : fx; fy = fy === undefined ? 540 : fy;
  return Object.assign({ x: fx - 960 - S * (p.X - 960), y: fy - 540 - S * (p.Y - 540), scale: S, rotationX: 0, rotationY: 0 }, extra || {});
}
// cursor tip at page point (sx, sy) inside the screen
function curPos(sx, sy) { return { x: sx * K - 3, y: sy * K - 3 }; }
function click(tl, cur, t) {
  tl.to(cur, { scale: 0.8, duration: 0.07, ease: "power2.out" }, t);
  tl.to(cur, { scale: 1, duration: 0.16, ease: "power2.out" }, t + 0.07);
}
// show one screen layer at time t (instant swap, like the real UI)
function swap(tl, from, to, t, fade) {
  if (fade) { tl.to(to, { opacity: 1, duration: fade, ease: "none" }, t); if (from) tl.set(from, { opacity: 0 }, t + fade); }
  else { tl.set(to, { opacity: 1 }, t); if (from) tl.set(from, { opacity: 0 }, t); }
}
// words: blur-in one by one
function wordsIn(tl, els, t, gap, dur) {
  gap = gap === undefined ? 0.07 : gap; dur = dur || 0.32;
  tl.fromTo(els, { opacity: 0, filter: "blur(10px)" }, { opacity: 1, filter: "blur(0px)", duration: dur, ease: "power2.out", stagger: gap }, t);
}
function wordsOut(tl, els, t, dur) {
  tl.to(els, { opacity: 0, filter: "blur(10px)", duration: dur || 0.22, ease: "power2.in", stagger: 0.03 }, t);
}
// odometer number: build digit strips inside el for the string `str`; returns strips
function odo(el, str, h) {
  el.innerHTML = "";
  const strips = [];
  for (const ch of str) {
    if (/\d/.test(ch)) {
      const d = document.createElement("span"); d.className = "digit"; d.style.height = h + "px";
      const s = document.createElement("span"); s.className = "strip";
      for (let k = 0; k <= 19; k++) { const n = document.createElement("span"); n.textContent = k % 10; n.style.height = h + "px"; n.style.lineHeight = h + "px"; s.appendChild(n); }
      d.appendChild(s); el.appendChild(d); strips.push({ s, v: +ch });
    } else { const n = document.createElement("span"); n.textContent = ch; n.style.display = "inline-block"; n.style.lineHeight = h + "px"; el.appendChild(n); }
  }
  return strips;
}
// roll strips from 0 to their digit (plus one full turn) between t and t+dur
function odoRoll(tl, strips, h, t, dur) {
  strips.forEach((o, i) => {
    tl.fromTo(o.s, { y: 0 }, { y: -(10 + o.v) * h, duration: dur - i * 0.04, ease: "power3.out" }, t + i * 0.04);
  });
}
// mulberry32 PRNG
function rng(seed) { return function () { seed |= 0; seed = seed + 0x6D2B79F5 | 0; let t = Math.imul(seed ^ seed >>> 15, 1 | seed); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; }; }
