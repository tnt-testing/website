import io, os, re
D = r"C:/Users/User/Desktop/MJ Dynamics/business_model/TNT/WEBSITE"

def patch(fn, pairs, required=True):
    p = os.path.join(D, fn)
    s = io.open(p, encoding="utf-8").read()
    for old, new in pairs:
        if old in s:
            s = s.replace(old, new)
        elif required:
            print(f"  !! MISS in {fn}: {old[:70]}")
    io.open(p, "w", encoding="utf-8").write(s)
    print(f"patched {fn}")

CSS_LINK = '  <link rel="stylesheet" href="assets/css/enterprise.css" />\n'
JS_LINK  = '  <script defer src="assets/js/contact.js"></script>\n'

def inject(fn, css_after, js_after):
    p = os.path.join(D, fn)
    s = io.open(p, encoding="utf-8").read()
    if "enterprise.css" not in s:
        s = s.replace(css_after, css_after + CSS_LINK)
    if "contact.js" not in s:
        s = s.replace(js_after, js_after + "\n" + JS_LINK)
    io.open(p, "w", encoding="utf-8").write(s)

# ---------------- index.html ----------------
matrix_cards = '''      <div class="matrix-grid">
        <div class="matrix-card reveal"><span class="mx-num">MX-01</span><h3>SUPPLEMENTS &amp; NUTRACEUTICALS</h3><p>Heavy metals, active assays, residual solvents in capsules, powders and oils.</p><span class="mx-kpi">USP &lt;232&gt;/&lt;233&gt; · &lt;467&gt;</span></div>
        <div class="matrix-card reveal d1"><span class="mx-num">MX-02</span><h3>FOOD &amp; INGREDIENTS</h3><p>Elemental contaminants, pesticide residues and label-claim support chemistry.</p><span class="mx-kpi">AOAC / EPA METHODS</span></div>
        <div class="matrix-card reveal d2"><span class="mx-num">MX-03</span><h3>BEVERAGES</h3><p>Organic acids, sweeteners, additives and contaminant screening for QA lots.</p><span class="mx-kpi">LOT-RELEASE CHECKS</span></div>
        <div class="matrix-card reveal d3"><span class="mx-num">MX-04</span><span class="mx-num"></span><h3>COSMETICS &amp; PERSONAL CARE</h3><p>Actives, fragrance components, purity and adulterant screening.</p><span class="mx-kpi">MoCRA-ALIGNED</span></div>
        <div class="matrix-card reveal"><span class="mx-num">MX-05</span><h3>WATER &amp; WASTEWATER</h3><p>Drinking, process and produced water — trace metals and organics panels.</p><span class="mx-kpi">EPA 200.8 / 6020</span></div>
        <div class="matrix-card reveal d1"><span class="mx-num">MX-06</span><h3>OIL &amp; GAS</h3><p>Crude, condensate and process streams — non-target impurity profiling.</p><span class="mx-kpi">HRAM NTA SCREEN</span></div>
        <div class="matrix-card reveal d2"><span class="mx-num">MX-07</span><h3>SOIL &amp; ENVIRONMENTAL</h3><p>RCRA-8 metals, agricultural runoff and toxic-element screening.</p><span class="mx-kpi">DIGESTED · ppb–ppt</span></div>
        <div class="matrix-card reveal d3"><span class="mx-num">MX-08</span><h3>PHARMA &amp; OTC</h3><p>Elemental impurities and residual solvents for cGMP release lots.</p><span class="mx-kpi">USP-COMPLIANT LOTS</span></div>
      </div>'''

patch("index.html", [
    ("<title>Texas Nuclear Technologies — Petrochemical & Analytical Testing Laboratory</title>",
     "<title>Texas Nuclear Technologies — Analytical Testing Laboratory</title>"),
    ('<meta name="description" content="TNT — 24/7 analytical testing laboratory. HRAM Orbitrap non-target impurity profiling for crude, condensate & process streams. Results in 24–48 hours." />',
     '<meta name="description" content="TNT — analytical testing laboratory. HRAM non-target screening, ICP-MS metals, LC-MS/MS and GC-MS panels across supplement, food, cosmetic, water and industrial matrices." />'),
    ('<h1 class="hero-title reveal d1">ANY MOLECULAR STRUCTURE.<br /><em>ANALYZED</em> OVERNIGHT.</h1>',
     '<h1 class="hero-title reveal d1">KNOW WHAT&rsquo;S IN IT.<br /><em>PROVE</em> IT.</h1>'),
    ('<p class="hero-sub reveal d2">Non-target HRAM screening of any matrix — crude to capsule. Reported in 24–48 hours.</p>',
     '<p class="hero-sub reveal d2">HRAM non-target screening, metals, solvents and regulated panels — supplement to soil, crude to capsule. Standard 24–48 hr turnaround; rush available.</p>'),
    ('<h2>FACILITY</h2>\n        <span class="sec-rule"></span>\n        <span class="sec-tag">PURPOSE-BUILT&nbsp;·&nbsp;TEXAS</span>',
     '<h2>MATRICES WE HANDLE</h2>\n        <span class="sec-rule"></span>\n        <span class="sec-tag">SAMPLE&nbsp;TYPES&nbsp;·&nbsp;REAL-WORLD</span>'),
    ('<h2 class="reveal">RESULTS IN 24 HOURS OR LESS</h2>\n      <p class="reveal d1">RUSH&nbsp;QUEUE&nbsp;·&nbsp;ANY&nbsp;MATRIX</p>',
     '<h2 class="reveal">STANDARD 24–48 HR · RUSH ON REQUEST</h2>\n      <p class="reveal d1">QUOTED&nbsp;PER&nbsp;METHOD&nbsp;·&nbsp;CONFIRMED&nbsp;AT&nbsp;INTAKE</p>'),
])
# swap the four equipment <figure>s for the matrix grid
p = os.path.join(D, "index.html")
s = io.open(p, encoding="utf-8").read()
s = re.sub(r'<div class="fac-grid">.*?</div>\s*</section>', matrix_cards + "\n    </section>", s, count=1, flags=re.S)
io.open(p, "w", encoding="utf-8").write(s)
print("  fac-grid swapped" if "matrix-grid" in s else "  !! fac-grid swap FAILED")

# ---------------- orbitrap.html ----------------
patch("orbitrap.html", [
    ('<meta name="description" content="Thermo Q Exactive Plus Orbitrap — non-target HRAM screening at 280,000 FWHM. Exact-mass identification of unknown impurities. 24–48 hr turnaround." />',
     '<meta name="description" content="Thermo Q Exactive Plus Orbitrap — non-target HRAM screening at 280,000 FWHM. Exact-mass formula proposals for unknown impurities across consumer and industrial matrices." />'),
    ('<p class="inst-role reveal d3">Non-target discovery — exact-mass identification of any unknown, in any matrix.</p>',
     '<p class="inst-role reveal d3">Non-target discovery — exact-mass formula proposals and fragment-confirmed identification of unknowns in your matrix.</p>'),
    ('<h2 class="reveal">RESULTS IN 24 HOURS OR LESS</h2>',
     '<h2 class="reveal">STANDARD 24–48 HR · RUSH ON REQUEST</h2>'),
])

# ---------------- other instrument pages ----------------
for fn in ("icp-ms.html", "lcms.html", "gcms.html"):
    patch(fn, [
        ('<h2 class="reveal">RESULTS IN 24 HOURS OR LESS</h2>',
         '<h2 class="reveal">STANDARD 24–48 HR · RUSH ON REQUEST</h2>'),
    ])

# ---------------- inject css + js into every page ----------------
for fn in ("index.html", "icp-ms.html", "lcms.html", "gcms.html", "orbitrap.html", "checkout.html"):
    p = os.path.join(D, fn)
    if not os.path.exists(p):
        print(f"skip {fn}"); continue
    s = io.open(p, encoding="utf-8").read()
    if "enterprise.css" not in s:
        s = s.replace('<link rel="stylesheet" href="assets/css/components.css" />',
                      '<link rel="stylesheet" href="assets/css/components.css" />\n' + CSS_LINK, 1)
    if "contact.js" not in s:
        s = s.replace('<script defer src="assets/js/main.js"></script>',
                      '<script defer src="assets/js/main.js"></script>\n' + JS_LINK, 1)
    io.open(p, "w", encoding="utf-8").write(s)
    print(f"injected {fn}")

print("done")
