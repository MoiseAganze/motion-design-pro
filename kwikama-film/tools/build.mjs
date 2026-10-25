// Authoring convenience: inlines shared CSS, helpers and the MacBook markup into each act.
// src/acts/<id>.html  ->  compositions/<id>.html
import fs from "node:fs";
import path from "node:path";
const root = path.resolve(path.dirname(new URL(import.meta.url).pathname), "..");
const base = fs.readFileSync(path.join(root, "src/base.css"), "utf8");
const helpers = fs.readFileSync(path.join(root, "src/helpers.js"), "utf8");
const mac = fs.readFileSync(path.join(root, "src/mac.html"), "utf8");
const drc = JSON.parse(fs.readFileSync(path.join(root, "assets/brand/drc.json"), "utf8"));
const logoSvg = fs.readFileSync(path.join(root, "assets/brand/kwikama-logo.svg"), "utf8");
const only = process.argv.slice(2);
for (const f of fs.readdirSync(path.join(root, "src/acts"))) {
  if (!f.endsWith(".html")) continue;
  if (only.length && !only.includes(f.replace(/\.html$/, ""))) continue;
  let s = fs.readFileSync(path.join(root, "src/acts", f), "utf8");
  s = s.replace("/*@BASE*/", base).replace("/*@HELPERS*/", helpers).replaceAll("{{DRC}}", drc.path);
  // the official logo, vectorised: <!--@LOGO:id--> inlines its three layers (sil, navy, gold) with prefixed ids
  s = s.replace(/<!--@LOGO:([\w-]+)-->/g, (_, id) => logoSvg.replace("<svg ", `<svg id="${id}" `).replace(/id="(sil|navy|gold)"/g, (m, l) => `id="${id}-${l}"`));
  s = s.replace(/<!--@MAC:([\w-]+)-->([\s\S]*?)<!--@\/MAC-->/g, (_, p, inner) => mac.replaceAll("{P}", p).replace("{SCREEN}", inner));
  fs.writeFileSync(path.join(root, "compositions", f), s);
  console.log("built", f);
}
