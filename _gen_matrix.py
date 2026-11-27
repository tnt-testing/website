# -*- coding: utf-8 -*-
# Regenerates the 8 matrix pages. Template is kept current with the site
# (dropdown nav, Manrope fonts, modal CTAs, footer sitemap, ?v= CSS bust).
import io, os
D = r"C:/Users/User/Desktop/MJ Dynamics/business_model/TNT/WEBSITE"

NAV = '''  <header class="nav" id="top">
    <div class="nav-inner">
      <a class="nav-brand" href="index.html" aria-label="Texas Nuclear Technologies — home">
        <span class="nav-word"><strong>TNT</strong><em>ANALYTICAL&nbsp;LAB</em></span>
      </a>
      <nav class="nav-links" aria-label="Primary">
        <a href="index.html">HOME</a>
        <div class="nav-dd"><a href="services.html" class="dd-btn">SERVICES <span class="dd-caret">▾</span></a>
          <div class="dd-menu dd-mega">
            <div class="dd-col">
              <a class="dd-sect" href="extraction.html">EXTRACTION</a>
              <p class="dd-sub">EQUIPMENT</p>
              <a href="extraction.html#train">UMAE REACTOR</a>
              <a href="extraction.html#train">SUPERCRITICAL CO2</a>
              <a href="extraction.html#train">WIPED-FILM</a>
              <a href="extraction.html#train">CHROMATOGRAPHY</a>
              <p class="dd-sub">SERVICES</p>
              <a href="extraction.html#services">TOLL EXTRACTION</a>
              <a href="extraction.html#services">BENCH STUDIES</a>
              <a href="extraction.html#engage">ENGAGEMENT</a>
            </div>
            <div class="dd-col">
              <a class="dd-sect" href="analytical.html">ANALYTICAL</a>
              <p class="dd-sub">EQUIPMENT</p>
              <a href="icp-ms.html">ICP-MS</a>
              <a href="lcms.html">LC-MS/MS</a>
              <a href="orbitrap.html">ORBITRAP</a>
              <a href="gcms.html">GC-MS</a>
              <p class="dd-sub">SERVICES</p>
              <a href="services.html">ALL SERVICES</a>
              <a href="analytical.html#departments">9 DEPARTMENTS</a>
              <a href="analytical.html#matrices">PRODUCT MATRICES</a>
            </div>
            <div class="dd-col">
              <a class="dd-sect" href="innovation.html">INNOVATION</a>
              <p class="dd-sub">EQUIPMENT</p>
              <a href="innovation.html#platform">FERMENTER</a>
              <a href="innovation.html#platform">FLOW CYTOMETER</a>
              <a href="innovation.html#platform">qPCR</a>
              <a href="innovation.html#platform">96-WELL FILLER</a>
              <p class="dd-sub">SERVICES</p>
              <a href="innovation.html#programs">NOVEL COMPOUNDS</a>
              <a href="innovation.html#programs">IP DOSSIERS</a>
              <a href="innovation.html#engage">CONTRACT R&amp;D</a>
            </div>
          </div>
        </div>
        <a href="checkout.html">PAY</a>
      </nav>
      <div class="nav-right">
        <a class="btn btn-gold" href="javascript:void(0)" onclick="window.tntContact()">GET A QUOTE</a>
        <button class="nav-toggle" aria-label="Menu" aria-expanded="false" aria-controls="mobileMenu"><span></span><span></span></button>
      </div>
    </div>
  </header>
  <div class="mobile-menu" id="mobileMenu" hidden>
    <a href="index.html">HOME</a><a href="analytical.html">ANALYTICAL</a><a href="extraction.html">EXTRACTION</a><a href="innovation.html">INNOVATION</a><a href="services.html">SERVICES</a><a href="icp-ms.html">ICP-MS</a>
    <a href="lcms.html">LC-MS/MS</a><a href="orbitrap.html">ORBITRAP</a><a href="gcms.html">GC-MS</a>
    <a href="matrix-supplements.html">SUPPLEMENTS</a><a href="matrix-food.html">FOOD</a>
    <a href="matrix-beverage.html">BEVERAGES</a><a href="matrix-cosmetics.html">COSMETICS</a>
    <a href="matrix-water.html">WATER</a><a href="matrix-oil-gas.html">OIL &amp; GAS</a>
    <a href="matrix-soil.html">SOIL</a><a href="matrix-pharma.html">PHARMA</a>
    <a href="checkout.html">PAY</a>
  </div>
'''

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
  <link href="https://fonts.googleapis.com/css2?family=Manrope:wght@500;600;700;800&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="assets/css/base.css" />
  <link rel="stylesheet" href="assets/css/layout.css" />
  <link rel="stylesheet" href="assets/css/components.css" />
  <link rel="stylesheet" href="assets/css/enterprise.css?v=6" />
</head>
<body data-sample="{sample}">
''' + NAV + '''  <main>
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
      <h2 class="reveal">STANDARD 24–72 HR · &lt;24 HR IN-HOUSE RUSH</h2>
      <p class="reveal d1">QUOTED&nbsp;PER&nbsp;METHOD&nbsp;·&nbsp;CONFIRMED&nbsp;AT&nbsp;INTAKE</p>
      <a class="btn btn-gold reveal d2" href="javascript:void(0)" onclick="window.tntContact()">REQUEST THIS TEST</a>
    </section>
  </main>
  <footer class="footer"><div class="footer-inner">
    <div class="footer-brand"><p>2101 GATEWAY DR<br /><span>IRVING, TX 75038</span></p></div>
    <div class="footer-meta">
      <a class="footer-mail" href="mailto:texas.nuclear.technologies@gmail.com">TEXAS.NUCLEAR.TECHNOLOGIES@GMAIL.COM</a>
      <a class="footer-mail" href="tel:+19728226494">(972) 822-6494</a>
      <p class="footer-nav"><a href="index.html">HOME</a> · <a href="services.html">SERVICES</a> · <a href="index.html#tests">TESTS</a> · <a href="index.html#faq">FAQ</a> · <a href="checkout.html">PAY</a></p>
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
  mx="MX-01", h1a="SUPPLEMENTS &amp;", h1b="NUTRACEUTICALS", sample="SUPPLEMENTS / NUTRACEUTICALS",
  type="CAPSULES · TABLETS · POWDERS · OILS · GUMMIES",
  role="Release-lot and label-claim chemistry for dietary supplements — elemental, solvent, active and microbial scope under one intake.",
  kpis=kpi("24–72<i>HR</i>","CHEM&nbsp;TAT")+kpi("3–5<i>D</i>","MICRO&nbsp;TAT")+kpi("USP","&lt;232&gt;/&lt;467&gt;/&lt;61&gt;")+kpi("≥50<i>G</i>","SAMPLE"),
  scope=scope_section(1,[
    ("METALS","ELEMENTAL IMPURITIES","Runs USP &lt;232&gt;/&lt;233&gt; — the compendial elemental-impurity limits for drug and supplement products. Cadmium, lead, arsenic, mercury plus expanded multi-element panels are digested in closed-vessel microwave systems and quantified by ICP-MS to sub-ppb reporting limits, with spike-recovery checks on every batch."),
    ("ACTIVES","ASSAY &amp; LABEL-CLAIM","Confirms the potency printed on the Supplement Facts panel — vitamins, minerals and botanical actives quantified against reference standards by LC-MS/MS. Adulterant and undeclared-ingredient screening runs on the Orbitrap non-target platform, so unknown peaks get identified, not ignored."),
    ("SOLVENTS","RESIDUAL SOLVENTS","USP &lt;467&gt; covers solvents left over from extraction and manufacturing, classed 1–3 by toxicity. We screen all three classes by headspace GC-MS — ethanol extraction carryover, hexane residues and processing aids quantified against compendial limits."),
    ("MICRO","MICROBIAL LIMITS","USP &lt;61&gt;/&lt;62&gt; enumeration for nonsterile products — total aerobic microbial count, yeast &amp; mold, plus specified organisms (E. coli, Salmonella, S. aureus, P. aeruginosa). USP &lt;51&gt; preservative-effectiveness challenge available where the formula calls for it."),
    ("NUTRITION","CLAIM CHEMISTRY","The proximate panel behind the Nutrition/Supplement Facts label — protein, fat, fiber, moisture and ash run by AOAC-referenced methods and reported per serving and per 100 g for label-substantiation files.")] ),
  send=[step("QTY","AMOUNT","≥ 50 g composite or 3+ retail units per test group — enough for the method blank, duplicate and spike-recovery portions every batch requires. Oils and gummies change digestion setup, so flag them at intake and we'll quote the right prep."),
         step("PACK","CONTAINER","Sealed original packaging or a clean unbreakable container. Ordering micro scope too? Send a separate sealed unit — microbial limits need an unopened aliquot to stay defensible."),
         step("SHIP","HANDLING","Ambient shipping is fine for chemistry panels. Micro samples ship cool and same-day preferred — transit time eats the 24–72 hr hold window before plating must start.")],
  tat=[step("CHEM","24–72 HR","Metals, solvents and most assay panels report within 24–72 hr of receipt. Rush queue available for release-blocking decisions — flagged at intake, quoted upfront, no surprises."),
        step("MICRO","3–5 DAYS","Plate counts are growth-based and can't be compressed — the organism dictates the schedule. Plating starts the day the sample logs in."),
        step("PET","28 DAYS","Preservative-effectiveness testing follows the USP &lt;51&gt; challenge schedule — inoculated units pulled and counted on compendial timepoints.")]),
"matrix-food.html": dict(
  title="Food & Ingredient Testing",
  desc="Food and ingredient testing — heavy metals, pesticide residues, nutrition proximates, allergen/gluten screens, water activity and microbiology.",
  mx="MX-02", h1a="FOOD &amp;", h1b="INGREDIENTS", sample="FOOD / INGREDIENTS",
  type="RAW INGREDIENTS · FINISHED GOODS · PROCESS AIDS",
  role="Contaminant screening and label-support chemistry for food matrices — one sample covers metals, residues, nutrition and micro.",
  kpis=kpi("24–72<i>HR</i>","CHEM&nbsp;TAT")+kpi("3–5<i>D</i>","MICRO&nbsp;TAT")+kpi("AOAC","PROXIMATES")+kpi("≥100<i>G</i>","SAMPLE"),
  scope=scope_section(1,[
    ("METALS","HEAVY METALS","FDA-aligned elemental panels for food — Pb, Cd, As, Hg and full multi-element screens. Samples are acid-digested and read on ICP-MS with reporting limits below the levels FDA guidance tracks for vulnerable products like infant food and juices."),
    ("RESIDUES","PESTICIDES &amp; PFAS","Multi-residue MRM panels — one tandem-MS run quantifies dozens of pesticides, each compound confirmed by two fragment transitions. PFAS panels use isotope-dilution quantitation for ng/L-level reporting on produce, protein and packaging-contact matrices."),
    ("NUTRITION","PROXIMATES","The Nutrition Facts package — protein by combustion, fat by extraction, dietary fiber, moisture, ash, sugars and organic acids by AOAC-validated consensus methods, reported for label panels and spec sheets."),
    ("ALLERGEN","GLUTEN &amp; ALLERGENS","ELISA-based detection of declared allergens — gluten, peanut, soy, milk, egg and tree nuts — at ppm sensitivity. Results report against kit thresholds for allergen-control verification and label decisions."),
    ("MICRO","FOOD MICRO &amp; Aw","BAM-aligned (FDA's Bacteriological Analytical Manual) aerobic count, yeast &amp; mold and pathogen screens. Water activity — the unbound water that predicts microbial shelf stability — measured alongside for stability modeling.")] ),
  send=[step("QTY","AMOUNT","≥ 100 g homogenized and representative of the lot — finished goods send 2–3 retail units so we can sample across the package. Homogeneity matters more than volume for residue work."),
         step("PACK","CONTAINER","Sealed food-grade bag or container. For PFAS scope: no PTFE-lined contact anywhere in the chain — it leaches the exact compounds we're measuring."),
         step("SHIP","HANDLING","Perishables ship cold with gel packs. Flag hold-time-sensitive analytes at intake — some residues and micro scopes carry 24–72 hr windows from sampling, not receipt.")],
  tat=[step("CHEM","24–72 HR","Metals, residues, sweeteners and acids report within the standard window after digestion and run."),
        step("MICRO","3–5 DAYS","Plate-based counts and pathogen screens — growth-based, plated day of receipt."),
        step("PANEL","3–5 DAYS","Full nutrition proximate panels run as a grouped workup — combustion, extraction and fiber fractions in parallel.")]),
"matrix-beverage.html": dict(
  title="Beverage Testing",
  desc="Beverage testing — organic acids, sweeteners, caffeine, preservatives, trace metals, pesticide residues and microbial screening.",
  mx="MX-03", h1a="BEVERAGES &amp;", h1b="BREWING INPUTS", sample="BEVERAGES",
  type="RTD DRINKS · CONCENTRATES · WATER · FERMENT INPUTS",
  role="Lot QA chemistry for beverages — additives, contaminants and micro, with source-water profiling for producers.",
  kpis=kpi("24–72<i>HR</i>","CHEM&nbsp;TAT")+kpi("3–5<i>D</i>","MICRO&nbsp;TAT")+kpi("LC","ACIDS · SWEETENERS")+kpi("≥250<i>ML</i>","SAMPLE"),
  scope=scope_section(1,[
    ("PROFILE","ACIDS &amp; SWEETENERS","Organic acids (citric, malic, tartaric, phosphoric), caffeine, sweeteners and preservatives profiled by LC — the formulation-verification panel that confirms a batch matches its spec sheet. Also catches authenticity issues like acid-profile drift in juice products."),
    ("PRESERV","SORBATE / BENZOATE","Preservative assay quantifies sorbate, benzoate and sulfite levels against regulatory and label limits — the numbers that decide whether a low-pH product holds its shelf life."),
    ("METALS","TRACE METALS","Source-water and finished-product metals by ICP-MS — iron, copper, arsenic and packaging-contact elements tracked for contamination, flavor defects and regulatory limits."),
    ("MICRO","SPOILAGE &amp; QA SCREENS","Aerobic count, yeast &amp; mold and acid-tolerant spoilage organisms — the shelf-stability screens that matter in low-pH products where pathogens can't grow but spoilage organisms can.")] ),
  send=[step("QTY","AMOUNT","≥ 250 mL sealed — original retail container preferred so results reflect the product as sold. Concentrates and syrup bases noted at intake; they dilute differently into method range."),
         step("PACK","CONTAINER","Unopened retail unit or sterile sample bottle with headspace minimized — headspace oxygen skews preservative and acid readings on sensitive products."),
         step("SHIP","HANDLING","Cool shipment recommended. Carbonated products flagged at intake — degassing before analysis is part of the prep, not an afterthought.")],
  tat=[step("CHEM","24–72 HR","Profiles, metals and preservative assays report within the standard window."),
        step("MICRO","3–5 DAYS","Plate counts and spoilage screens — growth-based, started day of receipt."),
        step("RUSH","&lt;24 HR","Available for release-blocking decisions — quoted at intake when the lot can't wait.")]),
"matrix-cosmetics.html": dict(
  title="Cosmetics & Personal Care Testing",
  desc="Cosmetic and personal-care testing — actives assay, fragrance allergens, heavy metals, microbial limits and preservative effectiveness, MoCRA-aligned.",
  mx="MX-04", h1a="COSMETICS &amp;", h1b="PERSONAL CARE", sample="COSMETICS / PERSONAL CARE",
  type="SKIN · HAIR · WIPES · TATTOO-AFTERCARE · OTC-ADJACENT",
  role="MoCRA-era purity and safety chemistry — metals, allergens, microbes and preservative performance on one submission.",
  kpis=kpi("24–72<i>HR</i>","CHEM&nbsp;TAT")+kpi("5<i>D</i>","MICRO&nbsp;TAT")+kpi("28<i>D</i>","PET&nbsp;CHALLENGE")+kpi("≥25<i>G</i>","SAMPLE"),
  scope=scope_section(1,[
    ("METALS","HEAVY METALS","FDA cosmetic-guidance panels — lead, arsenic, mercury and cadmium, plus colorant-adjacent metals, run by ICP-MS to the levels regulators audit in color cosmetics and imported ingredients."),
    ("ACTIVES","ASSAY &amp; ALLERGENS","Active concentrations (niacinamide, retinoids, acids) verified by LC-MS/MS and the EU-listed fragrance allergens profiled by GC-MS — the purity and sensitization data MoCRA safety-substantiation files need."),
    ("E&amp;L","EXTRACTABLES &amp; LEACHABLES","Compounds that migrate from packaging into the formula — screened by Orbitrap non-target identification so extractables get identified and reported, protecting purity claims on component changes."),
    ("MICRO","LIMITS + CHALLENGE","USP &lt;61&gt;/&lt;62&gt; microbial-limits testing for nonsterile cosmetics, plus the &lt;51&gt; preservative-effectiveness test — a 28-day inoculation study proving the formula's preservative system controls growth over its shelf life."),
    ("CLAIMS","CLINICAL &amp; SPF STUDIES","SPF, broad-spectrum and safety-in-use testing scheduled as specialty studies — quoted per protocol at intake.")] ),
  send=[step("QTY","AMOUNT","≥ 25 g / 25 mL per chemistry scope, plus a separate sealed unit for the micro aliquot — one opened container can't serve both scopes defensibly."),
         step("PACK","CONTAINER","Send the product in its original component where possible — for extractables/leachables relevance the packaging is part of the sample. Avoid decanting into PTFE containers."),
         step("SHIP","HANDLING","Ambient shipping is acceptable for most formulas; emulsions ship protected from freezing — a freeze-thaw cycle can break the emulsion before we ever plate it.")],
  tat=[step("CHEM","24–72 HR","Metals, allergens and active assays report within the standard window."),
        step("MICRO","5 DAYS","Microbial-limits testing — growth-based enumeration and specified-organism screens."),
        step("PET","28 DAYS","The preservative-effectiveness challenge runs the full USP &lt;51&gt; schedule — inoculation, then pulls at compendial timepoints.")]),
"matrix-water.html": dict(
  title="Water & Wastewater Testing",
  desc="Water and wastewater testing — EPA 200.8/6020 trace metals, volatile organics, PFAS panels, minerals and nutrients.",
  mx="MX-05", h1a="WATER &amp;", h1b="WASTEWATER", sample="WATER / ENVIRONMENTAL",
  type="DRINKING · PROCESS · PRODUCED · DISCHARGE",
  role="Trace metals and organics to ppb–ppt — compliance-style panels for drinking, process and produced water.",
  kpis=kpi("24–72<i>HR</i>","METALS&nbsp;TAT")+kpi("PPB–<i>PPT</i>","REPORTING")+kpi("EPA","200.8 / 6020")+kpi("≥250<i>ML</i>","PER&nbsp;FRACTION"),
  scope=scope_section(1,[
    ("METALS","TRACE METALS","EPA 200.8 / 6020(B) — the ICP-MS methods for metals in drinking, waste and groundwater. Full priority-metal scope plus minerals and hardness components, with reporting limits below action levels so results mean something at compliance margins."),
    ("VOCs","VOLATILE ORGANICS","BTEX and solvent-class volatiles by headspace GC-MS — the fuel and industrial-solvent signature panel for discharge, remediation and source-investigation work."),
    ("LC","PFAS &amp; ORGANICS","Per- and polyfluoroalkyl 'forever chemicals' quantified at ng/L by isotope-dilution LC-MS/MS, plus nonvolatile contaminant panels for process and discharge water."),
    ("FIELD","HIGH-TDS &amp; PRODUCED WATER","Oilfield and industrial brines don't run through drinking-water prep — high-TDS matrices get dilution-validated methods with matrix-matched calibration, flagged at intake and reported with dilution factors.")] ),
  send=[step("QTY","AMOUNT","≥ 250 mL per analytical fraction — metals, VOCs and organics run as separate bottles because each has its own preservation chemistry and hold clock."),
         step("PACK","CONTAINER","Metals: acid-cleaned HDPE preserved to pH &lt; 2. VOCs: 40 mL VOA vials filled zero-headspace. PFAS: HDPE only — no PTFE anywhere in contact."),
         step("SHIP","HANDLING","Cool to ≤ 6 °C and ship same-day — VOC hold times run 14 days from sampling under preservation, but every day in transit is a day off the analytical window. Chain-of-custody paperwork available for compliance and legal use.")],
  tat=[step("METALS","24–72 HR","Standard compliance-style panels report within the window after digestion and run."),
        step("VOC/LC","24–72 HR","Volatile and LC organic fractions — PFAS workups include isotope-dilution QA before reporting."),
        step("RUSH","&lt;24 HR","Discharge incidents and response decisions prioritized — quoted at intake.")]),
"matrix-oil-gas.html": dict(
  title="Oil & Gas Testing",
  desc="Oil and gas testing — non-target impurity profiling of crude and condensate, Ni/V metals, BTEX/TPH, produced water panels.",
  mx="MX-06", h1a="OIL &amp;", h1b="GAS", sample="OIL &amp; GAS",
  type="CRUDE · CONDENSATE · PROCESS STREAMS · PRODUCED WATER",
  role="Non-target impurity profiling — what is actually in the stream, not just what the spec sheet asks for.",
  kpis=kpi("24–72<i>HR</i>","CHEM&nbsp;TAT")+kpi("280<i>K</i>","FWHM&nbsp;RES")+kpi("NTA","FULL&nbsp;PROFILE")+kpi("≥50<i>ML</i>","SAMPLE"),
  scope=scope_section(1,[
    ("NTA","IMPURITY PROFILE","Non-target analysis — high-resolution screening that identifies every detectable compound, not just a target list. The Orbitrap acquires at 280,000 FWHM with &lt;3 ppm mass error, producing formula proposals for sulfur/nitrogen species, naphthenic acids and degradation products — reported as an annotated impurity map with confidence levels."),
    ("METALS","Ni · V · As","Nickel, vanadium and arsenic — the refinery-relevant trace metals that foul catalysts and drive blending decisions — quantified by ICP-MS in crude, condensate and process fluids after matrix-appropriate prep."),
    ("VOCs","BTEX / TPH","Benzene, toluene, ethylbenzene, xylenes and total petroleum hydrocarbons — the standard contamination metrics for stream quality and release assessment, by headspace GC-MS."),
    ("WATER","PRODUCED WATER","Formation water co-produced with hydrocarbons — high-TDS metals and organics panels under dilution-validated methods for disposal, reuse and compliance decisions.")] ),
  send=[step("QTY","AMOUNT","≥ 50 mL representative of the stream. For non-target workups a field or trip blank is strongly recommended — it separates stream signal from transport contamination, which is where these analyses live or die."),
         step("PACK","CONTAINER","Sealed glass or steel only — no plastics for profiling work, since polymer leachables would land directly in the non-target spectrum. Hazardous-material shipping applies; coordinate classification before sending."),
         step("NOTE","FIELD LIMITS","Pressure-sensitive or time-critical field measurements (H2S, flash point at the wellhead) aren't lab scope — we'll tell you at intake rather than accept a sample we can't report on.")],
  tat=[step("CHEM","24–72 HR","Metals and volatile fractions report within the standard window."),
        step("NTA","3–5 DAYS","Full non-target workups — acquisition, formula proposals and confidence-ranked identification take real analyst time."),
        step("RPT","+1 DAY","The annotated impurity map — chromatogram features tied to formula proposals — ships after review.")]),
"matrix-soil.html": dict(
  title="Soil & Environmental Testing",
  desc="Soil and environmental testing — RCRA-8 and full metal panels, PAH/TPH, pesticide residues and agricultural runoff nutrients.",
  mx="MX-07", h1a="SOIL &amp;", h1b="ENVIRONMENTAL", sample="SOIL / ENVIRONMENTAL",
  type="RCRA-8 · AG RUNOFF · SITE SCREENING · FILL DIRT",
  role="Digested metals and organic contaminant screening for soil, fill and runoff — defensible numbers for site decisions.",
  kpis=kpi("24–72<i>HR</i>","METALS&nbsp;TAT")+kpi("EPA","3051 / 6020")+kpi("RCRA-8","STANDARD&nbsp;PANEL")+kpi("≥100<i>G</i>","SAMPLE"),
  scope=scope_section(1,[
    ("METALS","RCRA-8 &amp; FULL PANELS","The eight federally regulated metals — As, Ba, Cd, Cr, Pb, Hg, Se, Ag — used for hazardous-waste characterization, plus extended screens. Samples are microwave-digested per EPA 3051 and quantified by ICP-MS per 6020, with reporting limits below action levels."),
    ("ORGANICS","PAH / TPH / SOLVENTS","Polycyclic aromatic hydrocarbons — combustion-derived contaminants common on industrial and fill sites — plus TPH split by carbon range (gasoline, diesel and oil-range organics) and solvent residues by GC-MS."),
    ("RESIDUES","PESTICIDES","Legacy and current-use residue panels by LC-MS/MS and GC-MS — organochlorines, organophosphates and modern actives for agricultural parcels and redevelopment sites."),
    ("AG","RUNOFF NUTRIENTS","Nitrate, phosphate and micronutrient-adjacent panels for soil fertility and agricultural-runoff assessment — the nutrient side of the environmental picture.")] ),
  send=[step("QTY","AMOUNT","≥ 100 g, composited from 5+ grabs for a representative lot — single-grab samples answer single-spot questions. For fill-dirt acceptance, composite across the pile."),
         step("PACK","CONTAINER","Glass jar preferred when organic scope is ordered — bags can leach plasticizers into the PAH spectrum. Clean bags are fine for metals-only panels."),
         step("SHIP","HANDLING","Cool shipment for organic scope to preserve volatiles and PAHs; metals-only panels ship ambient — metals don't degrade.")],
  tat=[step("METALS","24–72 HR","Digested metal panels report within the window."),
        step("ORGANICS","48–72 HR","PAH, TPH and residue fractions — extraction and concentration steps drive the longer window."),
        step("COMP","3–5 DAYS","Combined metals + organics packages run fractions in parallel and report together.")]),
"matrix-pharma.html": dict(
  title="Pharma & OTC Testing",
  desc="Pharmaceutical and OTC testing — USP <232>/<233> elemental impurities, <467> residual solvents, assay/impurity LC-MS/MS, nonsterile microbial limits.",
  mx="MX-08", h1a="PHARMA &amp;", h1b="OTC LOTS", sample="PHARMA / OTC LOT",
  type="RELEASE LOTS · API · EXCIPIENTS · FINISHED DOSE",
  role="cGMP-supporting chemistry — elemental, solvent, assay and microbial-limits testing with documented methods and regulated-scope scheduling.",
  kpis=kpi("24–72<i>HR</i>","CHEM&nbsp;TAT")+kpi("5<i>D</i>","MICRO&nbsp;TAT")+kpi("USP","&lt;232&gt;/&lt;467&gt;/&lt;61&gt;")+kpi("COC","DOCUMENTED"),
  scope=scope_section(1,[
    ("IMPURITY","ELEMENTAL","USP &lt;232&gt;/&lt;233&gt; — the compendial elemental-impurity limits driven by ICH Q3D, the international guideline for metals in drug products. Cd, Pb, As, Hg, Co, V, Ni and full option-1 panels run by ICP-MS after validated digestion, reported against permitted daily-exposure limits."),
    ("SOLVENT","RESIDUAL","USP &lt;467&gt; residual solvents — Class 1–3 compendial limits measured by headspace GC-MS with Procedure A screening and confirmatory runs, covering the solvent list regulators audit on API and excipient lots."),
    ("ASSAY","API &amp; DEGRADANTS","Active-ingredient potency plus related-substance and degradant panels by LC-MS/MS — the release and stability numbers a batch record needs. Unknown peaks escalate to the Orbitrap for formula-proposal identification."),
    ("MICRO","NONSTERILE LIMITS","USP &lt;61&gt;/&lt;62&gt; — microbial enumeration (total aerobic count, yeast &amp; mold) and objectionable-organism testing for oral and topical products, the nonsterile release panel."),
    ("ROUTE","STERILE SCOPE","Endotoxin (LAL), particulate matter, container-closure integrity and sterility testing for injectable release — scheduled through the Regulated &amp; Specialty department and quoted per protocol at intake.")] ),
  send=[step("QTY","AMOUNT","Per method — typically ≥ 5 g API or 10 dosage units per test, covering the blank, duplicate and spike portions the batch requires. Stability pulls are scheduled at kickoff so later timepoints don't bottleneck."),
         step("DOC","PAPERWORK","Chain-of-custody and COA requirements stated at intake — COC is the documented sample-handling record your QA team needs for audit trails. Lot numbers are tracked through the report."),
         step("SHIP","HANDLING","Per the product label — controlled substances require advance coordination for transfer documentation before anything ships.")],
  tat=[step("CHEM","24–72 HR","Elemental and solvent panels report within the standard window."),
        step("MICRO","5 DAYS","Growth-based limits testing — plated day of receipt, enumerated on schedule."),
        step("DEV","QUOTED","Method-transfer or new-method development is scoped and quoted separately — no silent substitutions, no untransferred methods presented as validated.")]),
}

for fn, cfg in PAGES.items():
    send_rows = "".join(cfg["send"]); tat_rows = "".join(cfg["tat"])
    html = (HEAD.format(**cfg)
            + cfg["scope"]
            + SEND.format(send=send_rows, tat=tat_rows)
            + FOOT)
    io.open(os.path.join(D, fn), "w", encoding="utf-8").write(html)
    print("wrote", fn)
