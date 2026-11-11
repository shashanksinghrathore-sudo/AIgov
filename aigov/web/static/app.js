/* AI Compliance Platform - browser UI. Plain JavaScript, no external libraries, talks only to this server. */
"use strict";

const $ = (s, r = document) => r.querySelector(s);
const $$ = (s, r = document) => Array.from(r.querySelectorAll(s));
const ESC = { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" };
const esc = (s) => String(s ?? "").replace(/[&<>"']/g, (c) => ESC[c]);
const pct = (x) => Math.round((x || 0) * 100);
const app = () => $("#app");
let META = null;
let TOKEN = "";
try { TOKEN = localStorage.getItem("aigov_token") || ""; } catch (e) { /* storage unavailable */ }

const STATUS = { met: "Met", partial: "Partial", gap: "Gap", not_applicable: "N/A" };
const BASIS = { verified: "Yes - evidenced", attested: "Yes - no evidence", partial: "Partial", failed: "No",
  not_applicable: "N/A", evidence: "Unanswered - scored from evidence", no_evidence: "Unanswered" };
const ANSWERS = [["yes", "Yes"], ["partial", "Partial"], ["no", "No"], ["na", "N/A"]];

/* ------------------------------------------------------------------ plumbing */
async function api(path, opts = {}) {
  const headers = Object.assign({}, opts.headers || {});
  if (opts.body !== undefined && typeof opts.body !== "string") { headers["Content-Type"] = "application/json"; opts.body = JSON.stringify(opts.body); }
  if (TOKEN) headers.Authorization = "Bearer " + TOKEN;
  const res = await fetch(path, Object.assign({}, opts, { headers }));
  if (res.status === 401) { askToken(); throw new Error("Authentication required"); }
  if (!res.ok) {
    let msg = res.status + " " + res.statusText;
    try { const j = await res.json(); msg = typeof j.detail === "string" ? j.detail : JSON.stringify(j.detail); } catch (e) { /* not json */ }
    throw new Error(msg);
  }
  const ct = res.headers.get("content-type") || "";
  return ct.includes("application/json") ? res.json() : res.text();
}

function toast(msg, ms = 2600) {
  const t = $("#toast"); t.textContent = msg; t.classList.add("show");
  clearTimeout(toast._t); toast._t = setTimeout(() => t.classList.remove("show"), ms);
}

function fail(e) { console.error(e); toast("Error: " + e.message, 5000); }

function modal(html, onReady) {
  const bg = document.createElement("div");
  bg.className = "modal-bg";
  bg.innerHTML = `<div class="modal" role="dialog" aria-modal="true">${html}</div>`;
  document.body.appendChild(bg);
  const close = () => bg.remove();
  bg.addEventListener("click", (e) => { if (e.target === bg || e.target.closest("[data-close]")) close(); });
  document.addEventListener("keydown", function k(e) { if (e.key === "Escape") { close(); document.removeEventListener("keydown", k); } });
  if (onReady) onReady(bg, close);
  const f = bg.querySelector("input,select,textarea,button.primary"); if (f) f.focus();
  return close;
}

function askToken() {
  if ($(".modal-bg")) return;
  modal(`<h2 style="margin-top:0">Access token required</h2>
    <p class="mute small">This server is protected. Enter the API token configured by your administrator (AIGOV_API_TOKEN).</p>
    <form id="tokform"><label class="f">Token<input type="password" name="t" autocomplete="off" required></label>
    <div class="row"><button class="primary">Continue</button></div></form>`, (bg, close) => {
    $("#tokform", bg).addEventListener("submit", (e) => {
      e.preventDefault(); TOKEN = e.target.t.value.trim();
      try { localStorage.setItem("aigov_token", TOKEN); } catch (err) { /* ignore */ }
      close(); route();
    });
  });
}

async function download(path, filename) {
  const headers = TOKEN ? { Authorization: "Bearer " + TOKEN } : {};
  const res = await fetch(path, { headers });
  if (!res.ok) throw new Error("download failed: " + res.status);
  const url = URL.createObjectURL(await res.blob());
  const a = document.createElement("a"); a.href = url; a.download = filename; document.body.appendChild(a); a.click(); a.remove();
  setTimeout(() => URL.revokeObjectURL(url), 2000);
}

const pill = (cls, text) => `<span class="pill ${esc(cls)}">${esc(text)}</span>`;
const bar = (score) => `<div class="bar"><i style="width:${Math.max(0, Math.min(100, score || 0))}%"></i></div>`;
const fwName = (k) => (META.frameworks.find((f) => f.key === k) || { name: k }).name;
const fwShort = (k) => ({ eu_ai_act: "EU AI Act", gdpr: "GDPR", colorado_ai_act: "Colorado AI Act", nyc_ll144: "NYC LL 144",
  india_dpdp: "India DPDP", nist_ai_rmf: "NIST AI RMF", iso_42001: "ISO/IEC 42001", oecd_ai: "OECD", custom: "Custom" }[k] || k);

/* ------------------------------------------------------------------ router */
async function route() {
  const parts = (location.hash.replace(/^#\/?/, "") || "").split("/").filter(Boolean);
  $$(".top nav a").forEach((a) => a.classList.toggle("active", a.dataset.nav === (parts[0] === "library" ? "library" : "home")));
  try {
    if (!META) META = await api("/api/meta");
    if (!parts.length) return await viewHome();
    if (parts[0] === "library") return await viewLibrary();
    if (parts[0] === "entity") return await viewEntity(parts[1], parts[2] || "profile");
    if (parts[0] === "assessment") return await viewAssessment(parts[1]);
    app().innerHTML = `<div class="empty">Page not found. <a href="#/">Go to entities</a></div>`;
  } catch (e) {
    if (e.message !== "Authentication required") { app().innerHTML = `<div class="card warn">Could not load this page: ${esc(e.message)}</div>`; }
  }
}
window.addEventListener("hashchange", route);
window.addEventListener("DOMContentLoaded", route);

/* ------------------------------------------------------------------ home */
async function viewHome() {
  const ents = await api("/api/entities");
  const cards = ents.map((e) => {
    const p = e.profile, last = e.last_assessment;
    return `<div class="card"><div class="spread"><h3 style="margin:0">${esc(p.entity.name)}</h3>
      ${last ? `<span class="big" style="font-size:28px">${Math.round(last.overall)}</span>` : pill("na", "not tested")}</div>
      <div class="small mute">${esc(p.entity.sector || "")}${p.entity.sector ? " · " : ""}${esc((p.entity.jurisdictions || []).join(", ") || "no jurisdictions")}</div>
      <div class="small mute">${p.systems.length} AI system(s) · ${e.evidence} evidence item(s) · ${e.answers} answer(s)</div>
      ${last ? `<div class="tiny mute">Last tested ${esc(last.created.replace("T", " ").slice(0, 16))} UTC</div>${bar(last.overall)}` : ""}
      <div class="row" style="margin-top:12px"><a class="btn primary" href="#/entity/${esc(e.id)}/profile">Open</a>
      <a class="btn" href="#/entity/${esc(e.id)}/tests">Tests</a><a class="btn" href="#/entity/${esc(e.id)}/results">Results</a>
      <button class="danger" data-del="${esc(e.id)}" data-name="${esc(p.entity.name)}">Delete</button></div></div>`;
  }).join("");
  const lib = META.frameworks.filter((f) => f.articles).map((f) => `<div class="card"><div class="spread"><h3 style="margin:0">${esc(fwShort(f.key))}</h3>
      ${pill(f.binding ? "gap" : "low", f.binding ? "Binding law" : "Voluntary")}</div><div class="small mute">${esc(f.name)}</div>
      <div class="small">${f.articles} articles · ${f.assessable} with obligations · ${f.tests} tests</div></div>`).join("");
  const totals = META.frameworks.reduce((a, f) => [a[0] + f.articles, a[1] + f.tests], [0, 0]);
  app().innerHTML = `<div class="spread"><div><h1>Entities</h1>
    <p class="mute" style="margin:0">Each entity is an organisation (or business unit) tested against the laws and standards that apply to it.</p></div>
    <button class="primary" id="newEnt">+ New entity</button></div>
    <div class="grid" style="margin-top:16px">${cards || `<div class="card empty" style="grid-column:1/-1">No entities yet. Create one to start testing.</div>`}</div>
    <h2>Rule library</h2><p class="mute small" style="margin-top:-6px">${totals[0]} articles and clauses, ${totals[1]} compliance tests.
    <a href="#/library">Browse or add your own rules</a>.</p><div class="grid">${lib}</div>`;
  $("#newEnt").addEventListener("click", newEntity);
  $$("[data-del]").forEach((b) => b.addEventListener("click", async () => {
    if (!confirm(`Delete "${b.dataset.name}" with all its evidence, answers and results? This cannot be undone.`)) return;
    try { await api("/api/entities/" + b.dataset.del, { method: "DELETE" }); toast("Deleted"); viewHome(); } catch (e) { fail(e); }
  }));
}

function newEntity() {
  modal(`<h2 style="margin-top:0">New entity</h2><form id="nf">
    <label class="f">Organisation name<input name="name" required maxlength="200"></label>
    <label class="f">Sector<input name="sector" placeholder="e.g. Financial services"></label>
    <div class="row"><button class="primary">Create</button><button type="button" data-close>Cancel</button></div></form>`, (bg, close) => {
    $("#nf", bg).addEventListener("submit", async (e) => {
      e.preventDefault();
      try {
        const r = await api("/api/entities", { method: "POST", body: { entity: { name: e.target.name.value.trim(), sector: e.target.sector.value.trim() }, systems: [] } });
        close(); location.hash = `#/entity/${r.id}/profile`;
      } catch (err) { fail(err); }
    });
  });
}

/* ------------------------------------------------------------------ entity shell */
async function viewEntity(id, tab) {
  const { profile } = await api(`/api/entities/${id}`);
  const tabs = [["profile", "1. Profile & scope"], ["evidence", "2. Evidence"], ["tests", "3. Compliance tests"], ["results", "4. Results"]];
  app().innerHTML = `<div class="small"><a href="#/">Entities</a> /</div><h1>${esc(profile.entity.name)}</h1>
    <nav class="tabs">${tabs.map(([k, l]) => `<a href="#/entity/${esc(id)}/${k}" class="${k === tab ? "active" : ""}">${l}</a>`).join("")}</nav><div id="tab"></div>`;
  const view = { profile: tabProfile, evidence: tabEvidence, tests: tabTests, results: tabResults }[tab] || tabProfile;
  await view(id, profile);
}

/* ------------------------------------------------------------------ profile */
const SYS_BOOLS = [["uses_personal_data", "Uses personal data"], ["generative", "Generates content (generative AI)"],
  ["consumer_facing", "Interacts directly with people"], ["automated_decisions", "Makes solely automated decisions"],
  ["gpai_model_provider", "Is a general-purpose AI model we provide"]];

function systemBlock(s, i) {
  const v = (k) => esc(s[k] || "");
  const sel = (k, opts) => `<select data-k="${k}">${opts.map(([val, lab]) => `<option value="${val}" ${String(s[k] ?? "") === val ? "selected" : ""}>${lab}</option>`).join("")}</select>`;
  return `<div class="sys" data-sys="${i}"><div class="spread"><b>AI system ${i + 1}</b>
    ${s.assessed_risk_tier ? `<span>${pill({ prohibited: "critical", high: "high", limited: "medium", minimal: "low" }[s.assessed_risk_tier], "screened: " + s.assessed_risk_tier)}</span>` : ""}
    <button type="button" class="danger" data-rmsys="${i}">Remove</button></div>
    <div class="sysgrid" style="margin-top:8px">
      <label class="f">Name<input data-k="name" value="${v("name")}" required></label>
      <label class="f">Your role${sel("role", [["deployer", "Deployer (we use it)"], ["provider", "Provider (we build / sell it)"], ["both", "Both"]])}</label>
      <label class="f">Declared risk tier${sel("risk_tier", [["", "Not classified"], ["minimal", "Minimal"], ["limited", "Limited"], ["high", "High"], ["prohibited", "Prohibited"]])}</label>
      <label class="f">Domain<input data-k="domain" value="${v("domain")}" placeholder="credit, employment, health..."></label>
      <label class="f">Owner<input data-k="owner" value="${v("owner")}"></label>
      <label class="f">Vendor<input data-k="vendor" value="${v("vendor")}"></label>
      <label class="f">Model<input data-k="model" value="${v("model")}"></label>
      <label class="f">Purpose<input data-k="purpose" value="${v("purpose")}"></label>
    </div>
    <label class="f">Description (used to screen the risk tier)<textarea data-k="description" style="min-height:60px">${v("description")}</textarea></label>
    <div class="cols">${SYS_BOOLS.map(([k, l]) => `<label class="check"><input type="checkbox" data-k="${k}" ${s[k] ? "checked" : ""}>${l}</label>`).join("")}</div>
    ${s.risk_rationale ? `<div class="tiny mute">${esc(s.risk_rationale)}</div>` : ""}</div>`;
}

async function tabProfile(id, profile) {
  const scope = await api(`/api/entities/${id}/scope`);
  const sysById = Object.fromEntries(scope.systems.map((s) => [s.id, s]));
  let systems = profile.systems.map((s) => Object.assign({}, s, sysById[s.id] || {}));
  const ent = profile.entity;
  const juris = Object.entries(META.jurisdictions).map(([k, l]) => `<label class="check"><input type="checkbox" name="j" value="${k}" ${ent.jurisdictions.includes(k) ? "checked" : ""}>${esc(l)}</label>`).join("");
  const attrs = META.entity_flags.map((k) => `<label class="check"><input type="checkbox" name="a" value="${k}" ${ent.attributes.includes(k) ? "checked" : ""}>${esc(META.flags[k])}</label>`).join("");
  $("#tab").innerHTML = `<div class="grid2"><form id="pf"><div class="card"><h3>Organisation</h3>
      <label class="f">Name<input name="name" value="${esc(ent.name)}" required></label>
      <div class="sysgrid"><label class="f">Sector<input name="sector" value="${esc(ent.sector)}"></label>
      <label class="f">Size<input name="size" value="${esc(ent.size)}" placeholder="e.g. 800 employees"></label></div>
      <h3 style="margin-top:8px">Where it operates</h3><div class="cols">${juris}</div>
      <h3 style="margin-top:14px">Characteristics</h3><p class="tiny mute" style="margin:0 0 6px">These decide which articles apply.</p><div class="cols">${attrs}</div></div>
      <div class="card"><div class="spread"><h3 style="margin:0">AI systems</h3><button type="button" id="addSys">+ Add AI system</button></div>
      <p class="tiny mute">Each system is screened for prohibited and high-risk use. A stricter screening result overrides a declared tier.</p>
      <div id="systems"></div></div>
      <div class="row sticky"><button class="primary" id="saveP">Save profile</button><span class="small mute" id="saved"></span></div></form>
    <div id="scopebox"></div></div>`;
  const drawSystems = () => { $("#systems").innerHTML = systems.map(systemBlock).join("") || `<div class="mute small">No AI systems yet.</div>`; };
  const readSystems = () => $$("[data-sys]").map((b, i) => {
    const s = { id: systems[i].id || "SYS-" + String(i + 1).padStart(3, "0") };
    $$("[data-k]", b).forEach((inp) => { s[inp.dataset.k] = inp.type === "checkbox" ? inp.checked : inp.value.trim(); });
    if (!s.risk_tier) s.risk_tier = null;
    return s;
  });
  drawSystems();
  drawScope(scope);
  $("#addSys").addEventListener("click", () => {
    systems = readSystems();
    const used = new Set(systems.map((s) => s.id)); let n = systems.length + 1;
    while (used.has("SYS-" + String(n).padStart(3, "0"))) n++;
    systems.push({ id: "SYS-" + String(n).padStart(3, "0"), name: "", role: "deployer", risk_tier: null });
    drawSystems();
  });
  $("#systems").addEventListener("click", (e) => {
    const b = e.target.closest("[data-rmsys]"); if (!b) return;
    systems = readSystems(); systems.splice(+b.dataset.rmsys, 1); drawSystems();
  });
  $("#pf").addEventListener("submit", async (e) => {
    e.preventDefault();
    const f = e.target;
    systems = readSystems();
    const body = { entity: { name: f.name.value.trim(), sector: f.sector.value.trim(), size: f.size.value.trim(),
      jurisdictions: $$("input[name=j]:checked").map((x) => x.value), attributes: $$("input[name=a]:checked").map((x) => x.value) }, systems };
    try {
      const sc = await api(`/api/entities/${id}`, { method: "PUT", body });
      const by = Object.fromEntries(sc.systems.map((s) => [s.id, s]));
      systems = systems.map((s) => Object.assign({}, s, by[s.id] || {}));
      drawSystems(); drawScope(sc);
      $("#saved").textContent = "Saved. Scope updated.";
      toast("Profile saved");
    } catch (err) { fail(err); }
  });
}

function drawScope(sc) {
  const rows = sc.frameworks.map((f) => `<tr><td><b>${esc(fwShort(f.key))}</b><div class="tiny mute">${esc(f.name)}</div></td>
    <td>${f.applicable ? pill("met", "in scope") : pill("na", "out of scope")}</td>
    <td>${f.applicable ? `${f.in_scope} of ${f.articles}` : `<span class="tiny mute">${esc(f.reason)}</span>`}</td></tr>`).join("");
  const warn = sc.warnings.map((w) => `<div class="card warn small">${esc(w)}</div>`).join("");
  $("#scopebox").innerHTML = `<div class="card"><h3>What applies</h3>
    <p class="small mute" style="margin-top:0">${sc.articles_in_scope} articles and ${sc.tests_in_scope} tests are in scope.</p>
    <div class="wrap"><table><tr><th>Framework</th><th>Status</th><th>Articles</th></tr>${rows}</table></div>
    <h3 style="margin-top:14px">Applicability flags</h3><div class="small">${sc.flags.map((f) => esc(META.flags[f] || f)).join(" · ") || '<span class="mute">None yet - add jurisdictions and AI systems.</span>'}</div></div>
    ${warn}${sc.articles_in_scope ? `<a class="btn primary" href="#/entity/${location.hash.split("/")[2]}/evidence">Next: add evidence →</a>` : ""}`;
}

/* ------------------------------------------------------------------ evidence */
async function tabEvidence(id) {
  const items = await api(`/api/entities/${id}/evidence`);
  const rows = items.map((e) => {
    const sig = Object.entries(e.signals || {}).filter(([, v]) => v === true).map(([k]) => k);
    return `<tr><td><b>${esc(e.title)}</b><div class="tiny mute">${esc(e.ev_id)}</div>
      ${sig.length ? `<div class="tiny">Signals: ${esc(sig.join(", "))}</div>` : `<div class="tiny mute">${esc((e.preview || "").slice(0, 160))}</div>`}</td>
      <td>${esc(e.kind)}</td><td>${esc(e.connector)}</td><td class="tiny">${(e.size / 1024).toFixed(1)} KB</td>
      <td><button class="danger" data-delev="${esc(e.id)}">Delete</button></td></tr>`;
  }).join("");
  $("#tab").innerHTML = `<div class="grid2"><div class="card"><h3>Upload documents</h3>
      <p class="small mute" style="margin-top:0">Policies, procedures, risk registers, model cards, DPIAs, audit reports (md, txt, pdf, docx, json, yaml, csv).
      Upload a <b>.zip</b> of a code repository or policy folder to scan it: ML libraries, model cards, tests, CI, fairness,
      explainability and monitoring tooling, and hard-coded secrets. Files are processed on this server only; code is never executed.</p>
      <div class="drop" id="drop"><p style="margin:0 0 8px">Drag files here or</p>
      <label class="btn primary">Choose files<input type="file" id="files" multiple hidden accept=".md,.txt,.pdf,.docx,.json,.yaml,.yml,.csv,.rst,.html,.zip"></label></div></div>
    <form class="card" id="tf"><h3>Paste text or a record</h3>
      <label class="f">Title<input name="title" required placeholder="e.g. Board minutes - AI policy approval"></label>
      <label class="f">Content<textarea name="text" required></textarea></label><button class="primary">Add evidence</button></form></div>
    <h2>Evidence on file (${items.length})</h2>
    ${items.length ? `<div class="card wrap"><table><tr><th>Item</th><th>Kind</th><th>Source</th><th>Size</th><th></th></tr>${rows}</table></div>`
      : `<div class="card empty">No evidence yet. Tests can still be answered, but "yes" answers without evidence score as unverified.</div>`}
    <p><a class="btn primary" href="#/entity/${esc(id)}/tests">Next: answer the compliance tests →</a></p>
    <p class="tiny mute">Other systems can push evidence with <code>POST /api/entities/${esc(id)}/evidence</code> (see API docs).</p>`;
  const upload = async (files) => {
    for (const f of files) {
      if (f.size > 25 * 1024 * 1024) { toast(`${f.name} is larger than 25 MB`); continue; }
      toast(`Processing ${f.name}...`, 10000);
      try {
        const b64 = await new Promise((res, rej) => { const r = new FileReader(); r.onload = () => res(String(r.result).split(",")[1] || ""); r.onerror = rej; r.readAsDataURL(f); });
        const out = await api(`/api/entities/${id}/evidence/file`, { method: "POST", body: { filename: f.name, content_b64: b64 } });
        toast(`${f.name}: ${out.added.length} item(s) added` + (out.warnings.length ? ` (${out.warnings.length} warning(s))` : ""));
      } catch (e) { fail(e); }
    }
    tabEvidence(id);
  };
  $("#files").addEventListener("change", (e) => upload(Array.from(e.target.files)));
  const drop = $("#drop");
  ["dragenter", "dragover"].forEach((t) => drop.addEventListener(t, (e) => { e.preventDefault(); drop.classList.add("over"); }));
  ["dragleave", "drop"].forEach((t) => drop.addEventListener(t, (e) => { e.preventDefault(); drop.classList.remove("over"); }));
  drop.addEventListener("drop", (e) => upload(Array.from(e.dataTransfer.files)));
  $("#tf").addEventListener("submit", async (e) => {
    e.preventDefault();
    try { await api(`/api/entities/${id}/evidence`, { method: "POST", body: { title: e.target.title.value.trim(), text: e.target.text.value } }); toast("Evidence added"); tabEvidence(id); } catch (err) { fail(err); }
  });
  $$("[data-delev]").forEach((b) => b.addEventListener("click", async () => {
    if (!confirm("Delete this evidence item?")) return;
    try { await api(`/api/entities/${id}/evidence/${b.dataset.delev}`, { method: "DELETE" }); tabEvidence(id); } catch (e) { fail(e); }
  }));
}

/* ------------------------------------------------------------------ tests */
async function tabTests(id) {
  $("#tab").innerHTML = `<div class="empty">Loading the tests that apply…</div>`;
  const sc = await api(`/api/entities/${id}/scope?details=true`);
  if (!sc.requirements.length) {
    $("#tab").innerHTML = `<div class="card empty">Nothing is in scope yet. <a href="#/entity/${esc(id)}/profile">Complete the profile</a> with jurisdictions and AI systems.</div>`;
    return;
  }
  const reqs = sc.requirements;
  const answers = {};
  reqs.forEach((r) => Object.assign(answers, r.answers));
  const fws = [...new Set(reqs.map((r) => r.framework))];
  let filt = { fw: fws[0], show: "all", q: "" };
  const evOpts = (sel) => `<option value="">Link evidence…</option>` + sc.evidence_items.map((e) => `<option value="${esc(e.title)}" ${sel === e.title ? "selected" : ""}>${esc(e.title)}</option>`).join("");
  const total = () => reqs.reduce((n, r) => n + r.tests.length, 0);
  const done = () => Object.keys(answers).length;

  $("#tab").innerHTML = `<div class="card sticky" style="padding:10px 14px">
      <div class="row"><select id="fF" style="width:auto">${fws.map((f) => `<option value="${f}">${esc(fwShort(f))} (${reqs.filter((r) => r.framework === f).length})</option>`).join("")}</select>
      <select id="fS" style="width:auto"><option value="all">All tests</option><option value="open">Unanswered</option><option value="answered">Answered</option></select>
      <input id="fQ" placeholder="Search articles and tests" style="flex:1;min-width:180px">
      <span class="small" id="prog"></span>
      <button class="primary" id="runNow">Run compliance test</button></div></div>
    <p class="small mute">Answer each test for the entity as a whole. Link an evidence item to a "yes" so it counts as verified;
    unlinked "yes" answers are verified only when the evidence checks find support. Unanswered tests are scored from evidence alone, capped at 80.</p>
    <div id="reqs"></div>`;

  const progress = () => { $("#prog").textContent = `${done()} / ${total()} answered`; };
  const testRow = (t) => {
    const a = answers[t.id] || {};
    return `<div class="test" data-test="${esc(t.id)}"><div>${esc(t.question)}<div class="tiny mute">${esc(t.id)}</div></div>
      <div class="seg" role="group" aria-label="Answer">${ANSWERS.map(([v, l]) => `<button type="button" class="${a.answer === v ? "on" : ""}" data-ans="${v}" aria-pressed="${a.answer === v}">${l}</button>`).join("")}</div>
      <div class="extra"><input data-note placeholder="Note or justification" value="${esc(a.note || "")}" ${a.answer ? "" : "disabled"}>
      <select data-ev ${a.answer ? "" : "disabled"}>${evOpts(a.evidence_ref || "")}</select></div></div>`;
  };
  const card = (r) => {
    const ev = r.evidence;
    const evText = ev.score > 0
      ? `Evidence check <b>${pct(ev.score)}/100</b>${ev.doc ? ` - best match <b>${esc(ev.doc)}</b>` : ""}${ev.quotes.map((q) => `<blockquote>“${esc(q)}”</blockquote>`).join("")}`
      : `No supporting evidence found by the evidence checks.`;
    const cav = ev.caveats.map((c) => `<div class="tiny gap">Caveat in evidence: “${esc(c)}”</div>`).join("");
    return `<details class="req" data-req="${esc(r.id)}" ${r.tests.some((t) => !answers[t.id]) ? "open" : ""}>
      <summary><b>${esc(r.ref)} · ${esc(r.title)}</b>${pill(r.binding_effective ? "gap" : "low", r.binding_effective ? "binding" : "voluntary")}
      <span class="tiny mute" data-cnt></span></summary><div class="body">
      ${r.summary && !(r.tests.length === 1 && r.tests[0].question === r.summary) ? `<p class="small">${esc(r.summary)}</p>` : ""}${r.note ? `<p class="tiny mute">${esc(r.note)}</p>` : ""}
      <div class="evbox">${evText}${cav}</div>
      <div class="row tiny" style="margin:6px 0">Set all tests: ${ANSWERS.map(([v, l]) => `<button type="button" data-all="${v}">${l}</button>`).join("")}<button type="button" data-all="">Clear</button></div>
      ${r.tests.map(testRow).join("")}</div></details>`;
  };
  const counts = () => $$("details.req").forEach((d) => {
    const r = reqs.find((x) => x.id === d.dataset.req);
    $("[data-cnt]", d).textContent = `${r.tests.filter((t) => answers[t.id]).length}/${r.tests.length} answered`;
  });
  const draw = () => {
    const q = filt.q.toLowerCase();
    const list = reqs.filter((r) => (q ? true : r.framework === filt.fw)).filter((r) => {
      if (q && !(r.ref + " " + r.title + " " + r.summary + " " + r.tests.map((t) => t.question).join(" ")).toLowerCase().includes(q)) return false;
      if (filt.show === "open") return r.tests.some((t) => !answers[t.id]);
      if (filt.show === "answered") return r.tests.some((t) => answers[t.id]);
      return true;
    });
    let html = "", chap = null;
    list.forEach((r) => {
      if (r.chapter !== chap) { chap = r.chapter; html += `<h3 style="margin:18px 0 8px">${esc(q ? fwShort(r.framework) + " - " : "")}${esc(chap)}</h3>`; }
      html += card(r);
    });
    $("#reqs").innerHTML = html || `<div class="card empty">No tests match.</div>`;
    counts(); progress();
  };
  const save = async (list) => {
    try { await api(`/api/entities/${id}/answers`, { method: "PUT", body: list }); } catch (e) { fail(e); }
    progress(); counts();
  };
  const rowState = (row) => {
    const tid = row.dataset.test;
    return { test_id: tid, answer: (answers[tid] || {}).answer || null, note: $("[data-note]", row).value, evidence_ref: $("[data-ev]", row).value };
  };
  const setRow = (row, val) => {
    const tid = row.dataset.test;
    if (val) answers[tid] = Object.assign(answers[tid] || {}, { answer: val }); else delete answers[tid];
    $$("[data-ans]", row).forEach((b) => { const on = b.dataset.ans === val; b.classList.toggle("on", on); b.setAttribute("aria-pressed", on); });
    $("[data-note]", row).disabled = !val; $("[data-ev]", row).disabled = !val;
    return rowState(row);
  };
  $("#reqs").addEventListener("click", (e) => {
    const b = e.target.closest("[data-ans]");
    if (b) {
      const row = b.closest("[data-test]");
      const cur = (answers[row.dataset.test] || {}).answer;
      save([setRow(row, cur === b.dataset.ans ? null : b.dataset.ans)]);
      return;
    }
    const all = e.target.closest("[data-all]");
    if (all) save($$("[data-test]", all.closest(".body")).map((row) => setRow(row, all.dataset.all || null)));
  });
  $("#reqs").addEventListener("change", (e) => {
    const row = e.target.closest("[data-test]");
    if (!row || !(e.target.matches("[data-note]") || e.target.matches("[data-ev]"))) return;
    const st = rowState(row);
    if (!st.answer) return;
    Object.assign(answers[st.test_id], { note: st.note, evidence_ref: st.evidence_ref });
    save([st]);
  });
  $("#fF").addEventListener("change", (e) => { filt.fw = e.target.value; draw(); });
  $("#fS").addEventListener("change", (e) => { filt.show = e.target.value; draw(); });
  let qt; $("#fQ").addEventListener("input", (e) => { clearTimeout(qt); qt = setTimeout(() => { filt.q = e.target.value.trim(); draw(); }, 200); });
  $("#runNow").addEventListener("click", () => runTest(id));
  draw();
}

async function runTest(id) {
  toast("Running compliance test…", 10000);
  try { const a = await api(`/api/entities/${id}/assessments`, { method: "POST" }); toast(`Score ${Math.round(a.overall_score)}/100`); location.hash = `#/assessment/${a.id}`; }
  catch (e) { fail(e); }
}

/* ------------------------------------------------------------------ results */
async function tabResults(id) {
  const hist = await api(`/api/entities/${id}/assessments`);
  const rows = hist.map((h, i) => `<tr><td><a href="#/assessment/${esc(h.id)}">${esc(h.created.replace("T", " ").slice(0, 16))} UTC</a></td>
    <td><b>${Math.round(h.overall)}</b></td><td>${i < hist.length - 1 ? delta(h.overall - hist[i + 1].overall) : ""}</td></tr>`).join("");
  $("#tab").innerHTML = `<div class="spread"><p class="mute" style="margin:0">Each run tests the current profile, evidence and answers against the rule library and is kept for comparison.</p>
    <button class="primary" id="run">Run compliance test now</button></div>
    ${hist.length ? `<div class="card wrap" style="margin-top:12px"><table><tr><th>Run</th><th>Score</th><th>Change</th></tr>${rows}</table></div><div id="latest"></div>`
      : `<div class="card empty" style="margin-top:12px">No runs yet.</div>`}`;
  $("#run").addEventListener("click", () => runTest(id));
  if (hist.length) { const a = await api(`/api/assessments/${hist[0].id}`); $("#latest").innerHTML = `<h2>Latest result</h2>` + assessmentHTML(a); bindAssessment(a); }
}
const delta = (d) => (Math.abs(d) < 0.05 ? `<span class="mute">no change</span>` : `<span class="${d > 0 ? "met" : "gap"}">${d > 0 ? "+" : ""}${d.toFixed(1)}</span>`);

async function viewAssessment(aid) {
  const a = await api(`/api/assessments/${aid}`);
  const ents = await api("/api/entities");
  const ent = ents.find((e) => e.profile.entity.name === a.profile.entity.name);
  app().innerHTML = `<div class="small"><a href="#/">Entities</a> / ${ent ? `<a href="#/entity/${esc(ent.id)}/results">${esc(a.profile.entity.name)}</a> /` : ""} result</div>
    <h1>Compliance test result</h1><div class="mute small">${esc(a.profile.entity.name)} · ${esc(a.created_at.replace("T", " ").replace("+00:00", ""))} UTC · ${esc(a.profile.entity.jurisdictions.join(", "))}</div>
    <div style="margin-top:16px">${assessmentHTML(a)}</div>`;
  bindAssessment(a);
}

function articleHTML(r, open) {
  const tests = r.tests.length ? `<div class="wrap"><table><tr><th>Test</th><th>Result</th><th>Score</th><th>Note / evidence</th></tr>${r.tests.map((t) =>
    `<tr><td class="small">${esc(t.question)}</td><td class="small">${esc(BASIS[t.basis])}</td><td>${t.score == null ? "" : pct(t.score)}</td>
     <td class="tiny">${esc(t.note)}${t.evidence_ref ? " · " + esc(t.evidence_ref) : ""}</td></tr>`).join("")}</table></div>` : "";
  const recs = r.recommendations.map((x) => `<div class="rec small"><b>Do:</b> ${esc(x.action)}<br><span class="tiny mute">Owner: ${esc(x.owner || "unassigned")} · Effort: ${esc(x.effort)}${x.control_id ? " · Control " + esc(x.control_id) : ""}</span></div>`).join("");
  return `<details ${open ? "open" : ""}><summary>${pill(r.status, STATUS[r.status])}<b>${esc(fwShort(r.framework))} · ${esc(r.ref)} · ${esc(r.title)}</b>
    ${r.priority ? pill(r.priority, r.priority) : ""}${r.legally_binding && r.status !== "met" ? pill("gap", "binding law") : ""}
    ${r.status !== "not_applicable" ? `<span class="tiny mute">${pct(r.score)}/100</span>` : ""}</summary>
    <div class="body"><p class="small">${esc(r.rationale)}</p>${tests}
    ${r.gaps.length ? `<ul class="small">${r.gaps.map((g) => `<li>${esc(g)}</li>`).join("")}</ul>` : ""}${recs}
    ${r.citations.map((c) => `<blockquote>“${esc(c.quote)}”<br>— ${esc(c.source)}</blockquote>`).join("")}</div></details>`;
}

function assessmentHTML(a) {
  const n = { met: 0, partial: 0, gap: 0, not_applicable: 0 };
  a.results.forEach((r) => n[r.status]++);
  const order = { critical: 0, high: 1, medium: 2, low: 3 };
  const gaps = a.results.filter((r) => r.status === "gap" || r.status === "partial").sort((x, y) => (order[x.priority] - order[y.priority]) || (x.score - y.score));
  const crit = gaps.filter((g) => g.priority === "critical").length;
  const fw = a.frameworks.map((f) => `<tr><td><b>${esc(fwShort(f.key))}</b><div class="tiny mute">${esc(f.citation)}</div></td>
    <td>${pill(f.binding ? "gap" : "low", f.binding ? "Binding" : "Voluntary")}</td>
    ${f.applicable && f.score != null ? `<td style="min-width:120px"><b>${Math.round(f.score)}</b>${bar(f.score)}</td><td>${f.in_scope}</td><td class="met">${f.met}</td><td class="partial">${f.partial}</td><td class="gap">${f.gap}</td>`
      : `<td colspan="5" class="tiny mute">Not in scope: ${esc(f.reason)}</td>`}</tr>`).join("");
  const dom = Object.entries(a.domains).map(([d, s]) => `<div class="card"><div class="spread"><b class="small">${esc(d)}</b><span>${Math.round(s)}</span></div>${bar(s)}</div>`).join("");
  const road = a.roadmap.map((p) => `<div class="card"><h3>${esc(p.phase)} <span class="mute small">${esc(p.horizon)}</span></h3><ul style="padding-left:18px">${p.actions.map((x) =>
    `<li class="small" style="margin-bottom:8px">${pill(x.priority, x.priority)} ${esc(x.action)}<div class="tiny mute">Owner: ${esc(x.owner || "unassigned")} · closes ${x.closes.length} article(s): ${esc(x.closes.slice(0, 6).join(", "))}${x.closes.length > 6 ? "…" : ""}</div></li>`).join("")}</ul></div>`).join("");
  const sys = a.profile.systems.map((s) => `<tr><td><b>${esc(s.name)}</b></td><td>${esc(s.role)}</td><td>${pill({ prohibited: "critical", high: "high", limited: "medium", minimal: "low" }[s.assessed_risk_tier] || "low", s.assessed_risk_tier || "")}</td><td class="tiny">${esc(s.risk_rationale)}</td></tr>`).join("");
  return `<div class="row" style="margin-bottom:12px"><span class="small mute">Download:</span>
      ${["html", "csv", "json", "md"].map((f) => `<button data-dl="${f}">${{ html: "Report (HTML)", csv: "Test log (CSV)", json: "Data (JSON)", md: "Markdown" }[f]}</button>`).join("")}</div>
    <div class="hero"><div class="card"><div class="small mute">Overall score</div><div class="big">${Math.round(a.overall_score)}</div>
      <div class="small mute">out of 100 · ${esc(a.maturity)}</div>${bar(a.overall_score)}
      <p class="small">${pill("met", n.met + " met")} ${pill("partial", n.partial + " partial")} ${pill("gap", n.gap + " gap")}<br>
      <span class="mute tiny">${crit} critical · ${a.tests_answered}/${a.tests_total} tests answered</span></p></div>
      <div class="card small">${a.executive_summary.split("\n\n").map((p) => `<p style="margin:0 0 10px">${esc(p)}</p>`).join("")}</div></div>
    <h2>Laws and frameworks</h2><div class="card wrap"><table><tr><th>Framework</th><th>Type</th><th>Score</th><th>In scope</th><th>Met</th><th>Partial</th><th>Gap</th></tr>${fw}</table></div>
    ${sys ? `<h2>AI systems</h2><div class="card wrap"><table><tr><th>System</th><th>Role</th><th>Risk tier</th><th>Basis</th></tr>${sys}</table></div>` : ""}
    <h2>Domains</h2><div class="grid">${dom}</div>
    <h2>Improvement roadmap</h2><p class="small mute" style="margin-top:-6px">Each action fixes a control shared by several articles, ordered by legal exposure.</p><div class="grid2">${road || '<div class="card">Nothing to remediate.</div>'}</div>
    <h2>Gaps by article (${gaps.length})</h2>
    <div class="row" style="margin-bottom:8px"><select id="gF" style="width:auto"><option value="">All frameworks</option>${[...new Set(gaps.map((g) => g.framework))].map((f) => `<option value="${f}">${esc(fwShort(f))}</option>`).join("")}</select>
    <select id="gP" style="width:auto"><option value="">All priorities</option>${["critical", "high", "medium", "low"].map((p) => `<option>${p}</option>`).join("")}</select></div>
    <div id="gaplist"></div>
    <h2>Met (${n.met})</h2><div>${a.results.filter((r) => r.status === "met").map((r) => articleHTML(r)).join("") || '<div class="card mute">None yet.</div>'}</div>
    ${a.warnings.length ? `<h2>Notes</h2>${a.warnings.map((w) => `<div class="card warn small">${esc(w)}</div>`).join("")}` : ""}
    <p class="tiny mute">Rule-based diagnostic, not legal advice. Article summaries are paraphrased; confirm against official texts.</p>`;
}

function bindAssessment(a) {
  const order = { critical: 0, high: 1, medium: 2, low: 3 };
  const gaps = a.results.filter((r) => r.status === "gap" || r.status === "partial").sort((x, y) => (order[x.priority] - order[y.priority]) || (x.score - y.score));
  const drawGaps = () => {
    const f = $("#gF").value, p = $("#gP").value;
    const list = gaps.filter((g) => (!f || g.framework === f) && (!p || g.priority === p));
    $("#gaplist").innerHTML = list.map((r, i) => articleHTML(r, i < 2)).join("") || `<div class="card mute">No gaps for this filter.</div>`;
  };
  $("#gF").addEventListener("change", drawGaps); $("#gP").addEventListener("change", drawGaps); drawGaps();
  $$("[data-dl]").forEach((b) => b.addEventListener("click", () => {
    const slug = a.profile.entity.name.replace(/[^A-Za-z0-9]+/g, "-").toLowerCase();
    download(`/api/assessments/${a.id}/report?format=${b.dataset.dl}`, `aigov-${slug}-${a.created_at.slice(0, 10)}.${b.dataset.dl}`).catch(fail);
  }));
}

/* ------------------------------------------------------------------ rule library */
let LIB = { fw: "eu_ai_act", kind: "all", q: "" };
async function viewLibrary() {
  const fwOpts = META.frameworks.map((f) => `<option value="${f.key}" ${f.key === LIB.fw ? "selected" : ""}>${esc(fwShort(f.key))} (${f.articles})</option>`).join("");
  app().innerHTML = `<div class="spread"><div><h1>Rule library</h1><p class="mute" style="margin:0">Every article and clause the platform knows, the tests it runs, and when each applies.
    Built-in rules are read-only; add your own laws, internal policies or contractual duties as custom rules.</p></div>
    <button class="primary" id="addRule">+ Add custom rule</button></div>
    <div class="card sticky row" style="margin-top:14px;padding:10px 14px"><select id="lF" style="width:auto"><option value="">All frameworks</option>${fwOpts}</select>
    <select id="lK" style="width:auto"><option value="all">All articles</option><option value="obligation">With obligations (tested)</option><option value="info">Reference only</option></select>
    <input id="lQ" placeholder="Search text, article or test" value="${esc(LIB.q)}" style="flex:1;min-width:180px"><span class="small mute" id="lN"></span></div>
    <div id="fwinfo"></div><div id="lib"></div>`;
  $("#lK").value = LIB.kind;
  const draw = async () => {
    const qs = new URLSearchParams({ framework: LIB.fw, kind: LIB.kind, q: LIB.q });
    const list = await api("/api/library?" + qs);
    $("#lN").textContent = `${list.length} article(s)`;
    const f = META.frameworks.find((x) => x.key === LIB.fw);
    $("#fwinfo").innerHTML = f ? `<div class="card small"><b>${esc(f.name)}</b> · ${esc(f.citation)} · ${esc(f.region)} · ${f.binding ? "binding law" : "voluntary"}
      ${f.note ? `<div class="tiny mute">${esc(f.note)}</div>` : ""}</div>` : "";
    let html = "", chap = null;
    list.forEach((r) => {
      const ch = (LIB.fw ? "" : fwShort(r.framework) + " - ") + r.chapter;
      if (ch !== chap) { chap = ch; html += `<h3 style="margin:18px 0 8px">${esc(ch)}</h3>`; }
      html += ruleHTML(r);
    });
    $("#lib").innerHTML = html || `<div class="card empty">No articles match.</div>`;
  };
  $("#lF").addEventListener("change", (e) => { LIB.fw = e.target.value; draw().catch(fail); });
  $("#lK").addEventListener("change", (e) => { LIB.kind = e.target.value; draw().catch(fail); });
  let t; $("#lQ").addEventListener("input", (e) => { clearTimeout(t); t = setTimeout(() => { LIB.q = e.target.value.trim(); draw().catch(fail); }, 250); });
  $("#addRule").addEventListener("click", () => ruleForm(null, draw));
  $("#lib").addEventListener("click", async (e) => {
    const ed = e.target.closest("[data-edit]"), del = e.target.closest("[data-delrule]");
    if (ed) { const list = await api("/api/library?" + new URLSearchParams({ q: ed.dataset.edit })); ruleForm(list.find((r) => r.id === ed.dataset.edit), draw); }
    if (del && confirm("Delete this custom rule? Answers to its tests are kept but ignored.")) {
      try { await api("/api/rules/" + encodeURIComponent(del.dataset.delrule), { method: "DELETE" }); META = await api("/api/meta"); draw(); toast("Rule deleted"); } catch (err) { fail(err); }
    }
  });
  await draw();
}

function ruleHTML(r) {
  const ctl = r.controls.map((c) => { const x = META.controls.find((y) => y.id === c); return x ? `${esc(c)} ${esc(x.title)}` : esc(c); });
  const appl = [r.need_labels.length ? "All of: " + r.need_labels.join("; ") : "", r.when_labels.length ? "Any of: " + r.when_labels.join("; ") : ""].filter(Boolean).join(" · ");
  return `<details><summary>${r.kind === "info" ? pill("na", "reference") : pill(r.binding_effective ? "gap" : "low", r.binding_effective ? "binding" : "voluntary")}
    <b>${esc(r.ref)} · ${esc(r.title)}</b>${r.custom ? pill("medium", "custom") : ""}${r.kind !== "info" ? `<span class="tiny mute">${r.tests.length} test(s) · weight ${r.weight}</span>` : ""}</summary>
    <div class="body">${r.summary ? `<p class="small">${esc(r.summary)}</p>` : ""}${r.note ? `<p class="small mute">${esc(r.note)}</p>` : ""}
    ${r.kind === "info" ? `<p class="tiny mute">Reference provision (definitions, duties of authorities, amendments or penalties). Listed for completeness; not tested.</p>` : `
    <dl class="kv"><dt>Rule id</dt><dd>${esc(r.id)}</dd><dt>Applies when</dt><dd>${esc(appl || "Whenever the framework applies")}</dd>
    <dt>Evidence checks</dt><dd>${ctl.join("<br>") || "Keyword checks only"}${r.keywords.length ? "<br>Keywords: " + esc(r.keywords.join(", ")) : ""}</dd></dl>
    <ol class="small">${r.tests.map((t) => `<li>${esc(t.question)} <span class="tiny mute">${esc(t.id)}</span></li>`).join("")}</ol>`}
    ${r.custom ? `<div class="row"><button data-edit="${esc(r.id)}">Edit</button><button class="danger" data-delrule="${esc(r.id)}">Delete</button></div>` : ""}</div></details>`;
}

function ruleForm(r, after) {
  r = r || { framework: "custom", ref: "", title: "", chapter: "Custom rules", summary: "", note: "", tests: [], controls: [], keywords: [], need: [], when: [], weight: 2, binding: null, action: "", owner: "" };
  const fl = (name, sel) => Object.entries(META.flags).map(([k, l]) => `<label class="check"><input type="checkbox" name="${name}" value="${k}" ${sel.includes(k) ? "checked" : ""}>${esc(l)}</label>`).join("");
  modal(`<h2 style="margin-top:0">${r.id ? "Edit" : "Add"} custom rule</h2><form id="rf">
    <div class="sysgrid"><label class="f">Framework<select name="framework" ${r.id ? "disabled" : ""}>${META.frameworks.map((f) => `<option value="${f.key}" ${f.key === r.framework ? "selected" : ""}>${esc(f.name)}</option>`).join("")}</select></label>
    <label class="f">Reference<input name="ref" required value="${esc(r.ref)}" placeholder="e.g. Policy 4.2 or Art. 12" ${r.id ? "disabled" : ""}></label>
    <label class="f">Chapter / group<input name="chapter" value="${esc(r.chapter)}"></label></div>
    <label class="f">Title<input name="title" required value="${esc(r.title)}"></label>
    <label class="f">Requirement (what must be true)<textarea name="summary">${esc(r.summary)}</textarea></label>
    <label class="f">Tests - one question per line (leave empty to test the requirement as one question)<textarea name="tests">${esc(r.tests.map((t) => t.question || t).join("\n"))}</textarea></label>
    <label class="f">Evidence keywords - comma separated phrases to look for in uploaded documents<input name="keywords" value="${esc(r.keywords.join(", "))}"></label>
    <details><summary><b>Evidence checks and remediation from the control library</b></summary><div class="body cols">${META.controls.map((c) => `<label class="check"><input type="checkbox" name="controls" value="${c.id}" ${r.controls.includes(c.id) ? "checked" : ""}>${esc(c.id)} ${esc(c.title)}</label>`).join("")}</div></details>
    <details><summary><b>Applies only when ALL of these hold</b></summary><div class="body cols">${fl("need", r.need)}</div></details>
    <details><summary><b>Applies only when ANY of these hold</b></summary><div class="body cols">${fl("when", r.when)}</div></details>
    <div class="sysgrid" style="margin-top:10px"><label class="f">Weight<select name="weight">${[1, 2, 3].map((w) => `<option ${w === r.weight ? "selected" : ""}>${w}</option>`).join("")}</select></label>
    <label class="f">Legally binding<select name="binding"><option value="">Same as framework</option><option value="true" ${r.binding === true ? "selected" : ""}>Yes</option><option value="false" ${r.binding === false ? "selected" : ""}>No</option></select></label>
    <label class="f">Owner<input name="owner" value="${esc(r.owner)}"></label></div>
    <label class="f">Remediation if not met<input name="action" value="${esc(r.action)}"></label>
    <label class="f">Note<input name="note" value="${esc(r.note)}"></label>
    <div class="row"><button class="primary">Save rule</button><button type="button" data-close>Cancel</button></div></form>`, (bg, close) => {
    $("#rf", bg).addEventListener("submit", async (e) => {
      e.preventDefault();
      const f = e.target, vals = (n) => $$(`input[name=${n}]:checked`, f).map((x) => x.value);
      const body = { framework: f.framework.value, ref: f.ref.value.trim(), title: f.title.value.trim(), chapter: f.chapter.value.trim(),
        summary: f.summary.value.trim(), note: f.note.value.trim(), tests: f.tests.value.split("\n").map((x) => x.trim()).filter(Boolean),
        keywords: f.keywords.value.split(",").map((x) => x.trim()).filter(Boolean), controls: vals("controls"), need: vals("need"), when: vals("when"),
        weight: +f.weight.value, binding: f.binding.value === "" ? null : f.binding.value === "true", action: f.action.value.trim(), owner: f.owner.value.trim() };
      try {
        await api(r.id ? "/api/rules/" + encodeURIComponent(r.id) : "/api/rules", { method: r.id ? "PUT" : "POST", body });
        META = await api("/api/meta"); close(); toast("Rule saved"); after();
      } catch (err) { fail(err); }
    });
  });
}
