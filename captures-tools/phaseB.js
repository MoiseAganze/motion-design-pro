const L = require('./lib');
const step = async (name, fn) => { try { await fn(); } catch (e) { console.error('FAIL', name, e.message.split('\n')[0]); throw e; } };
async function compter(page, devise, coupures) {
  for (const [v, n] of Object.entries(coupures)) {
    await page.getByLabel(new RegExp(`^Nombre de coupures de ${v}(\\.00)? ${devise}$`)).fill(String(n));
  }
}
(async () => {
  await L.start();
  const cai = await L.login('caissier');
  await step('session', async () => {
    await cai.goto(L.BASE + '/caisse');
    await compter(cai, 'CDF', { 20000: 491, 10000: 1, 5000: 1, 1000: 1, 500: 1 });
    await compter(cai, 'USD', { 100: 8 });
    await L.shot(cai, 'a20c-billetage-conforme', { full: true });
    await cai.getByRole('button', { name: 'Ouvrir la session' }).click();
    await cai.getByText('Session ouverte : vous pouvez opérer.').waitFor();
    await L.shot(cai, 'a21-session-ouverte');
    await L.shot(cai, 'a21b-session-ouverte-full', { full: true });
  });
  await L.browser.close();
})().catch(e => { console.error(e.message); process.exit(1); });
