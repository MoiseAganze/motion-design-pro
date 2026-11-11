// V2 captures of kwikamademo.vercel.app at 2x, demo message hidden, with element boxes (page px)
const { chromium } = require('playwright');
const fs = require('fs');
const OUT = process.argv[2] || 'final/';
fs.mkdirSync(OUT, { recursive: true });
const boxes = {};
let browser;
const BASE = 'https://kwikamademo.vercel.app';

async function login(role) {
  const ctx = await browser.newContext({ viewport: { width: 1440, height: 900 }, deviceScaleFactor: 2 });
  const page = await ctx.newPage();
  await page.goto(BASE + '/connexion', { waitUntil: 'networkidle', timeout: 60000 });
  await page.locator('button', { hasText: role }).first().click();
  await page.waitForLoadState('networkidle'); await page.waitForTimeout(1500);
  const m = page.locator('button', { hasText: 'Masquer le message' });
  if (await m.count()) { await m.first().click(); await page.waitForTimeout(500); }
  return page;
}
async function nav(page, href) {
  await page.locator(`a[href="${href}"]`).first().click();
  await page.waitForLoadState('networkidle'); await page.waitForTimeout(1200);
  await page.evaluate(() => window.scrollTo(0, 0)); await page.waitForTimeout(300);
}
// boxes of elements; css or text match (deepest), optional closest(); coordinates in document px
async function find(page, specs) {
  return await page.evaluate((specs) => {
    const out = {};
    for (const [key, sp] of Object.entries(specs)) {
      let els = [];
      if (sp.css) els = Array.from(document.querySelectorAll(sp.css));
      if (sp.text) {
        const all = Array.from(document.querySelectorAll(sp.within || 'body *'));
        els = all.filter(e => {
          if (e.offsetParent === null && getComputedStyle(e).position !== 'fixed') return false;
          const t = (e.innerText || e.textContent || '').trim().replace(/\s+/g, ' ');
          if (!t) return false;
          return sp.exact ? t === sp.text : t.includes(sp.text);
        });
        els = els.filter(e => !els.some(o => o !== e && e.contains(o)));
      }
      if (sp.closest) els = els.map(e => e.closest(sp.closest)).filter(Boolean);
      els = els.filter(e => { const r = e.getBoundingClientRect(); return r.width > 0 && r.height > 0; });
      const e = els[sp.nth || 0];
      if (!e) { out[key] = null; continue; }
      const r = e.getBoundingClientRect();
      out[key] = { x: Math.round(r.x + window.scrollX), y: Math.round(r.y + window.scrollY), w: Math.round(r.width), h: Math.round(r.height) };
    }
    return out;
  }, specs);
}
async function shot(page, name, specs, full = false) {
  await page.waitForTimeout(300);
  await page.screenshot({ path: OUT + name + '.png', fullPage: full });
  if (specs) boxes[name] = await find(page, specs);
  console.log('shot', name, JSON.stringify(boxes[name] || {}).slice(0, 400));
}
const NAV = {
  n_home: { css: 'a[href="/app"]', nth: 1 }, n_verif: { css: 'a[href="/app/verification"]' }, n_preuves: { css: 'a[href="/app/preuves"]' },
  n_analyse: { css: 'a[href="/app/analyse"]' }, n_coord: { text: 'Coordination des institutions', within: 'aside *, nav *' },
  n_avoirs: { css: 'a[href="/app/avoirs"]' }, n_switch: { text: 'Changer de rôle', within: 'aside *, nav *' },
  steps: { text: 'Le contrôle de légalité', within: 'main *, body *', nth: 0 }
};

(async () => {
  browser = await chromium.launch();
  // landing + workstation choice
  let ctx = await browser.newContext({ viewport: { width: 1440, height: 900 }, deviceScaleFactor: 2 });
  let p = await ctx.newPage();
  await p.goto(BASE + '/', { waitUntil: 'networkidle' }); await p.waitForTimeout(1500);
  await shot(p, 'landing', { h1: { css: 'h1' } });
  await p.goto(BASE + '/connexion', { waitUntil: 'networkidle' }); await p.waitForTimeout(1200);
  await shot(p, 'connexion', {
    w_parquet: { text: 'Magistrat du Parquet', closest: 'button' }, w_coord: { text: 'Coordonnateur UNICEP', closest: 'button' }, w_cenaref: { text: 'Point focal CENAREF', closest: 'button' },
    title: { css: 'h1, h2', nth: 0 }
  }, true);
  await ctx.close();

  // ---------- Magistrat du Parquet ----------
  p = await login('Magistrat du Parquet');
  await shot(p, 'm_home', Object.assign({ kpi1: { text: 'PRÉJUDICE ÉTABLI', closest: 'div' }, persona: { text: 'Mulumba Kanyinda Victor', nth: 0 }, badge: { text: 'aucun scellé rompu', exact: true } }, NAV));
  // scroll behaviour probe
  await p.evaluate(() => window.scrollTo(0, 500)); await p.waitForTimeout(400);
  await p.screenshot({ path: OUT + 'probe_scroll.png' });
  await p.evaluate(() => window.scrollTo(0, 0));

  await nav(p, '/app/verification');
  const VSPEC = Object.assign({
    k_recues: { text: 'SAISINES REÇUES', exact: true }, k_reg: { text: 'RÉGULARITÉ ÉTABLIE', exact: true }, k_bloc: { text: 'BLOQUÉES AU CONTRÔLE', exact: true },
    c0163: { text: 'SIG-2026-0163', within: 'main *', closest: 'button' }, c0186: { text: 'SIG-2026-0186', within: 'main *', closest: 'button' },
    verrou: { text: 'Le premier verrou de la plateforme.', within: 'main *' }
  }, NAV);
  await shot(p, 'm_verif', VSPEC);
  for (const sig of ['0163', '0186']) {
    await p.locator('main button', { hasText: 'SIG-2026-' + sig }).first().click(); await p.waitForTimeout(1200);
    const DS = { panel: { css: '[role="dialog"]' }, title: { text: 'SIG-2026-' + sig, within: '[role="dialog"] *' }, chip: { text: sig === '0163' ? 'Validée' : 'Clarification demandée', exact: true, within: '[role="dialog"] *' },
      ctrl_h: { text: 'Les quatre contrôles de régularité', within: '[role="dialog"] *' }, foot: { text: 'Contrôle clos', within: '[role="dialog"] *' } };
    await shot(p, 'm_sig' + sig + '_a', DS);
    // scroll the drawer body to show the four controls
    const sc = await p.evaluate(() => {
      const d = document.querySelector('[role="dialog"]'); if (!d) return null;
      const cands = [d, ...d.querySelectorAll('*')].filter(e => e.scrollHeight > e.clientHeight + 20 && /(auto|scroll)/.test(getComputedStyle(e).overflowY));
      const s = cands[0]; if (!s) return 'none';
      const top0 = s.scrollTop; s.scrollTop = s.scrollHeight; return { cls: s.className, max: s.scrollTop, h: s.clientHeight, sh: s.scrollHeight, top0 };
    });
    console.log('drawer scroll', sig, JSON.stringify(sc));
    const DS2 = Object.assign({}, DS, {
      q1: { text: "Compétence de l'autorité saisissante", within: '[role="dialog"] *', closest: 'li, div' },
      q2: { text: 'Références procédurales', within: '[role="dialog"] *', closest: 'li, div' },
      q3: { text: 'Droits des tiers', within: '[role="dialog"] *', closest: 'li, div' },
      q4: { text: 'Recherches initiales sur les faits', within: '[role="dialog"] *', closest: 'li, div' },
      obs: { text: 'Observation du vérificateur', within: '[role="dialog"] *' }
    });
    await shot(p, 'm_sig' + sig + '_b', DS2);
    boxes['m_sig' + sig + '_scroll'] = sc;
    await p.keyboard.press('Escape'); await p.waitForTimeout(600);
  }

  await nav(p, '/app/preuves');
  const PSPEC = Object.assign({
    badge: { text: 'aucun scellé rompu', exact: true, within: 'main *' }, counts: { text: 'pièces au registre', within: 'main *' },
    r0356: { css: 'main tr', nth: 1 }, r0355: { css: 'main tr', nth: 2 }, r0357: { css: 'main tr', nth: 3 },
    st0356: { text: 'Transmise au parquet', exact: true, within: 'main *' }, garantit: { text: 'Ce que garantit le registre.', within: 'main *' }
  }, NAV);
  await shot(p, 'm_preuves', PSPEC);
  await p.locator('main tr', { hasText: 'PRV-2026-0356' }).first().click(); await p.waitForTimeout(1200);
  await shot(p, 'm_prv0356', {
    panel: { css: '[role="dialog"]' }, chips: { text: 'Transmise au parquet', exact: true, within: '[role="dialog"] *' },
    scelle: { text: 'SC-00356', exact: true, within: '[role="dialog"] *' }, chaine: { text: 'Chaîne de garde', exact: true, within: '[role="dialog"] *' },
    t1: { text: '18/09/2026 20:40', within: '[role="dialog"] *' }, t2: { text: '19/09/2026 09:00', within: '[role="dialog"] *' },
    i1: { text: 'scellé intact', exact: true, within: '[role="dialog"] *', nth: 0 }, i2: { text: 'scellé intact', exact: true, within: '[role="dialog"] *', nth: 1 }
  });
  await p.keyboard.press('Escape'); await p.waitForTimeout(600);

  await nav(p, '/app/analyse');
  await shot(p, 'm_analyse0', Object.assign({ launch: { text: "Lancer l'analyse", exact: true, within: 'main button', nth: 0 }, idle: { text: 'Aucune analyse en cours', within: 'main *' } }, NAV));
  await p.locator('main button', { hasText: "Lancer l'analyse" }).first().click();
  for (let i = 0; i < 5; i++) {
    await p.waitForTimeout(i === 0 ? 150 : 420);
    await shot(p, 'm_analyse_run' + i, i === 0 ? { list: { text: 'Analyse en cours', within: 'main *', closest: 'section, div' } } : null);
  }
  await p.waitForTimeout(2500);
  await p.evaluate(() => window.scrollTo(0, 0)); await p.waitForTimeout(400);
  await shot(p, 'm_analyse', Object.assign({
    k_pieces: { text: 'PIÈCES LUES', exact: true, within: 'main *' }, k_ops: { text: 'OPÉRATIONS EXAMINÉES', exact: true, within: 'main *' },
    rap: { text: 'RAPPROCHEMENT ENTRE DEUX DOSSIERS', exact: true, within: 'main *' }, rap_title: { text: 'partagent un même compte intermédiaire', within: 'main *' },
    rn1: { text: 'Réhabilitation de la RN1', within: 'main *' }, p84: { text: '84 %', exact: true, within: 'main *' }, p84box: { text: 'DE PROXIMITÉ MESURÉE', within: 'main *' },
    bcf: { text: 'Le compte BCF 00214', within: 'main li, main p, main *' }, nedemontre: { text: 'Ce que ce rapprochement ne démontre pas.', within: 'main *' },
    graph_h: { text: 'Vérification sur le graphe des flux', exact: true, within: 'main *' }, graph: { css: 'main svg', nth: 0 },
    n_bcf: { text: 'Compte BCF 00214-…-77', exact: true, within: 'main svg *' }, n_kmp: { text: 'Katanga Mineral Processing', exact: true, within: 'main svg *' },
    n_ash: { text: 'Atlantic Shore Holdings Ltd', exact: true, within: 'main svg *' }, n_imm: { text: 'Immeuble R+4 — Lubumbashi', exact: true, within: 'main svg *' },
    ops_h: { text: "Opérations retenues par l'analyse", exact: true, within: 'main *' },
    infra: { text: 'Infrastructure requise', exact: true, within: 'main *' }, infra_txt: { text: 'En exploitation, le traitement reposerait', within: 'main *' },
    nonctr: { text: 'Proposition non contraignante', within: 'main *' }
  }, NAV), true);
  await shot(p, 'm_analyse_v', null);
  await nav(p, '/app/avoirs');
  await shot(p, 'm_avoirs', Object.assign({
    ri8: { text: 'RÉSULTAT IMMÉDIAT 8 DU GAFI — RECOUVREMENT', within: 'main *' }, ri8_q: { text: "Une enquête qui ne récupère rien n'a rien réparé.", within: 'main *' },
    acquis: { text: "ACQUIS DÉFINITIVEMENT À L'ÉTAT", within: 'main *' }, taux: { text: 'TAUX DE COUVERTURE DU PRÉJUDICE', within: 'main *' },
    k_prej: { text: 'PRÉJUDICE ÉTABLI', exact: true, within: 'main *' }, k_conf: { text: 'CONFISQUÉS', exact: true, within: 'main *' },
    bar: { text: 'RÉPARTITION DE LA VALEUR PAR STATUT', within: 'main *' }, table: { css: 'main table' },
    a071: { css: 'main tbody tr', nth: 0 }, a075: { css: 'main tbody tr', nth: 5 }
  }, NAV), true);
  await shot(p, 'm_avoirs_v', null);
  await p.context().close();

  // ---------- Coordonnateur UNICEP ----------
  p = await login('Coordonnateur UNICEP');
  await shot(p, 'c_home', Object.assign({ persona: { text: 'Ilunga Mwadi Josephine', nth: 0 } }, NAV));
  await p.locator('a[href="/app/coordination"]').first().click(); await p.waitForTimeout(1300);
  await shot(p, 'c_coord', Object.assign({
    k_ech: { text: 'ÉCHANGES ENREGISTRÉS', exact: true, within: 'main *' }, k_hd: { text: 'HORS DÉLAI', exact: true, within: 'main *' }, k_taux: { text: 'TAUX DE RÉPONSE', exact: true, within: 'main *' },
    hexa: { css: 'main svg', nth: 0 }, qui: { text: 'QUI FAIT QUOI SUR CE DOSSIER', within: 'main *' },
    table: { css: 'main table' }, r_no41: { css: 'main tbody tr', nth: 0 }, r_cog: { css: 'main tbody tr', nth: 5 }, retard: { text: 'En retard', exact: true, within: 'main td *, main td' },
    registres: { text: "Les trois registres de l'État interrogés", within: 'main *' }
  }, NAV), true);
  await shot(p, 'c_coord_v', null);
  await p.context().close();

  // ---------- Point focal CENAREF ----------
  p = await login('Point focal CENAREF');
  await shot(p, 'f_home', Object.assign({
    persona: { text: 'Nsimba Lelo Georgine', nth: 0 }, niveau: { text: 'Accès cloisonné — niveau 3', nth: 0 },
    vue: { text: 'Vue cloisonnée — institution membre.', within: 'main *' }, visible: { text: 'Ce qui est visible depuis ce poste', within: 'main *' },
    h1: { text: 'hors habilitation', exact: true, within: 'main *', nth: 0 }, h2: { text: 'hors habilitation', exact: true, within: 'main *', nth: 1 },
    k_dem: { text: 'DEMANDES REÇUES', exact: true, within: 'main *' }
  }, NAV));
  await p.locator('a[href="/app/coordination"]').first().click(); await p.waitForTimeout(1300);
  await shot(p, 'f_coord', NAV);
  await p.context().close();

  fs.writeFileSync(OUT + 'boxes.json', JSON.stringify(boxes, null, 1));
  await browser.close();
})();
