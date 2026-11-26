# -*- coding: utf-8 -*-
import io, os
D = r"C:/Users/User/Desktop/MJ Dynamics/business_model/TNT/WEBSITE"

HEAD = '''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{title} — Texas Nuclear Technologies</title>
  <meta name="description" content="{desc}" />
  <link rel="icon" type="image/jpeg" href="assets/img/logo-mark.jpg" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Chakra+Petch:wght@400;500;600;700&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500;700&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="assets/css/base.css" />
  <link rel="stylesheet" href="assets/css/layout.css" />
  <link rel="stylesheet" href="assets/css/components.css" />
  <link rel="stylesheet" href="assets/css/enterprise.css" />
</head>
<body>
  <header class="nav" id="top">
    <div class="nav-inner">
      <a class="nav-brand" href="index.html" aria-label="Texas Nuclear Technologies — home">
        <span class="nav-word"><strong>TNT</strong><em>ANALYTICAL&nbsp;LAB</em></span>
      </a>
      <nav class="nav-links" aria-label="Primary">
        <a href="index.html">HOME</a>
        <a href="icp-ms.html">ICP-MS</a>
        <a href="lcms.html">LC-MS/MS</a>
        <a href="orbitrap.html">ORBITRAP</a>
        <a href="gcms.html">GC-MS</a>
        <a href="services.html">SERVICES</a>
        <a href="checkout.html">PAY</a>
      </nav>
      <div class="nav-right">
        <a class="btn btn-gold btn-sm" href="index.html#quote">GET A QUOTE</a>
        <button class="nav-toggle" aria-label="Menu" aria-expanded="false" aria-controls="mobileMenu"><span></span><span></span></button>
      </div>
    </div>
  </header>
  <div class="mobile-menu" id="mobileMenu" hidden>
    <a href="index.html">HOME</a><a href="icp-ms.html">ICP-MS</a><a href="lcms.html">LC-MS/MS</a>
    <a href="orbitrap.html">ORBITRAP</a><a href="gcms.html">GC-MS</a><a href="services.html">SERVICES</a>
    <a href="checkout.html">PAY</a><a href="index.html#quote">QUOTE</a>
  </div>
  <main>
    <section class="inst-hero">
      <p class="inst-id reveal"><span class="led"></span>MATRIX&nbsp;·&nbsp;{mx}</p>
      <h1 class="inst-name reveal d1">{h1a}<br /><em>{h1b}</em></h1>
      <p class="inst-type reveal d2">{type}</p>
      <p class="inst-role reveal d3">{role}</p>
      <div class="kpi-strip reveal d4">{kpis}</div>
    </section>
'''

SEND = '''    <section class="section" id="send">
      <div class="sec-head reveal"><span class="sec-idx">02</span><h2>SAMPLE REQUIREMENTS</h2><span class="sec-rule"></span><span class="sec-tag">CHAIN-OF-CUSTODY&nbsp;AVAILABLE</span></div>
      <div class="proc-list">{send}</div>
    </section>
    <section class="section" id="tat">
      <div class="sec-head reveal"><span class="sec-idx">03</span><h2>TURNAROUND</h2><span class="sec-rule"></span><span class="sec-tag">CONFIRMED&nbsp;AT&nbsp;INTAKE</span></div>
      <div class="proc-list">{tat}</div>
    </section>
'''

FOOT = '''    <section class="inst-cta">
      <h2 class="reveal">STANDARD 24–48 HR · RUSH ON REQUEST</h2>
      <p class="reveal d1">QUOTED&nbsp;PER&nbsp;METHOD&nbsp;·&nbsp;CONFIRMED&nbsp;AT&nbsp;INTAKE</p>
      <a class="btn btn-gold reveal d2" href="index.html#quote">GET A QUOTE</a>
    </section>
  </main>
  <footer class="footer"><div class="footer-inner">
    <div class="footer-brand"><p>2101 GATEWAY DR<br /><span>IRVING, TX 75038</span></p></div>
    <div class="footer-meta">
      <a class="footer-mail" href="mailto:texas.nuclear.technologies@gmail.com">TEXAS.NUCLEAR.TECHNOLOGIES@GMAIL.COM</a>
      <a class="footer-mail" href="tel:+19728226494">(972) 822-6494</a>
      <p class="footer-copy">© 2025 TEXAS NUCLEAR TECHNOLOGIES</p>
    </div>
  </div></footer>
  <script defer src="assets/js/main.js"></script>
  <script defer src="assets/js/contact.js"></script>
  <div class="skyline" aria-hidden="true"></div>
</body>
</html>
'''

def kpi(b, s): return f'<div class="kpi-stat"><b>{b}</b><span>{s}</span></div>'
def step(n, h, p): return f'<div class="proc-step reveal"><span class="proc-num">{n}</span><div><h3>{h}</h3><p>{p}</p></div></div>'
def scope_section(idx, items):
    rows = "".join(step(*it) for it in items)
    return f'''    <section class="section" id="scope">
      <div class="sec-head reveal"><span class="sec-idx">01</span><h2>TEST SCOPE</h2><span class="sec-rule"></span><span class="sec-tag">METHOD-REFERENCED</span></div>
      <div class="proc-list">{rows}</div>
    </section>
'''

PAGES = {
 "matrix-supplements.html": dict(
   title="Supplements & Nutraceuticals Testing",
   desc="Supplement and nutraceutical testing — USP <232>/<233> elemental impurities, actives assay, residual solvents, microbial limits and label-claim chemistry.",
   mx="MX-01", h1a="SUPPLEMENTS &amp;", h1b="NUTRACEUTICALS",
   type="CAPSULES · TABLETS · POWDERS · OILS · GUMMIES",
   role="Release-lot and label-claim chemistry for dietary supplements — elemental, solvent, active and microbial scope under one intake.",
   kpis=kpi("24–48<i>HR</i>","CHEM&nbsp;TAT")+kpi("3–5<i>D</i>","MICRO&nbsp;TAT")+kpi("USP","&lt;232&gt;/&lt;467&gt;/&lt;61&gt;")+kpi("≥50<i>G</i>","SAMPLE"),
   scope=scope_section(1,[
     ("METALS","ELEMENTAL IMPURITIES","USP &lt;232&gt;/&lt;233&gt; Cd, Pb, As, Hg plus expanded panels — ICP-MS after closed-vessel microwave digestion. Sub-ppb reporting limits."),
     ("ACTIVES","ASSAY &amp; ID","Vitamin, mineral and active quantitation by LC-MS/MS; botanical and adulterant screening by Orbitrap non-target HRAM."),
     ("SOLVENTS","RESIDUAL SOLVENTS","USP &lt;467&gt; Class 1–3 headspace GC-MS — ethanol extraction carryover, processing aids."),
     ("MICRO","MICROBIAL LIMITS","USP &lt;61&gt;/&lt;62&gt; aerobic count, yeast &amp; mold, specified organisms; USP &lt;51&gt; preservative effectiveness where applicable."),
     ("LABEL","CLAIM CHEMISTRY","Protein, fat, fiber, moisture — AOAC-referenced methods supporting Supplement Facts panels.")]),
   send=[step("QTY","AMOUNT","≥ 50 g composite or 3+ retail units per test group. Oils and gummies noted at intake — they change digestion setup."),
          step("PACK","CONTAINER","Sealed original or clean unbreakable container. Separate aliquot for micro if both scopes ordered."),
          step("SHIP","HANDLING","Ambient is fine for most chem; ship micro samples cool, same-day preferred.")],
   tat=[step("CHEM","24–48 HR","Metals, solvents and most assays report within the standard window; rush queue available."),
        step("MICRO","3–5 DAYS","Growth-based — cannot be compressed; plate counts start day of receipt."),
        step("PET","28 DAYS","Preservative-effectiveness testing follows the standard challenge schedule.")]),
 "matrix-food.html": dict(
   title="Food & Ingredient Testing",
   desc="Food and ingredient testing — heavy metals, pesticide residues, nutrition proximates, allergen/gluten screens, water activity and microbiology.",
   mx="MX-02", h1a="FOOD &amp;", h1b="INGREDIENTS",
   type="RAW INGREDIENTS · FINISHED GOODS · PROCESS AIDES",
   role="Contaminant screening and label-support chemistry for food matrices — one sample covers metals, residues, nutrition and micro.",
   kpis=kpi("24–48<i>HR</i>","CHEM&nbsp;TAT")+kpi("3–5<i>D</i>","MICRO&nbsp;TAT")+kpi("AOAC","PROXIMATES")+kpi("≥100<i>G</i>","SAMPLE"),
   scope=scope_section(1,[
     ("METALS","HEAVY METALS","FDA-aligned elemental panels — Pb, Cd, As, Hg and full screens by ICP-MS."),
     ("RESIDUES","PESTICIDES &amp; PFAS","Multi-residue MRM panels on LC-MS/MS and GC-MS; isotope-dilution quantitation where available."),
     ("NUTRITION","PROXIMATES","Protein (combustion), fat, dietary fiber, moisture, ash, sugars and organic acids — Nutrition Facts support."),
     ("ALLERGEN","GLUTEN &amp; ALLERGENS","ELISA screens for gluten and major allergens; results reported against kit thresholds."),
     ("MICRO","FOOD MICRO","BAM-aligned aerobic count, yeast &amp; mold, pathogen screens; water activity for shelf-stability modeling.")]),
   send=[step("QTY","AMOUNT","≥ 100 g homogenized, representative of the lot. Finished goods: 2–3 retail units."),
          step("PACK","CONTAINER","Sealed food-grade bag or container; PFAS samples: no PTFE-lined contact."),
          step("SHIP","HANDLING","Perishables ship cold with gel packs; note hold-time-sensitive analytes at intake.")],
   tat=[step("CHEM","24–48 HR","Metals, residues, sweeteners and acids."),
        step("MICRO","3–5 DAYS","Plate-based counts and screens."),
        step("PANEL","3–5 DAYS","Full nutrition proximate panels run as a grouped workup.")]),
 "matrix-beverage.html": dict(
   title="Beverage Testing",
   desc="Beverage testing — organic acids, sweeteners, caffeine, preservatives, trace metals, pesticide residues and microbial screening.",
   mx="MX-03", h1a="BEVERAGES &amp;", h1b="BREWING INPUTS",
   type="RTD DRINKS · CONCENTRATES · WATER · FERMENT INPUTS",
   role="Lot QA chemistry for beverages — additives, contaminants and micro, with source-water profiling for producers.",
   kpis=kpi("24–48<i>HR</i>","CHEM&nbsp;TAT")+kpi("3–5<i>D</i>","MICRO&nbsp;TAT")+kpi("LC","ACIDS · SWEETENERS")+kpi("≥250<i>ML</i>","SAMPLE"),
   scope=scope_section(1,[
     ("PROFILE","ACIDS &amp; SWEETENERS","Organic acids, caffeine, sweeteners and preservatives by LC — formulation verification."),
     ("METALS","TRACE METALS","Source and product metals by ICP-MS — packaging-contact screening included."),
     ("RESIDUES","PESTICIDES","Input-ingredient residue carryover — MRM panels at ng/L reporting levels."),
     ("MICRO","BEVERAGE MICRO","Aerobic count, yeast &amp; mold, spoilage screens — shelf-stability relevant organisms.")]),
   send=[step("QTY","AMOUNT","≥ 250 mL sealed, original container preferred."),
          step("PACK","CONTAINER","Unopened retail unit or sterile sample bottle; headspace minimized."),
          step("SHIP","HANDLING","Cool shipment recommended; carbonated products noted at intake.")],
   tat=[step("CHEM","24–48 HR","Profiles, metals, preservatives."),
        step("MICRO","3–5 DAYS","Plate counts and spoilage screens."),
        step("RUSH","&lt;24 HR","Available for release-blocking decisions — quoted at intake.")]),
 "matrix-cosmetics.html": dict(
   title="Cosmetics & Personal Care Testing",
   desc="Cosmetic and personal-care testing — actives assay, fragrance allergens, heavy metals, microbial limits and preservative effectiveness, MoCRA-aligned.",
   mx="MX-04", h1a="COSMETICS &amp;", h1b="PERSONAL CARE",
   type="SKIN · HAIR · WIPES · TATTOO-AFTERCARE · OTC-ADJACENT",
   role="MoCRA-era purity and safety chemistry — metals, allergens, microbes and preservative performance on one submission.",
   kpis=kpi("24–48<i>HR</i>","CHEM&nbsp;TAT")+kpi("5<i>D</i>","MICRO&nbsp;TAT")+kpi("28<i>D</i>","PET&nbsp;CHALLENGE")+kpi("≥25<i>G</i>","SAMPLE"),
   scope=scope_section(1,[
     ("METALS","HEAVY METALS","FDA cosmetic-guidance panels — Pb, As, Cd, Hg plus colorant-adjacent metals by ICP-MS."),
     ("ACTIVES","ASSAY &amp; PURITY","Active concentrations, adulterant screens, fragrance-allergen profiling by GC-MS and LC-MS/MS."),
     ("E&amp;L","PACKAGING CONTACT","Extractables &amp; leachables from components — Orbitrap non-target identification."),
     ("MICRO","LIMITS + PET","USP &lt;61&gt;/&lt;62&gt; microbial limits and &lt;51&gt; preservative-effectiveness challenge."),
     ("NOTE","CLINICAL CLAIMS","SPF, broad-spectrum and safety-in-use testing is routed via qualified partners — disclosed on the report.")]),
   send=[step("QTY","AMOUNT","≥ 25 g / 25 mL per chem scope; separate micro aliquot."),
          step("PACK","CONTAINER","Original component preferred for E&amp;L relevance; avoid decanting into PTFE."),
          step("SHIP","HANDLING","Ambient acceptable; emulsions ship protected from freezing.")],
   tat=[step("CHEM","24–48 HR","Metals, allergens, assays."),
        step("MICRO","5 DAYS","Limits testing."),
        step("PET","28 DAYS","Challenge schedule per USP &lt;51&gt;.")]),
 "matrix-water.html": dict(
   title="Water & Wastewater Testing",
   desc="Water and wastewater testing — EPA 200.8/6020 trace metals, volatile organics, PFAS panels, minerals and nutrients.",
   mx="MX-05", h1a="WATER &amp;", h1b="WASTEWATER",
   type="DRINKING · PROCESS · PRODUCED · DISCHARGE",
   role="Trace metals and organics to ppb–ppt — compliance-style panels for drinking, process and produced water.",
   kpis=kpi("24–48<i>HR</i>","METALS&nbsp;TAT")+kpi("PPB–<i>PPT</i>","REPORTING")+kpi("EPA","200.8 / 6020")+kpi("≥250<i>ML</i>","PER&nbsp;FRACTION"),
   scope=scope_section(1,[
     ("METALS","TRACE METALS","EPA 200.8 / 6020(B) panels — full priority-metal scope plus minerals and hardness components."),
     ("VOCs","VOLATILE ORGANICS","BTEX / TPH and solvent screening by headspace GC-MS."),
     ("LC","PFAS &amp; ORGANICS","PFAS and nonvolatile contaminant panels to ng/L by LC-MS/MS."),
     ("FIELD","PRODUCED WATER","High-TDS matrices get dilution-validated methods — flagged at intake, not forced through drinking-water prep.")]),
   send=[step("QTY","AMOUNT","≥ 250 mL per analytical fraction (metals / VOC / organics run as separate bottles)."),
          step("PACK","CONTAINER","Metals: acid-cleaned HDPE. VOCs: 40 mL VOA vials, zero headspace. PFAS: HDPE only, no PTFE."),
          step("SHIP","HANDLING","Cool to ≤ 6 °C; hold times apply — ship same-day.")],
   tat=[step("METALS","24–48 HR","Standard compliance-style panels."),
        step("VOC/LC","24–72 HR","Volatile and LC organic fractions."),
        step("RUSH","&lt;24 HR","Discharge and incident-response decisions prioritized.")]),
 "matrix-oil-gas.html": dict(
   title="Oil & Gas Testing",
   desc="Oil and gas testing — non-target impurity profiling of crude and condensate, Ni/V metals, BTEX/TPH, produced water panels.",
   mx="MX-06", h1a="OIL &amp;", h1b="GAS",
   type="CRUDE · CONDENSATE · PROCESS STREAMS · PRODUCED WATER",
   role="Non-target impurity profiling — what is actually in the stream, not just the spec sheet asks for.",
   kpis=kpi("24–48<i>HR</i>","CHEM&nbsp;TAT")+kpi("280<i>K</i>","FWHM&nbsp;RES")+kpi("NTA","FULL&nbsp;PROFILE")+kpi("≥50<i>ML</i>","SAMPLE"),
   scope=scope_section(1,[
     ("NTA","IMPURITY PROFILE","Orbitrap HRAM non-target screening — sulfur/nitrogen species, naphthenic acids, degradation products mapped, not just checked."),
     ("METALS","Ni · V · As","ICP-MS trace metals in crude, condensate and process fluids after matrix-appropriate prep."),
     ("VOCs","BTEX / TPH","Volatile fractions and contamination screening by GC-MS."),
     ("WATER","PRODUCED WATER","Associated-water metals and organics — see the water matrix page for discharge-style panels.")]),
   send=[step("QTY","AMOUNT","≥ 50 mL representative; field-blank and trip-blank welcome for NTA work."),
          step("PACK","CONTAINER","Sealed glass or steel — no plastics for profiling work. Hazardous-material shipping applies; coordinate before sending."),
          step("NOTE","FIELD LIMITS","Pressure-sensitive or time-critical field measurements (H2S, flash) are not lab-scope — noted at intake.")],
   tat=[step("CHEM","24–48 HR","Metals and volatile fractions."),
        step("NTA","3–5 DAYS","Full non-target workups with formula proposals."),
        step("RPT","+1 DAY","Annotated impurity map with confidence levels.")]),
 "matrix-soil.html": dict(
   title="Soil & Environmental Testing",
   desc="Soil and environmental testing — RCRA-8 and full metal panels, PAH/TPH, pesticide residues and agricultural runoff nutrients.",
   mx="MX-07", h1a="SOIL &amp;", h1b="ENVIRONMENTAL",
   type="RCRA-8 · AG RUNOFF · SITE SCREENING · FILL DIRT",
   role="Digested metals and organic contaminant screening for soil, fill and runoff — defensible numbers for site decisions.",
   kpis=kpi("24–48<i>HR</i>","METALS&nbsp;TAT")+kpi("EPA","3051 / 6020")+kpi("RCRA-8","STANDARD&nbsp;PANEL")+kpi("≥100<i>G</i>","SAMPLE"),
   scope=scope_section(1,[
     ("METALS","RCRA-8 &amp; FULL PANELS","As, Ba, Cd, Cr, Pb, Hg, Se, Ag plus extended screens — microwave digestion (EPA 3051) then ICP-MS (6020)."),
     ("ORGANICS","PAH / TPH / SOLVENTS","Petroleum fractions and solvent contamination by GC-MS."),
     ("RESIDUES","PESTICIDES","Legacy and current-use residue panels by LC-MS/MS and GC-MS."),
     ("AG","RUNOFF NUTRIENTS","Nitrate/phosphate-adjacent nutrient screening for agricultural parcels.")]),
   send=[step("QTY","AMOUNT","≥ 100 g; composite of 5+ grabs for representative lots."),
          step("PACK","CONTAINER","Glass jar preferred for organics scope; clean bags acceptable for metals-only."),
          step("SHIP","HANDLING","Cool shipment for organic scope; metals-only ships ambient.")],
   tat=[step("METALS","24–48 HR","Digested panels."),
        step("ORGANICS","48–72 HR","PAH/TPH/residue fractions."),
        step("COMP","3–5 DAYS","Combined metals + organics packages.")]),
 "matrix-pharma.html": dict(
   title="Pharma & OTC Testing",
   desc="Pharmaceutical and OTC testing — USP <232>/<233> elemental impurities, <467> residual solvents, assay/impurity LC-MS/MS, nonsterile microbial limits.",
   mx="MX-08", h1a="PHARMA &amp;", h1b="OTC LOTS",
   type="RELEASE LOTS · API · EXCIPIENTS · FINISHED DOSE",
   role="cGMP-supporting chemistry for nonsterile scope — elemental, solvent, assay and microbial-limits testing with documented methods.",
   kpis=kpi("24–48<i>HR</i>","CHEM&nbsp;TAT")+kpi("5<i>D</i>","MICRO&nbsp;TAT")+kpi("USP","&lt;232&gt;/&lt;467&gt;/&lt;61&gt;")+kpi("COC","DOCUMENTED"),
   scope=scope_section(1,[
     ("IMPURITY","ELEMENTAL","USP &lt;232&gt;/&lt;233&gt; Cd, Pb, As, Hg, Co, V, Ni and full ICH Q3D option-1 panels by ICP-MS."),
     ("SOLVENT","RESIDUAL","USP &lt;467&gt; Class 1–3 by headspace GC-MS — Procedure A screening with confirmation."),
     ("ASSAY","API &amp; DEGRADANTS","Potency, related-substance and degradant panels by LC-MS/MS; Orbitrap support for unknown-peak identification."),
     ("MICRO","NONSTERILE LIMITS","USP &lt;61&gt;/&lt;62&gt; microbial enumeration and specified organisms."),
     ("ROUTE","STERILE SCOPE","Sterility, bacterial endotoxin and container-closure integrity route through qualified partners — disclosed on the report.")]),
   send=[step("QTY","AMOUNT","Per method — typically ≥ 5 g API or 10 dosage units per test; stability pulls scheduled at kickoff."),
          step("DOC","PAPERWORK","Chain-of-custody and COA requirements stated at intake; lot numbers tracked through reporting."),
          step("SHIP","HANDLING","Per product label; controlled substances require advance coordination.")],
   tat=[step("CHEM","24–48 HR","Elemental and solvent panels."),
        step("MICRO","5 DAYS","Growth-based limits testing."),
        step("DEV","QUOTED","Method-transfer or new-method work scoped and quoted separately — no silent substitutions.")]),
}

for fn, cfg in PAGES.items():
    send_rows = "".join(cfg["send"]); tat_rows = "".join(cfg["tat"])
    html = (HEAD.format(**cfg)
            + cfg["scope"]
            + SEND.format(send=send_rows, tat=tat_rows)
            + FOOT)
    io.open(os.path.join(D, fn), "w", encoding="utf-8").write(html)
    print("wrote", fn)

# repoint index cards to the new matrix pages
s = io.open(os.path.join(D, "index.html"), encoding="utf-8").read()
mapping = {"dept-01":"matrix-supplements.html","dept-02":"matrix-food.html","dept-03":"matrix-beverage.html",
           "dept-04":"matrix-cosmetics.html","dept-05":"matrix-water.html","dept-06":"matrix-oil-gas.html",
           "dept-07":"matrix-soil.html","dept-08":"matrix-pharma.html"}
for old, new in mapping.items():
    s = s.replace(f"services.html#{old}", new)
io.open(os.path.join(D, "index.html"), "w", encoding="utf-8").write(s)
print("cards repointed:", s.count("matrix-"))
