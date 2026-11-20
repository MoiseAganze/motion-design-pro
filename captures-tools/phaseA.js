const L = require('./lib');
const step = async (name, fn) => { try { await fn(); } catch (e) { console.error('FAIL', name, e.message.split('\n')[0]); throw e; } };
(async () => {
  const b = await L.start();
  // Login screen
  const ctx0 = await b.newContext({ viewport: { width: 1536, height: 864 }, deviceScaleFactor: 2, locale: 'fr-FR' });
  const p0 = await ctx0.newPage(); await p0.goto(L.BASE + '/connexion');
  await L.shot(p0, 'a01-connexion');
  await p0.locator('#identifiant').fill('directeur'); await p0.locator('#motDePasse').fill('Guichet-Bandal-2026');
  await L.shot(p0, 'a02-connexion-remplie');
  // wrong password demo for security
  await p0.locator('#motDePasse').fill('mauvais-mot'); await p0.locator('button[type=submit]').click(); await p0.waitForTimeout(1200);
  await L.shot(p0, 'a03-connexion-refusee');
  await ctx0.close();

  const dir = await L.login('directeur');
  await L.shot(dir, 'a10-dashboard-directeur');
  await step('ouvrir journee', async () => {
    await dir.goto(L.BASE + '/caisse'); await L.shot(dir, 'a11-caisse-journee-fermee');
    await dir.getByRole('button', { name: 'Ouvrir la journée' }).click();
    await dir.getByText('Journée ouverte').first().waitFor();
    await L.shot(dir, 'a12-journee-ouverte');
  });
  const cai = await L.login('caissier');
  await step('session', async () => {
    await cai.goto(L.BASE + '/caisse'); await L.shot(cai, 'a20-caisse-ouvrir-session');
    await L.shot(cai, 'a20b-caisse-ouvrir-session-full', { full: true });
    await cai.getByRole('button', { name: 'Ouvrir la session' }).click();
    await cai.getByText('Session ouverte : vous pouvez opérer.').waitFor();
    await L.shot(cai, 'a21-session-ouverte');
    await L.shot(cai, 'a21b-session-ouverte-full', { full: true });
  });
  await b.close();
})().catch(e => { console.error(e.message); process.exit(1); });
