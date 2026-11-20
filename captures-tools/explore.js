const L = require('./lib');
(async () => {
  await L.start();
  const p = await L.login('directeur');
  await L.shot(p, 'x-dashboard-directeur');
  await L.shot(p, 'x-dashboard-directeur-full', { full: true });
  await p.goto(L.BASE + '/connexion'); 
  await L.browser.close();
})().catch(e => { console.error(e); process.exit(1); });
