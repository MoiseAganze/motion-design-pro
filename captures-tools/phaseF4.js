const L = require('./lib');
(async () => {
  await L.start();
  const c = await L.login('caissier');
  await c.goto(L.BASE + '/caisse');
  console.log((await c.locator('body').innerText()).slice(-900)); console.log(await c.locator('main a, main button').evaluateAll(es=>es.map(e=>e.tagName+':'+(e.getAttribute('aria-label')||e.innerText.trim())).slice(0,40)));
  const [r] = await Promise.all([c.context().waitForEvent('page'), c.getByRole('link', { name: /Imprimer|Reçu|reçu/ }).first().click().catch(async () => { await c.locator('main a[target=_blank], main button[aria-label*=eçu], main a[aria-label*=eçu]').first().click(); })]);
  await r.setViewportSize({ width: 1536, height: 864 }); await r.waitForLoadState('networkidle');
  await L.shot(r, 'f21-recu-retrait');
  await L.browser.close();
})().catch(e => { console.error(e.message); process.exit(1); });
