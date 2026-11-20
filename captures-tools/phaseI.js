const L = require('./lib');
const step = async (name, fn) => { try { await fn(); } catch (e) { console.error('FAIL', name, e.message.split('\n')[0]); } };
async function compter(page, devise, coupures) { for (const [v, n] of Object.entries(coupures)) await page.getByLabel(new RegExp(`^Nombre de coupures de ${v}(\\.00)? ${devise}$`)).fill(String(n)); }
(async () => {
  await L.start();
  const d = await L.login('directeur');
  await step('palette', async () => { await d.waitForTimeout(1500); await d.getByRole('button', { name: /Rechercher/ }).click(); await d.waitForTimeout(600); await d.keyboard.type('Mwang', { delay: 80 }); await d.waitForTimeout(2000); await L.shot(d, 'h23-palette'); await d.keyboard.press('Escape'); });
  const k = await L.login('comptable');
  await step('ecriture', async () => { await k.goto(L.BASE + '/comptabilite/ecritures'); await k.getByText(/Retrait|Dépôt sur|Déblocage/).first().click(); await k.waitForTimeout(1500); await L.shot(k, 'h02b-ecriture-auto'); console.log(k.url()); });
  const c = await L.login('caissier');
  await step('cloture', async () => {
    await c.goto(L.BASE + '/caisse');
    await c.getByRole('button', { name: 'Clôturer' }).click(); await c.waitForTimeout(800);
    await compter(c, 'CDF', { 20000: 500, 10000: 1, 1000: 1, 500: 1 }); await compter(c, 'USD', { 100: 8 });
    await c.waitForTimeout(500);
    await L.shot(c, 'i01-cloture-billetage'); await L.shot(c, 'i01b-cloture-billetage-full', { full: true });
    const dlg = c.getByRole('dialog');
    const scope = (await dlg.count()) ? dlg : c.locator('main');
    await scope.getByRole('button', { name: /Demander la clôture|Clôturer|Envoyer/ }).last().click();
    await c.waitForTimeout(2000); await L.shot(c, 'i02-cloture-demandee');
  });
  await step('valider cloture', async () => {
    await d.goto(L.BASE + '/caisse/supervision'); await L.shot(d, 'i10-supervision-cloture');
    console.log((await d.locator('main').innerText()).slice(0, 900));
  });
  await L.browser.close();
})().catch(e => { console.error(e.message); process.exit(1); });
