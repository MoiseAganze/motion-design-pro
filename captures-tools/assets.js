const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 600, height: 600 } });
  await p.setContent(`<body style="margin:0"><svg width="600" height="600" viewBox="0 0 600 600" xmlns="http://www.w3.org/2000/svg">
  <defs><linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#dbe7f3"/><stop offset="1" stop-color="#b9cde3"/></linearGradient></defs>
  <rect width="600" height="600" fill="url(#bg)"/>
  <path d="M90 600 C110 470 200 420 300 420 C400 420 490 470 510 600Z" fill="#1f4e79"/>
  <path d="M250 420 L300 500 L350 420Z" fill="#f4f1ea"/>
  <rect x="262" y="330" width="76" height="100" rx="30" fill="#6b4226"/>
  <ellipse cx="300" cy="260" rx="105" ry="125" fill="#7a4b2c"/>
  <path d="M195 230 C195 140 250 120 300 120 C360 120 410 150 405 235 C395 190 360 175 300 178 C240 180 205 195 195 230Z" fill="#1b1410"/>
  <ellipse cx="262" cy="265" rx="9" ry="11" fill="#1b1410"/><ellipse cx="338" cy="265" rx="9" ry="11" fill="#1b1410"/>
  <path d="M265 325 Q300 350 335 325" stroke="#3b2214" stroke-width="7" fill="none" stroke-linecap="round"/>
  <ellipse cx="195" cy="270" rx="16" ry="26" fill="#6e4327"/><ellipse cx="405" cy="270" rx="16" ry="26" fill="#6e4327"/>
  </svg></body>`);
  await p.screenshot({ path: 'photo-membre.png', clip: { x: 0, y: 0, width: 600, height: 600 } });
  await p.setViewportSize({ width: 800, height: 300 });
  await p.setContent(`<body style="margin:0;background:#fff"><svg width="800" height="300" xmlns="http://www.w3.org/2000/svg"><path d="M60 200 C90 80 140 80 130 170 C120 250 170 120 210 110 C250 100 200 220 250 200 C300 180 300 120 340 130 C380 140 330 220 380 210 C430 200 440 120 480 140 C520 160 470 230 530 200 C590 170 620 150 700 160" stroke="#14213d" stroke-width="7" fill="none" stroke-linecap="round" stroke-linejoin="round"/><path d="M120 235 L640 225" stroke="#14213d" stroke-width="4" stroke-linecap="round"/></svg></body>`);
  await p.screenshot({ path: 'signature.png' });
  await b.close();
})();
