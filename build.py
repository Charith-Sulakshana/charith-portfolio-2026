#!/usr/bin/env python3
"""Builds index.html from the content below and the image manifest.
Edit the CONTENT section to change text, order or captions, then run:  python3 build.py
"""
import json, html, re, os
HERE = os.path.dirname(os.path.abspath(__file__))
MAN = json.load(open(os.path.join(HERE, 'assets/manifest.json')))
E = html.escape

def img(slug, alt, cls='', gallery=None, cap=None, sizes='100vw', eager=False):
    w, h = MAN[slug]
    g = f' data-gallery="{gallery}"' if gallery else ''
    c = f' data-cap="{E(cap)}"' if cap else ''
    load = 'eager' if eager else 'lazy'
    return (f'<button type="button" class="shot {cls}"{g}{c} data-src="assets/img/{slug}.webp" aria-label="Open {E(alt)}">'
            f'<img src="assets/img/{slug}.webp" alt="{E(alt)}" width="{w}" height="{h}" loading="{load}" decoding="async" style="aspect-ratio:{w}/{h}">'
            f'</button>')

def fig(slug, alt, caption, cls='', gallery=None, eager=False):
    return f'<figure class="fig {cls}">{img(slug, alt, gallery=gallery, cap=caption, eager=eager)}<figcaption>{caption}</figcaption></figure>'

def chapter_head(num, kicker, title, intro, meta, right_label):
    meta_html = ''.join(f'<div><dt>{E(k)}</dt><dd>{v}</dd></div>' for k, v in meta)
    return f'''
    <header class="ch-head reveal">
      <div class="ch-row label"><span>Chapter {num}</span><span>{right_label}</span></div>
      <p class="ch-kicker label">{kicker}</p>
      <h2 class="ch-title">{title}</h2>
      <div class="ch-body">
        <p class="ch-intro">{intro}</p>
        <dl class="ch-meta">{meta_html}</dl>
      </div>
      <i class="crop tl"></i><i class="crop tr"></i><i class="crop bl"></i><i class="crop br"></i>
    </header>'''

# ----------------------------------------------------------------------------
# CONTENT — Creative Designer
# ----------------------------------------------------------------------------
SAILS = [
    ('sail-a', 'Flite', 'Heraldic crest on a red and white spinnaker'),
    ('sail-b', 'Kraken', 'Tentacle linework across a mainsail'),
    ('sail-c', 'SoulShine & Panthers', 'Two sails, two logos, one order'),
    ('sail-d', "Bove's", 'Family badge on a pale yellow spinnaker'),
    ('sail-e', 'Flamingo', 'Illustration on a spinnaker with yellow edging'),
    ('sail-f', 'Helia · OPT-NC', 'Black mainsail with Pantone and vinyl notes'),
    ('sail-g', 'Portrait', 'Vectorised portrait inside a circle'),
    ('sail-h', 'Corsair', 'Pirate silhouette on a yellow spinnaker'),
    ('sail-i', 'Braves 150', 'Wordmark and tomahawk on a red spinnaker'),
]
GREEK = [('greek-athena', 'Athena', 'Wisdom. Strategy. War.'), ('greek-medusa', 'Medusa', 'Curse. Fear. Power.'),
         ('greek-hercules', 'Hercules', 'Strength. Endurance. Legacy.'), ('greek-poseidon', 'Poseidon', 'Depth. Chaos. Control.')]
NTG = [('ntg-1', 'Cover'), ('ntg-2', 'January – February'), ('ntg-3', 'March – April'), ('ntg-4', 'May – June'),
       ('ntg-5', 'July – August'), ('ntg-6', 'September – October'), ('ntg-7', 'November – December')]
ASTRO = ['Offer: gems at the best price', 'Offer: gems at the best price (version 2)', 'Offer: gems in Malabe',
         'Offer: 30% off', 'Gems for planetary periods', 'Lucky gem by birth chart', '30% off, poster style',
         '30% off silver and gems', '30% off jewellery for astrology work', 'Offer: now in Malabe',
         'Gems for each ascendant', 'Navaratna: the nine gems', 'Peridot for August birthdays', 'Hiring: jewellery craftsman']

def c_layers(n=14, depth=30.0):
    def mix(a, b, t):
        a = [int(a[i:i+2], 16) for i in (1, 3, 5)]; b = [int(b[i:i+2], 16) for i in (1, 3, 5)]
        return '#' + ''.join(f'{round(x + (y - x) * t):02x}' for x, y in zip(a, b))
    out = []
    for i in range(n):
        t = i / (n - 1)
        out.append(f'            <svg viewBox="0 0 161.08 134.23" class="layer" data-z="{depth * t:.2f}" style="fill:{mix("#01111A", "#005478", t)}"><use href="#c-path"/></svg>\n')
    out.append(f'            <svg viewBox="0 0 161.08 134.23" class="layer face" data-z="{depth + 0.6:.2f}"><use href="#c-path"/></svg>\n')
    return ''.join(out)

def designer():
    s = []
    LAYERS = c_layers()
    # --- Cover
    s.append(f'''
  <section class="cover" id="d-top" aria-label="Cover">
    <div class="wrap cover__grid">
      <div class="cover__copy">
        <p class="label cover__vol"><span>Vol. 01</span><span>2026</span><span>Colombo</span></p>
        <h1 class="cover__title"><span class="split">Portfolio</span></h1>
        <p class="label cover__role">Charith Sulakshana &nbsp;·&nbsp; Creative Designer</p>
        <p class="cover__lead">I design sail graphics, brand identities and print. At North Manufacturing I also run the laser and the plotter, so most of what I draw ends up as something you can hold.</p>
        <p class="cover__tag label"><i></i><span>Where<br>brands<br>begin.</span></p>
      </div>
      <div class="cover__art" aria-hidden="true">
        <ul class="label cover__index"><li>Ideas</li><li>Sketches</li><li>Brands</li><li>People</li></ul>
        <div class="draw" data-draw>
          <svg class="draw__lines" viewBox="0 0 600 600">
            <circle cx="300" cy="300" r="268"/><circle cx="300" cy="300" r="190"/>
            <rect x="139.46" y="166" width="321.08" height="268"/>
            <line x1="40" y1="300" x2="560" y2="300"/><line x1="300" y1="20" x2="300" y2="580"/>
            <line x1="110" y1="110" x2="490" y2="490"/><line x1="490" y1="110" x2="110" y2="490"/>
            <circle cx="353.46" cy="273.38" r="107.38"/>
            <path class="dim" d="M139.46 456 H460.54 M139.46 450 v12 M460.54 450 v12"/>
            <path class="dim" d="M482 166 V434 M476 166 h12 M476 434 h12"/>
            <text x="300" y="476" text-anchor="middle">161.08</text>
            <text x="496" y="304" class="v">134.23</text>
            <path class="dim" d="M429 197 L466 160 H520"/><text x="472" y="152">R 53.69</text>
          </svg>
          <div class="stack" data-stack>
{LAYERS}            <svg viewBox="0 0 161.08 134.23" class="layer outline" data-z="31"><use href="#c-path"/></svg>
          </div>
        </div>
      </div>
    </div>
    <div class="cover__bar"></div>
  </section>''')

    # --- Contents
    toc = [('01', 'Sail graphics', 'North Sails · 9 layouts', 'd-sails'),
           ('02', 'Bella Spencer', 'Brand identity · 7 pieces and a reel', 'd-bella'),
           ('03', 'Print', 'Calendar, diary, sketchbook · 9 pages', 'd-print'),
           ('04', 'Greek Gods Reimagined', 'Illustration · 5 posters', 'd-greek'),
           ('05', 'Astro Jewellers', 'Social campaign · 14 posts', 'd-astro'),
           ('06', 'Identities', 'RMN, Nethmina, Sanjula · 14 pieces', 'd-ids'),
           ('07', 'Logo boards', 'Concepts · 7 boards', 'd-logos'),
           ('08', 'About me', 'Experience, tools, contact', 'd-about')]
    rows = ''.join(f'<li><a href="#{a}"><span class="n">{n}</span><span class="t">{t}</span><span class="dots" aria-hidden="true"></span><span class="m">{m}</span></a></li>' for n, t, m, a in toc)
    s.append(f'''
  <section class="contents wrap" aria-labelledby="d-contents-t">
    <div class="contents__head reveal"><p class="label" id="d-contents-t">Contents</p><p class="contents__note">66 pieces from my working folders, grouped the way I keep them.</p></div>
    <ol class="toc reveal">{rows}</ol>
  </section>''')

    # --- 01 Sails
    figs = ''.join(fig(sl, f'{n} sail layout', f'<b>{n}</b><span>{d}</span>', gallery='sails') for sl, n, d in SAILS)
    s.append(f'''
  <section class="chapter wrap" id="d-sails">
    {chapter_head('01', 'Sail graphics', 'Drawn to the<br>sail plan', 'Each layout sits on the real sail shape, port side, with luff, leech and foot marked, and the artwork on its own beside it. From here the file goes to print and to the plotter for cutting.', [('For', 'North Sails'), ('At', 'North Manufacturing'), ('Tools', 'Illustrator, Flexi')], 'North Manufacturing')}
    <div class="g-sails">{figs}</div>
  </section>''')

    # --- 02 Bella
    s.append(f'''
  <section class="chapter wrap" id="d-bella">
    {chapter_head('02', 'Brand identity', 'Bella Spencer', 'A quiet identity for a travel-goods brand. The monogram tucks an S inside the B, and the wordmark is a light serif that stays readable small. Then three colourways, posts for The Travel Edit, and an eight-second reel.', [('Pieces', 'Monogram, wordmark, colourways, social, reel'), ('Tools', 'Illustrator, Photoshop')], 'Identity')}
    <div class="g-bella">
      <div class="bella-marks">
        {fig('bella-monogram', 'Bella Spencer monogram', '<b>Monogram</b><span>B with the S tucked inside</span>', 'paper', gallery='bella')}
        {fig('bella-wordmark', 'Bella Spencer wordmark', '<b>Wordmark</b><span>Light serif, two lines</span>', 'paper', gallery='bella')}
      </div>
      <div class="bella-boards">
        {fig('bella-board-1', 'Bella Spencer colourway in cream and blush', '<b>Colourway 1</b><span>Cream, charcoal, blush</span>', gallery='bella')}
        {fig('bella-board-2', 'Bella Spencer colourway in charcoal and sage', '<b>Colourway 2</b><span>Charcoal, ivory, sage</span>', gallery='bella')}
        {fig('bella-board-3', 'Bella Spencer colourway in stone and black', '<b>Colourway 3</b><span>Stone, blush, black</span>', gallery='bella')}
      </div>
      <div class="bella-social">
        {fig('bella-post', 'Bella Spencer social post, Everything in its place', '<b>The Travel Edit</b><span>Instagram post</span>', gallery='bella')}
        <figure class="fig reel"><div class="reel__frame"><video src="assets/media/bella-reel.mp4" poster="assets/media/bella-reel-poster.jpg" muted loop playsinline preload="none" data-reel aria-label="Bella Spencer brand reel"></video><button type="button" class="reel__btn label" data-reel-btn>Play</button></div><figcaption><b>Brand reel</b><span>8 seconds, vertical</span></figcaption></figure>
        {fig('bella-fb', 'Bella Spencer Facebook landscape post', '<b>Facebook post</b><span>Landscape version</span>', 'wide', gallery='bella')}
      </div>
    </div>
  </section>''')

    # --- 03 Print
    pages = ''.join(f'<li>{img(sl, f"NTG 2026 calendar, {n}", gallery="ntg", cap=f"<b>NTG 2026 calendar</b><span>{n}</span>")}<span class="label">{n}</span></li>' for sl, n in NTG)
    s.append(f'''
  <section class="chapter wrap" id="d-print">
    {chapter_head('03', 'Print', 'Calendar, diary,<br>sketchbook', 'The 2026 corporate calendar for North Sails and Future Fibres, built around racing photography with the brand colours running down each page. Also the cover of the North Sails Industrial Training Diary, and the cover of my own sketchbook.', [('For', 'North Sails, Future Fibres'), ('Format', 'Wall calendar, A4 diary'), ('Tools', 'Illustrator, Photoshop')], 'Print-ready')}
    <ol class="ntg" data-fan>{pages}</ol>
    <div class="g-print">
      {fig('diary', 'North Sails Industrial Training Diary cover', '<b>Industrial Training Diary</b><span>Front and back cover, North Sails</span>', 'diary', gallery='print')}
      {fig('sketchbook', 'Charith Sulakshana sketchbook cover', '<b>My sketchbook, Vol. 01</b><span>Logo design, brand identity, typography</span>', 'sketch', gallery='print')}
    </div>
  </section>''')

    # --- 04 Greek
    gods = ''.join(fig(sl, f'{n}, Greek Gods Reimagined', f'<b>{n}</b><span>{d}</span>', gallery='greek') for sl, n, d in GREEK)
    s.append(f'''
  <section class="chapter wrap" id="d-greek">
    {chapter_head('04', 'Illustration', 'Greek Gods<br>Reimagined', 'A personal series. Four gods with their faces masked, each one set inside a Greek key ring with three words underneath.', [('Type', 'Personal series, 2026'), ('Pieces', '4 posters and a title card')], 'Personal work')}
    <div class="g-greek">
      {fig('greek-title', 'Greek Gods Reimagined title poster', '<b>Title card</b><span>Greek Gods Reimagined</span>', 'title', gallery='greek')}
      {gods}
    </div>
  </section>''')

    # --- 05 Astro
    posts = ''.join(f'<li>{img(f"astro-{i+1:02d}", f"Astro Jewellers post: {c}", gallery="astro", cap=f"<b>Astro Jewellers</b><span>{c}</span>")}</li>' for i, c in enumerate(ASTRO))
    s.append(f'''
  <section class="chapter wrap" id="d-astro">
    {chapter_head('05', 'Social campaign', 'Astro Jewellers', 'Fourteen Sinhala posts for a gem and jewellery shop in Malabe. Offers, gem guides by birth chart and planetary period, the nine gems of the Navaratna, and a hiring post.', [('For', 'Astro Jewellers (Pvt) Ltd, Malabe'), ('Language', 'Sinhala'), ('Format', 'Square social posts')], 'Digital marketing')}
    <ol class="g-astro">{posts}</ol>
  </section>''')

    # --- 06 Identities
    sanju = ''.join(f'<li>{img(f"sanju-{i}", "Sanjula Gaming avatar or badge", gallery="ids", cap="<b>Sanjula Gaming</b><span>Avatar and badge set</span>")}</li>' for i in range(1, 8))
    s.append(f'''
  <section class="chapter wrap" id="d-ids">
    {chapter_head('06', 'Identities', 'Three brands,<br>three moods', 'An industrial machine supplier, a motorbike repair shop and a gaming streamer. Different jobs. Each one started with the logo, then the pieces the business uses day to day.', [('Clients', 'RMN Lanka Automation, Nethmina Motors, Sanjula Gaming')], 'Branding')}
    <div class="ids">
      <article class="id-block">
        <h3 class="id-name"><span class="label">A</span>RMN Lanka Automation</h3>
        <p class="id-note">Logo for a Piliyandala supplier of spring-making machines, in colour, red and blue, and black. Plus a Sinhala ad for their machines.</p>
        <div class="g-rmn">
          {fig('rmn-logo-colour', 'RMN Lanka Automation logo, colour', '<b>Primary</b><span>Gradient version</span>', 'paper', gallery='ids')}
          {fig('rmn-logo-red', 'RMN Lanka Automation logo, red and blue', '<b>Two colour</b><span>Red and blue</span>', 'paper', gallery='ids')}
          {fig('rmn-logo-black', 'RMN Lanka Automation logo, black', '<b>One colour</b><span>Black</span>', 'paper', gallery='ids')}
          {fig('rmn-post', 'RMN Lanka Automation Sinhala ad', '<b>Machine ad</b><span>Sinhala, square</span>', 'tall', gallery='ids')}
        </div>
      </article>
      <article class="id-block">
        <h3 class="id-name"><span class="label">B</span>Nethmina Motors</h3>
        <p class="id-note">Helmet and spanners for a bike repair and service shop, and an A4 flyer listing every service with a free inspection offer.</p>
        <div class="g-neth">
          {fig('nethmina-logo', 'Nethmina Motors logo', '<b>Logo</b><span>Repairing and services</span>', 'paper', gallery='ids')}
          {fig('nethmina-flyer', 'Nethmina Motors service flyer', '<b>Flyer</b><span>A4, services and hours</span>', gallery='ids')}
        </div>
      </article>
      <article class="id-block">
        <h3 class="id-name"><span class="label">C</span>Sanjula Gaming</h3>
        <p class="id-note">A streamer avatar drawn from a photo, then pushed into neon badges and a channel cover.</p>
        {fig('sanju-cover', 'Sanjula Gaming channel cover', '<b>Channel cover</b><span>Wide banner</span>', 'wide', gallery='ids')}
        <ol class="g-sanju">{sanju}</ol>
      </article>
    </div>
  </section>''')

    # --- 07 Logos
    boards = ''.join(fig(f'logos-{i}', 'Logo presentation board', f'<b>Board {i:02d}</b><span>Logo concepts</span>', 'first' if i == 1 else '', gallery='logos') for i in range(1, 8))
    s.append(f'''
  <section class="chapter wrap" id="d-logos">
    {chapter_head('07', 'Logo boards', 'More marks', 'Presentation boards for logo concepts: travel, a dance academy, an app called Unlock, a garden brand and more. Each board shows the mark the way a client first sees it.', [('Format', '16:9 boards'), ('Tools', 'Illustrator, CorelDRAW')], 'Concepts')}
    <div class="g-logos">{boards}</div>
  </section>''')

    # --- 08 About
    s.append(about('d', designer=True))
    return '\n'.join(s)

def about(p, designer):
    if designer:
        bio = ('<p>I\'m Charith, a designer from Colombo. My day job is marine graphics and production at North Manufacturing, where I make the sail graphics, calendars and print for North Sails and Future Fibres, and run the laser cutter and vinyl plotter that turn them into real things.</p>'
               '<p>Before that I freelanced for five years on Fiverr, mostly logos and brand identities for clients abroad. I also write small Illustrator scripts that take the boring steps out of prepress.</p>')
        exp = [('2025 — now', 'Marine Graphic Designer & Production Coordinator', 'North Manufacturing (Pvt) Ltd'),
               ('2020 — 2025', 'Freelance Designer', 'Fiverr, international clients')]
        tools = ['Illustrator', 'CorelDRAW', 'Photoshop', 'Flexi Complete', 'LaserCAD', 'Cutting Master', 'Figma', 'Framer', 'ExtendScript', 'Pantone', 'RAL']
        ask = 'Got a sail, a brand or a print job?'
    else:
        bio = ('<p>I\'m Charith. At Thinex Enterprises I work between the people who sell, stock and ship things and the data that says how it\'s going. I gather what they need, map how the work really moves, then build the reports and fixes.</p>'
               '<p>I came to this through IT administration and software work, and I\'m finishing a BSc in Business Information Systems.</p>')
        exp = [('Aug 2024 — now', 'Business Analyst', 'Thinex Enterprises (Pvt) Ltd'),
               ('2021 — 2023', 'IT Administrator', 'DC Engineers'),
               ('2020 — 2025', 'Freelance Software Consultant', 'Fiverr, international clients'),
               ('2026', 'BSc (Hons) Business Information Systems', 'Cardiff Metropolitan University, ICBT'),
               ('2024', 'Higher Diploma, Software Engineering & CS', 'Cardiff Metropolitan University, ICBT')]
        tools = ['SQL', 'Excel', 'Power Query', 'Power BI', 'RStudio', 'SPSS', 'QGIS', 'Dynamics 365', 'JavaScript', 'Node.js', 'PHP', 'Python', 'Java']
        ask = 'Got a process that needs a second look?'
    exp_html = ''.join(f'<li><span class="label">{w}</span><b>{r}</b><span>{o}</span></li>' for w, r, o in exp)
    tools_html = ''.join(f'<li>{t}</li>' for t in tools)
    num = '08' if designer else '05'
    return f'''
  <section class="chapter about wrap" id="{p}-about">
    <div class="about__grid">
      <figure class="about__photo reveal"><img src="assets/img/portrait.webp" alt="Charith Sulakshana" width="{MAN['portrait'][0]}" height="{MAN['portrait'][1]}" loading="lazy"><figcaption class="label">Charith Sulakshana · Colombo</figcaption></figure>
      <div class="about__text">
        <div class="ch-row label reveal"><span>Chapter {num}</span><span>About me</span></div>
        <h2 class="ch-title reveal">Hello.</h2>
        <div class="about__bio reveal">{bio}</div>
        <ol class="exp reveal">{exp_html}</ol>
        <ul class="tools reveal">{tools_html}</ul>
      </div>
    </div>
    <div class="contact reveal" id="{p}-contact">
      <p class="label">Contact</p>
      <p class="contact__ask">{ask}</p>
      <div class="contact__row">
        <span class="contact__mail" data-email>charithsulakshana2003@gmail.com</span>
        <button type="button" class="btn" data-copy>Copy email</button>
        <a class="btn" href="https://www.linkedin.com/in/charith-sulakshana-1625a3306" target="_blank" rel="noopener">LinkedIn ↗</a>
        <span class="contact__msg label" data-copymsg aria-live="polite"></span>
      </div>
    </div>
  </section>'''

# ----------------------------------------------------------------------------
# CONTENT — Business Analyst
# ----------------------------------------------------------------------------
def analyst():
    s = []
    w, h = MAN['thinex-overview']
    s.append(f'''
  <section class="cover cover--a" id="a-top" aria-label="Cover">
    <div class="wrap cover__grid">
      <div class="cover__copy">
        <p class="label cover__vol"><span>Vol. 01</span><span>Case notes</span><span>2026</span></p>
        <h1 class="cover__title"><span class="split">Business</span><span class="split">Analyst</span></h1>
        <p class="label cover__role">Charith Sulakshana &nbsp;·&nbsp; Thinex Enterprises</p>
        <p class="cover__lead">I sit between the people who sell, stock and ship, and the data behind it. I find out what they need, map how the work actually moves, and build the report or the fix.</p>
        <ul class="label cover__index cover__index--row"><li>Requirements</li><li>Process</li><li>Data</li><li>Decisions</li></ul>
      </div>
      <div class="cover__art cover__art--a">
        <div class="screen" data-screen>
          <div class="screen__bar"><i></i><i></i><i></i><span>Thinex Sales.pbix · Executive Overview</span></div>
          <img src="assets/img/thinex-overview.webp" alt="Power BI executive overview built for Thinex: revenue, gross profit, margin, orders, channel and category" width="{w}" height="{h}" loading="eager">
        </div>
        <p class="label screen__note">The real report, open in Power BI Desktop</p>
      </div>
    </div>
    <div class="cover__bar"></div>
  </section>''')

    toc = [('01', 'Thinex sales dashboard', 'Power BI · 3 pages', 'a-thinex'),
           ('02', 'Order to delivery', 'Process mapping · 25% faster', 'a-process'),
           ('03', 'CryptoRateX', 'Real-time dashboard · live site', 'a-crx'),
           ('04', 'Other systems', 'FixPoint and two smaller builds', 'a-systems'),
           ('05', 'About me', 'Experience, education, tools', 'a-about')]
    rows = ''.join(f'<li><a href="#{a}"><span class="n">{n}</span><span class="t">{t}</span><span class="dots" aria-hidden="true"></span><span class="m">{m}</span></a></li>' for n, t, m, a in toc)
    s.append(f'''
  <section class="contents wrap" aria-labelledby="a-contents-t">
    <div class="contents__head reveal"><p class="label" id="a-contents-t">Contents</p><p class="contents__note">What I've built and changed, with the screens to show for it.</p></div>
    <ol class="toc reveal">{rows}</ol>
    <ul class="numbers reveal">
      <li><b><span data-count="25">25</span>%</b><span>faster order processing after fixing three bottlenecks</span></li>
      <li><b><span data-count="3">3</span> h</b><span>of manual reporting saved every week</span></li>
      <li><b>~<span data-count="20">20</span>%</b><span>fewer stock-outs from a reorder-point model</span></li>
      <li><b>~<span data-count="2">2</span>M</b><span>slow-moving stock found in a year of data</span></li>
    </ul>
  </section>''')

    tabs = [('thinex-overview', 'Executive Overview', 'Revenue and gross margin by month, with revenue split by channel (store, website, marketplace) and by product category. This is the page management opens first.'),
            ('thinex-inventory', 'Inventory & Working Capital', 'Average stock value, turnover, days of stock and the slow-moving stock figure, plus stock value over time and by category. This is where the slow stock showed up.'),
            ('thinex-campaigns', 'Campaigns', 'Spend against revenue for each online campaign, with ROI, so the team can see which promotions to run again and which to drop.')]
    btns = ''.join(f'<button type="button" role="tab" class="tab label" data-tab="{i}" aria-selected="{"true" if i == 0 else "false"}">{t}</button>' for i, (_, t, _) in enumerate(tabs))
    panes = ''.join(f'<div class="pane" data-pane="{i}"{"" if i == 0 else " hidden"}><div class="screen screen--flat"><div class="screen__bar"><i></i><i></i><i></i><span>Thinex Sales.pbix · {t}</span></div>{img(sl, t + " page of the Thinex Power BI report", gallery="thinex", cap=f"<b>{t}</b><span>Thinex Power BI report</span>")}</div><p class="pane__note">{d}</p></div>' for i, (sl, t, d) in enumerate(tabs))
    s.append(f'''
  <section class="chapter wrap" id="a-thinex">
    {chapter_head('01', 'Reporting', 'Thinex sales<br>dashboard', 'Thinex sells IT gear through stores, a website and online marketplaces, and the weekly numbers used to be put together by hand. I built this Power BI report on SQL and Power Query instead. It saves about three hours a week and it\'s where the inventory and campaign findings came from.', [('For', 'Thinex Enterprises'), ('Tools', 'Power BI, SQL, Power Query, Excel'), ('Pages', '3')], 'Power BI')}
    <div class="tabs reveal"><div class="tabs__list" role="tablist" aria-label="Report pages">{btns}</div>{panes}</div>
  </section>''')

    steps = [('Order received', 10, 10, 0), ('Payment check', 45, 30, 1), ('Stock pick', 60, 45, 1), ('Pack & label', 25, 25, 0), ('Dispatch handover', 40, 25, 1)]
    rows = ''.join(f'<li class="{"hot" if hot else ""}" data-b="{b}" data-a="{a}"><span class="label">{i+1:02d}</span><b>{n}{"<em>bottleneck</em>" if hot else ""}</b><span class="bar"><i style="--w:{b/60*100:.1f}%"></i></span><span class="min">{b}m</span></li>' for i, (n, b, a, hot) in enumerate(steps))
    s.append(f'''
  <section class="chapter wrap" id="a-process">
    {chapter_head('02', 'Process', 'Order to<br>delivery', 'I walked an order through the business with sales, the warehouse and dispatch, and drew every step. Timing them showed three places where orders waited. We changed those three things and average processing time dropped by a quarter.', [('Result', '25% faster on average'), ('Method', 'Process mapping, gap analysis')], 'Process improvement')}
    <div class="flow reveal" data-flow>
      <div class="flow__head"><div class="seg" role="group" aria-label="Before or after"><button type="button" class="label on" data-state="b" aria-pressed="true">Before</button><button type="button" class="label" data-state="a" aria-pressed="false">After</button></div><p class="flow__total"><b data-total>180</b> min per order <span data-delta>−25%</span></p></div>
      <ol class="flow__rows">{rows}</ol>
      <p class="flow__note label">Step timings here are illustrative. The 25% is the real average.</p>
    </div>
  </section>''')

    s.append(f'''
  <section class="chapter wrap" id="a-crx">
    {chapter_head('03', 'Side project', 'CryptoRateX', 'A dashboard I built. It streams funding rates, open interest, volume and long/short ratios for every Binance USDT perpetual pair over WebSockets (748 of them when I took these), and sends Telegram alerts when a pair crosses a threshold you set.', [('Stack', 'JavaScript, WebSockets, Telegram Bot API'), ('Live', '<a href="https://cryptoratex.com" target="_blank" rel="noopener">cryptoratex.com ↗</a>')], 'Real-time data')}
    <div class="g-crx">
      {fig('crx-1', 'CryptoRateX dashboard sorted by open interest', '<b>Dashboard</b><span>Sorted by open interest</span>', 'wide', gallery='crx')}
      {fig('crx-2', 'CryptoRateX dashboard with funding sentiment', '<b>Funding view</b><span>Sentiment tags per pair</span>', gallery='crx')}
      {fig('crx-alert', 'CryptoRateX Telegram alert setup', '<b>Set alert</b><span>Telegram threshold alerts</span>', gallery='crx')}
    </div>
  </section>''')

    s.append(f'''
  <section class="chapter wrap" id="a-systems">
    {chapter_head('04', 'Systems', 'Other builds', 'Smaller systems from my software diploma and freelance work, where I did the analysis and the build.', [('Stack', 'PHP, MySQL, Java, C++')], 'Development')}
    <div class="systems reveal">
      <article><p class="label">B2B platform</p><h3>FixPoint</h3><p>A machinery repair marketplace. A company logs a breakdown with the fault and how urgent it is, and a matching algorithm pairs it with a technician by location, skills, availability and track record. I modelled the database and the whole flow from job posted to technician assigned.</p><p class="label sys-stack">PHP · MySQL · JavaScript</p></article>
      <article><p class="label">Internal system</p><h3>Employee management</h3><p>Role-based system for employees, departments and designations, with logins for different user types and filters to find records fast.</p><p class="label sys-stack">Java · Java GUI</p></article>
      <article><p class="label">Automation</p><h3>Bakery orders &amp; invoices</h3><p>Replaced a paper ordering process: browse products, apply discount rules, take payment and print the invoice.</p><p class="label sys-stack">C++</p></article>
    </div>
  </section>''')
    s.append(about('a', designer=False))
    return '\n'.join(s)

# ----------------------------------------------------------------------------
TEMPLATE = open(os.path.join(HERE, 'template.html')).read()
LOGO = open(os.path.join(HERE, 'assets/logo.svg')).read()
paths = re.findall(r'<path class="cls-1" d="([^"]+)"/>', LOGO)
out = (TEMPLATE.replace('{{LOGO_PATHS}}', '\n'.join(f'      <path d="{p}"/>' for p in paths))
       .replace('{{DESIGNER}}', designer())
       .replace('{{ANALYST}}', analyst()))
open(os.path.join(HERE, 'index.html'), 'w').write(out)
print('built index.html', len(out))
