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
  const scrollTo = async (sel, off=0)=>{ await p.evaluate(([s,o])=>{let e=null; try{e=document.querySelector(s)}catch(_){}; e=e||[...document.querySelectorAll('h2,h1')].find(h=>h.innerText.toUpperCase().includes(s)); window.scrollTo(0, e.getBoundingClientRect().top+scrollY-o);},[sel,off]); await p.waitForTimeout(700); };
  const hideFab = async()=>{ await p.addStyleTag({content:'.fixed.bottom-6, a[aria-label*=WhatsApp].fixed{opacity:1}'}); };
  // public
  await go(''); await snap('home');
  await scrollTo('NOS 8 PÔLES', 40); await snap('home-poles');
  await go('index.php?r=services'); await snap('services');
  await p.evaluate(()=>window.scrollTo(0,document.body.scrollHeight)); await p.waitForTimeout(600); await snap('services-end');
  await go('index.php?r=pole&p=restauration'); await snap('pole-resto');
  await go('index.php?r=service&s=kinesitherapie-reeducation'); await snap('service-kine');
  await go('index.php?r=rendez-vous'); await p.evaluate(()=>window.scrollTo(0,250)); await p.waitForTimeout(400); await snap('rdv-empty');
  await p.selectOption('select[name=pole]','kinesitherapie');
  await p.selectOption('select[name=service]','reeducation-orthopedique');
  await p.fill('input[name=prenom]','Joël'); await p.fill('input[name=nom]','Mabiala');
  await p.fill('input[name=telephone]','+243 810 000 000'); await p.fill('input[name=date]','2026-11-26');
  await p.selectOption('select[name=moment]','matin');
  await p.fill('textarea[name=motif]','Entorse de la cheville au football, ordonnance de 10 séances.');
  await p.check('input[name=consentement]');
  await p.evaluate(()=>window.scrollTo(0,250)); await p.waitForTimeout(300); await snap('rdv-filled');
  await p.evaluate(()=>window.scrollTo(0,700)); await p.waitForTimeout(300); await snap('rdv-filled-bottom');
  await p.getByRole('button',{name:/Envoyer ma/}).click(); await p.waitForLoadState('networkidle'); await p.waitForTimeout(800); await snap('rdv-sent');
  // login page
  await go('index.php?r=connexion'); await snap('login');
  await p.getByText('Essayer avec un compte de démonstration').click(); await p.waitForTimeout(600);
  await p.evaluate(()=>window.scrollTo(0,150)); await p.waitForTimeout(300); await snap('login-demo');
  await p.getByRole('button', { name: /Nadine/ }).click(); await p.waitForLoadState('networkidle'); await p.waitForTimeout(600);
  await p.evaluate(()=>document.querySelectorAll('[role=status],[class*=toast]').forEach(e=>e.remove()));
  await go('index.php?r=demandes'); await snap('acc-list');
  await go('index.php?r=demandes&id=DR-0001'); await snap('acc-detail');
  await p.getByText('Planifier le rendez-vous').click(); await p.waitForTimeout(400);
  const f = p.locator('form:has(input[name=operation][value=planifier])');
  await f.locator('select[name=intervenant]').selectOption('U-K3');
  await f.locator('textarea[name=note]').fill('Rappelé, bilan initial jeudi 9 h.');
  await f.scrollIntoViewIfNeeded(); await p.waitForTimeout(300); await snap('acc-plan-form');
  await f.locator('button').click(); await p.waitForLoadState('networkidle'); await p.waitForTimeout(900); await snap('acc-planned');
  await p.waitForTimeout(6000); await snap('acc-planned-clean');
  // direction
  await go('index.php?r=deconnexion').catch(()=>{});
  await ctx.clearCookies();
  await go('index.php?r=connexion');
  await p.getByText('Essayer avec un compte de démonstration').click();
  await p.getByRole('button', { name: /Bernard/ }).click(); await p.waitForLoadState('networkidle'); await p.waitForTimeout(7000); await snap('dir-dash');
  await go('index.php?r=partenaires'); await snap('dir-part');
  await go('index.php?r=partenaires&action=nouveau'); await snap('dir-part-new');
  await p.fill('input[name=nom]','Nouveau partenaire'); await p.fill('input[name=sigle]','NP');
  await p.fill('textarea[name=description]','Présentation officielle du partenaire.');
  await snap('dir-part-new-filled');
  await p.locator('form:has(input[name=action][value=partenaire_enregistrer]) button[type=submit]').click(); await p.waitForLoadState('networkidle'); await p.waitForTimeout(900); await snap('dir-part-saved');
  await go(''); await snap('home-after-part');
  await scrollTo('NOS PARTENAIRES', 40); await snap('home-partners-after');
  // modules
  for (const [who,slug] of [['Espérant','kine'],['Aimée','medecin'],['Ruth','nutri'],['Merveille','coach'],['Fiston','caisse'],['Nadine','accueil']]) {
    await ctx.clearCookies();
    await go('index.php?r=connexion');
    await p.getByText('Essayer avec un compte de démonstration').click();
    await p.getByRole('button', { name: new RegExp(who) }).click(); await p.waitForLoadState('networkidle'); await p.waitForTimeout(700);
    await snap('mod-'+slug+'-toast');
    await p.waitForTimeout(6000); await snap('mod-'+slug);
  }
  await b.close();
})();
