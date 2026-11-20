const L = require('./lib');
(async () => {
  await L.start();
  const c = await L.login('caissier');
  await c.goto(L.BASE + '/caisse');
  const pages = []; c.context().on('page', p => pages.push(p));
  const ex = c.getByRole('button', { name: 'Exécuter' });
  console.log('exec buttons', await ex.count());
  if (await ex.count()) { await ex.first().click(); await c.waitForTimeout(1500); await L.shot(c, 'f20b-executer-clic');
    const d = c.getByRole('dialog'); if (await d.count()) { console.log(await d.innerText()); await d.getByRole('button').last().click(); await c.waitForTimeout(2000); } }
  console.log('pages', pages.length);
  for (const r of pages) { await r.setViewportSize({ width: 1536, height: 864 }); await r.waitForLoadState('networkidle'); await L.shot(r, 'f21-recu-retrait'); }
  await c.waitForTimeout(800); await L.shot(c, 'f22-caisse-apres-retrait');
  await L.browser.close();
})().catch(e => { console.error(e.message); process.exit(1); });
