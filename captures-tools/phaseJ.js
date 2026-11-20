const L = require('./lib');
const step = async (name, fn) => { try { await fn(); } catch (e) { console.error('FAIL', name, e.message.split('\n')[0]); } };
(async () => {
  await L.start();
  const d = await L.login('directeur');
  await step('valider', async () => {
    await d.goto(L.BASE + '/caisse/supervision');
    await d.getByRole('button', { name: 'Valider' }).first().click(); await d.waitForTimeout(800);
    await L.shot(d, 'i11-valider-cloture');
    const dl = d.getByRole('dialog'); if (await dl.count()) await dl.getByRole('button', { name: /Valider|Confirmer/ }).last().click();
    await d.waitForTimeout(2000); await L.shot(d, 'i12-cloture-validee');
  });
  await step('fermer', async () => {
    await d.getByRole('button', { name: 'Fermer la journée' }).click(); await d.waitForTimeout(800);
    await L.shot(d, 'i13-fermer-journee-dialog');
    const dl = d.getByRole('dialog'); if (await dl.count()) await dl.getByRole('button', { name: /Fermer/ }).last().click();
    await d.waitForTimeout(4000); await L.shot(d, 'i14-journee-fermee');
    console.log((await d.locator('[data-sonner-toast]').allInnerTexts()).join('|'));
  });
  await step('dash', async () => { await d.goto(L.BASE + '/tableau-de-bord'); await L.shot(d, 'i20-dashboard-fin'); await L.shot(d, 'i20b-dashboard-fin-full', { full: true }); });
  const k = await L.login('comptable');
  await step('ecriture', async () => { await k.goto(L.BASE + '/comptabilite/ecritures'); const r = k.locator('main tbody tr').filter({ hasText: /Retrait|Déblocage|Dépôt/ }).first(); await r.click(); await k.waitForTimeout(1500); console.log(k.url()); await L.shot(k, 'h02b-ecriture-auto'); });
  await L.browser.close();
})().catch(e => { console.error(e.message); process.exit(1); });
