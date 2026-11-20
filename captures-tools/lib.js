const { chromium } = require('playwright');
const fs = require('fs'); const path = require('path');
const BASE = 'http://localhost:3000';
const PW = 'Guichet-Bandal-2026';
const OUT = process.env.OUT || '/home/user/motion-design-pro/coopecplus-video/captures';
fs.mkdirSync(OUT, { recursive: true });
const HIDE = `[data-demo-banner], .bandeau-demo { display:none !important }`;
let browser;
async function start() { browser = await chromium.launch(); return browser; }
async function login(id, pw = PW) {
  const ctx = await browser.newContext({ viewport: { width: 1536, height: 864 }, deviceScaleFactor: 2, locale: 'fr-FR', timezoneId: 'Africa/Lubumbashi' });
  await ctx.addInitScript(() => { const st = () => { if (document.getElementById('__hb')) return; const e = document.createElement('style'); e.id='__hb'; e.textContent = '.bg-avertissement.uppercase{display:none!important} nextjs-portal{display:none!important}'; (document.head||document.documentElement).appendChild(e); }; document.addEventListener('DOMContentLoaded', st); st(); });
  const page = await ctx.newPage();
  await page.goto(BASE + '/connexion');
  await page.locator('#identifiant').fill(id);
  await page.locator('#motDePasse').fill(pw);
  await page.locator('button[type=submit]').click();
  await page.waitForURL(/tableau-de-bord|mot-de-passe/);
  return page;
}
async function shot(page, name, opts = {}) {
  await page.waitForLoadState('networkidle').catch(() => {});
  await page.waitForTimeout(opts.wait ?? 600);
  const f = path.join(OUT, name + '.png');
  await page.screenshot({ path: f, fullPage: !!opts.full });
  console.log('shot', name);
  return f;
}
module.exports = { start, login, shot, BASE, PW, OUT, get browser() { return browser; } };
