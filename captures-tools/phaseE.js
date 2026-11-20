const L = require('./lib'); const fs = require('fs');
const st = JSON.parse(fs.readFileSync('state.json'));
const step = async (name, fn) => { try { await fn(); } catch (e) { console.error('FAIL', name, e.message.split('\n')[0]); throw e; } };
(async () => {
  await L.start();
  const a = await L.login('admin', 'Lac-Kivu-Securise-2026');
  await step('user', async () => {
    await a.goto(L.BASE + '/administration/utilisateurs/nouveau');
    await a.locator('#identifiant').fill('neema');
    await a.locator('#nomComplet').fill('Neema Bahizire');
    await a.locator('#telephone').fill('0991234567');
    await a.locator('label', { hasText: 'Opérations de guichet' }).first().click();
    await a.locator('label', { hasText: 'Guichet 1' }).first().click();
    await L.shot(a, 'e01-nouvel-utilisateur'); await L.shot(a, 'e01b-nouvel-utilisateur-full', { full: true });
    await a.getByRole('button', { name: "Créer l'utilisateur" }).click();
    await a.waitForTimeout(2000);
    await L.shot(a, 'e02-utilisateur-cree'); await L.shot(a, 'e02b-utilisateur-cree-full', { full: true });
    console.log((await a.locator('body').innerText()).slice(0, 800));
  });
  await step('seuil', async () => {
    await a.goto(L.BASE + '/parametres/validation');
    await a.getByText('Nouveau seuil').first().click();
    const d = a.getByRole('dialog');
    await d.locator('#champ-seuilMontant').fill('500000');
    await L.shot(a, 'e03-nouveau-seuil');
    await d.getByRole('button', { name: 'Enregistrer' }).click();
    await a.waitForTimeout(1500);
    await L.shot(a, 'e04-seuil-enregistre');
  });
  await L.browser.close();
})().catch(e => { console.error(e.message); process.exit(1); });
