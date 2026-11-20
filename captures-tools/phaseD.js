const L = require('./lib');
(async () => {
  await L.start();
  const a = await L.login('admin', 'Initial-Kivu-2026!');
  await a.locator('#actuel').fill('Initial-Kivu-2026!');
  await a.locator('#nouveau').fill('Lac-Kivu-Securise-2026');
  await a.locator('#confirmation').fill('Lac-Kivu-Securise-2026');
  await L.shot(a, 'd02-admin-mdp-rempli');
  await a.locator('button[type=submit]').click();
  await a.waitForURL(/tableau-de-bord/, { timeout: 15000 }).catch(()=>{});
  await L.shot(a, 'd04-admin-dashboard');
  for (const [u, n] of [['/administration/utilisateurs','d10-utilisateurs'],['/administration/roles','d11-roles'],['/administration/sessions','d12-sessions'],['/administration/connexions','d13-connexions'],['/parametres/validation','d14-seuils'],['/parametres','d15-parametres'],['/parametres/produits-credit','d16-produits-credit']]) {
    await a.goto(L.BASE + u); await L.shot(a, n);
  }
  const h = await a.locator('main').innerText(); console.log(h.slice(0, 1500));
  await L.browser.close();
})().catch(e => { console.error(e.message); process.exit(1); });
