const L = require('./lib'); const fs = require('fs');
const st = JSON.parse(fs.readFileSync('state.json'));
const step = async (name, fn) => { try { await fn(); } catch (e) { console.error('FAIL', name, e.message.split('\n')[0]); throw e; } };
(async () => {
  await L.start();
  const c = await L.login('caissier');
  const dir = await L.login('directeur');
  await step('caissier ne peut valider', async () => {
    await c.goto(L.BASE + '/caisse/supervision'); await L.shot(c, 'f05-caissier-acces-refuse');
  });
  await step('approuver', async () => {
    await dir.goto(L.BASE + '/caisse/supervision');
    await dir.getByRole('button', { name: 'Approuver' }).first().click();
    await dir.waitForTimeout(800);
    await L.shot(dir, 'f11-approuver-dialog');
    const dd = dir.getByRole('dialog');
    if (await dd.count()) { const btn = dd.getByRole('button', { name: /Approuver|Confirmer|Valider/ }).last(); await btn.click(); }
    await dir.waitForTimeout(1500);
    await L.shot(dir, 'f12-approuve');
  });
  await step('executer', async () => {
    await c.goto(L.BASE + '/caisse');
    await L.shot(c, 'f20-caisse-a-executer');
    const [recu] = await Promise.all([c.context().waitForEvent('page', { timeout: 15000 }), c.getByRole('button', { name: 'Exécuter' }).first().click().then(async () => { await c.waitForTimeout(500); const d = c.getByRole('dialog'); if (await d.count()) await d.getByRole('button', { name: /Exécuter|Décaisser|Confirmer/ }).last().click(); })]);
    await recu.setViewportSize({ width: 1536, height: 864 }); await recu.waitForLoadState('networkidle');
    await L.shot(recu, 'f21-recu-retrait'); await recu.close();
    await c.waitForTimeout(800); await L.shot(c, 'f22-caisse-apres-retrait');
  });
  await L.browser.close();
})().catch(e => { console.error(e.message); process.exit(1); });
