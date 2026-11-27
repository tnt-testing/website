import glob, re

MEGA = '''<div class="dd-menu dd-mega">
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
          </div>'''

SECT = ('<a href="analytical.html">ANALYTICAL</a>'
        '<a href="extraction.html">EXTRACTION</a>'
        '<a href="innovation.html">INNOVATION</a>')

done_dd, done_mm = [], []
for f in glob.glob('*.html'):
    if f in ('analytical.html', 'innovation.html'):
        continue
    s = open(f, encoding='utf-8').read()
    n = re.sub(r'<div class="dd-menu">.*?</div>', lambda m: MEGA, s, count=1, flags=re.S)
    if n != s:
        s = n
        done_dd.append(f)
    m = re.search(r'(<div class="mobile-menu" id="mobileMenu" hidden>)(.*?)(</div>)', s, re.S)
    if m and 'analytical.html' not in m.group(2):
        blk = m.group(2)
        blk = blk.replace('<a href="extraction.html">EXTRACTION &amp; R&amp;D</a>', '')
        blk = blk.replace('<a href="index.html">HOME</a>', '<a href="index.html">HOME</a>' + SECT, 1)
        s = s.replace(m.group(2), blk, 1)
        done_mm.append(f)
    open(f, 'w', encoding='utf-8').write(s)

print('dd updated:', len(done_dd), done_dd)
print('mm updated:', len(done_mm), done_mm)
