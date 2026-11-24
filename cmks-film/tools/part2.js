const { chromium } = require('playwright');
const OUT = process.argv[2];
const B='https://cmks.therapeutique.online/';
(async () => {
  const b = await chromium.launch();
  const ctx = await b.newContext({ viewport: { width: 1440, height: 900 }, deviceScaleFactor: 2 });
  const p = await ctx.newPage();
  p.on('dialog', d=>d.accept());
  const go = async (u)=>{ await p.goto(B+u,{waitUntil:'networkidle'}); await p.waitForTimeout(900); };
  const snap = async (n, opt={})=>{ await p.screenshot({ path: `${OUT}/${n}.png`, ...opt }); console.log('shot',n); };
  const login = async (who)=>{ await ctx.clearCookies(); await go('index.php?r=connexion'); await p.getByText('Essayer avec un compte de démonstration').click(); await p.getByRole('button', { name: new RegExp(who) }).click(); await p.waitForLoadState('networkidle'); await p.waitForTimeout(700); };
  const killToast = ()=>p.evaluate(()=>{ for (const el of document.querySelectorAll('body *')) { const s=getComputedStyle(el); if (s.position==='fixed' && /Session ouverte|Rendez-vous planifié/.test(el.innerText||'') ) el.remove(); }});
  await login('Nadine');
  await go('index.php?r=demandes'); await killToast(); await snap('acc-list');
  await go('index.php?r=demandes&id=DR-0002'); await killToast(); await snap('acc-detail');
  await p.getByText('Planifier le rendez-vous').click(); await p.waitForTimeout(400);
  const f = p.locator('form:has(input[name=operation][value=planifier])');
  await f.locator('select[name=intervenant]').selectOption('U-K3');
  await f.locator('textarea[name=note]').fill('Rappelé, bilan initial jeudi 9 h.');
  await f.scrollIntoViewIfNeeded(); await p.waitForTimeout(300); await snap('acc-plan-form');
  await f.locator('button').click(); await p.waitForLoadState('networkidle'); await p.waitForTimeout(900); await snap('acc-planned');
  await killToast(); await snap('acc-planned-clean');
  // direction
  await login('Bernard'); await snap('dir-dash-toast'); await killToast(); await snap('dir-dash');
  await go('index.php?r=partenaires'); await snap('dir-part');
  await go('index.php?r=partenaires&action=nouveau'); await snap('dir-part-new');
  await go('index.php?r=partenaires');
  await p.locator('form:has(input[name=id][value=PA-002]):has(input[value=avant]) button').click(); await p.waitForLoadState('networkidle'); await p.waitForTimeout(900); await snap('dir-part-toggled');
  await killToast(); await snap('dir-part-toggled-clean');
  await go(''); await snap('home-toggled');
  await go('index.php?r=partenaires');
  await p.locator('form:has(input[name=id][value=PA-002]):has(input[value=avant]) button').click(); await p.waitForLoadState('networkidle'); await p.waitForTimeout(900);
  console.log('RESTORED:', (await p.evaluate(()=>document.querySelector('main').innerText)).replace(/\s+/g,' ').slice(0,500));
  await go(''); await snap('home-restored');
  for (const [who,slug] of [['Espérant','kine'],['Aimée','medecin'],['Ruth','nutri'],['Merveille','coach'],['Fiston','caisse']]) {
    await login(who); await snap('mod-'+slug+'-toast'); await killToast(); await snap('mod-'+slug);
  }
  await b.close();
})();
