const L = require('./lib'); const fs = require('fs');
const st = JSON.parse(fs.readFileSync('state.json'));
const step = async (name, fn) => { try { await fn(); } catch (e) { console.error('FAIL', name, e.message.split('\n')[0]); throw e; } };
(async () => {
  await L.start();
  const c = await L.login('caissier');
  const dir = await L.login('directeur');
  await step('retrait', async () => {
    await c.goto(L.BASE + st.compte);
    await L.shot(c, 'f00-compte-solde');
    await c.getByRole('button', { name: 'Retrait' }).click();
    const d = c.getByRole('dialog');
    await d.getByLabel('Montant').fill('600000');
    await c.waitForTimeout(600);
    await L.shot(c, 'f01-retrait-photo-signature');
    await d.getByRole('button', { name: 'Décaisser' }).click();
    await c.waitForTimeout(2000);
    await L.shot(c, 'f02-retrait-en-attente');
    console.log((await c.locator('[data-sonner-toast], [role=status]').allInnerTexts()).join(' | '));
    await c.goto(L.BASE + '/caisse'); await L.shot(c, 'f03-caisse-attente');
  });
  await step('validation', async () => {
    await dir.goto(L.BASE + '/caisse/supervision');
    await L.shot(dir, 'f10-supervision'); await L.shot(dir, 'f10b-supervision-full', { full: true });
    const t = await dir.locator('main').innerText(); console.log(t.slice(0, 1500));
  });
  await L.browser.close();
})().catch(e => { console.error(e.message); process.exit(1); });
