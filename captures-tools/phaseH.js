const L = require('./lib');
const step = async (name, fn) => { try { await fn(); } catch (e) { console.error('FAIL', name, e.message.split('\n')[0]); } };
(async () => {
  await L.start();
  const k = await L.login('comptable');
  await L.shot(k, 'h00-dashboard-comptable');
  for (const [u, n] of [['/comptabilite/ecritures','h01-ecritures'],['/comptabilite/balance','h03-balance'],['/comptabilite/etats','h04-etats'],['/comptabilite/grand-livre','h05-grand-livre'],['/comptabilite/clotures','h06-clotures'],['/epargne/traitements','h07-interets']]) {
    await step(n, async () => { await k.goto(L.BASE + u); await L.shot(k, n); });
  }
  await step('ecriture detail', async () => { await k.goto(L.BASE + '/comptabilite/ecritures'); await k.locator('main table tbody tr a, main a[href*="/comptabilite/ecritures/"]').first().click(); await k.waitForTimeout(1000); await L.shot(k, 'h02-ecriture-detail'); });
  const a = await L.login('auditeur');
  await L.shot(a, 'h10-dashboard-auditeur');
  await step('audit', async () => {
    await a.goto(L.BASE + '/administration/audit'); await L.shot(a, 'h11-journal-audit');
    const b = a.getByRole('button', { name: /Vérifier l'intégrité/ });
    await b.click(); await a.waitForTimeout(2500); await L.shot(a, 'h12-audit-integrite-ok');
    console.log((await a.locator('[data-sonner-toast]').allInnerTexts()).join('|'));
  });
  await step('integrite', async () => {
    await a.goto(L.BASE + '/administration/integrite'); await L.shot(a, 'h13-controles');
    const b = a.getByRole('button', { name: /Lancer|Exécuter|contrôles/ }).first();
    if (await b.count()) { await b.click(); await a.waitForTimeout(5000); }
    await L.shot(a, 'h14-controles-ok'); await L.shot(a, 'h14b-controles-ok-full', { full: true });
  });
  await step('audit-modif-refus', async () => { await a.goto(L.BASE + '/membres/nouveau'); await L.shot(a, 'h15-auditeur-lecture-seule'); });
  const d = await L.login('directeur');
  await L.shot(d, 'h20-dashboard-directeur'); await L.shot(d, 'h20b-dashboard-directeur-full', { full: true });
  await step('rapports', async () => { await d.goto(L.BASE + '/rapports'); await L.shot(d, 'h21-rapports');
    await d.locator('main a[href^="/rapports/"]').first().click(); await d.waitForTimeout(1500); await L.shot(d, 'h22-rapport'); });
  await step('palette', async () => { await d.goto(L.BASE + '/tableau-de-bord'); await d.keyboard.press('Control+k'); await d.waitForTimeout(500); await d.keyboard.type('Mwang', { delay: 60 }); await d.waitForTimeout(1500); await L.shot(d, 'h23-palette'); });
  await step('manuel', async () => { await d.goto(L.BASE + '/manuels'); await L.shot(d, 'h24-manuel'); });
  await step('membres', async () => { await d.goto(L.BASE + '/membres'); await L.shot(d, 'h25-liste-membres'); });
  await step('credits', async () => { await d.goto(L.BASE + '/credits'); await L.shot(d, 'h26-portefeuille'); });
  await L.browser.close();
})().catch(e => { console.error(e.message); process.exit(1); });
