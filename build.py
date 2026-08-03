#!/usr/bin/env python3
"""
Static site builder for the ASDG (CUSAT) group website.

Why this exists: the site is plain static HTML (drop it in any web host or a
GitHub Pages repo), but the header, footer and <head> are identical on every
page. Rather than hand-maintain eight copies, we define them once here and
stamp out the final .html files. Edit content in the PAGES dict, run
`python3 build.py`, and re-upload. You can also just edit the generated .html
directly if you prefer — the output is 100% standalone.
"""

import os

SITE = {
    "name": "ASDG",
    "full": "Advanced Sensing &amp; Diagnostics Group",
    "sub": "CUSAT · School of Engineering",
    "dept": "Cochin University of Science and Technology",
    "pi": "Prof. Biju N",
    "email": "asdg@cusat.ac.in",
    "phone": "+91 484 XXXX XXX",
    "addr": "School of Engineering, CUSAT,<br>Kalamassery, Kochi, Kerala 682022, India",
}

# ---- Inline SVG icons (stroke = currentColor) --------------------------------
IC = {
    "arrow": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>',
    "chev": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 12 15 18 9"/></svg>',
    "menu": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><line x1="3" y1="7" x2="21" y2="7"/><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="17" x2="21" y2="17"/></svg>',
    "mail": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="5" width="18" height="14" rx="2"/><polyline points="3 7 12 13 21 7"/></svg>',
    "phone": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3 19.5 19.5 0 0 1-6-6 19.8 19.8 0 0 1-3-8.6A2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.3 1.8.6 2.6a2 2 0 0 1-.5 2.1L8.1 9.9a16 16 0 0 0 6 6l1.5-1.1a2 2 0 0 1 2.1-.5c.8.3 1.7.5 2.6.6a2 2 0 0 1 1.7 2z"/></svg>',
    "pin": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>',
    "clock": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><polyline points="12 7 12 12 15 14"/></svg>',
    "linkedin": '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M4.98 3.5A2.5 2.5 0 1 1 0 3.5a2.5 2.5 0 0 1 4.98 0zM.25 8h4.5v14H.25zM8.5 8h4.3v1.9h.06c.6-1.1 2.06-2.26 4.24-2.26 4.53 0 5.37 2.98 5.37 6.86V22h-4.5v-6.2c0-1.48-.03-3.38-2.06-3.38-2.06 0-2.38 1.6-2.38 3.27V22H8.5z"/></svg>',
    "scholar": '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 3 1 9l11 6 9-4.9V17h2V9zM5 13.2V17c0 1.7 3.13 3 7 3s7-1.3 7-3v-3.8l-7 3.8z"/></svg>',
    "gate": '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2a10 10 0 1 0 0 20 10 10 0 0 0 0-20zm3.3 6.4c1.2 0 2 .8 2 2 0 1.5-1.4 2.6-3.4 4.3l-.8.6h4v1.6H8.2v-1.3c2.7-2.3 4.9-3.7 4.9-5 0-.6-.4-1-1-1s-1 .5-1 1.2H8.4c0-1.9 1.4-3.2 3.4-3.2z"/></svg>',
    "x": '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M18.9 2h3.3l-7.2 8.2L23.5 22h-6.6l-5.2-6.8L5.8 22H2.5l7.7-8.8L1.8 2h6.8l4.7 6.2zM17.7 20h1.8L7.1 3.9H5.1z"/></svg>',
    "youtube": '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M23 7.5a3 3 0 0 0-2.1-2.1C19 5 12 5 12 5s-7 0-8.9.4A3 3 0 0 0 1 7.5 31 31 0 0 0 .6 12 31 31 0 0 0 1 16.5a3 3 0 0 0 2.1 2.1C5 19 12 19 12 19s7 0 8.9-.4a3 3 0 0 0 2.1-2.1 31 31 0 0 0 .4-4.5 31 31 0 0 0-.4-4.5zM9.8 15.3V8.7l5.7 3.3z"/></svg>',
    "flask": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M9 3h6M10 3v6.5L4.6 18a2 2 0 0 0 1.7 3h11.4a2 2 0 0 0 1.7-3L14 9.5V3"/><line x1="7" y1="15" x2="17" y2="15"/></svg>',
    "wave": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M2 12c2 0 2-5 4-5s2 10 4 10 2-14 4-14 2 9 4 9 2-5 4-5"/></svg>',
    "chip": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="6" y="6" width="12" height="12" rx="2"/><path d="M9 2v3M15 2v3M9 19v3M15 19v3M2 9h3M2 15h3M19 9h3M19 15h3"/></svg>',
    "brain": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M9.5 3A2.5 2.5 0 0 0 7 5.5c-1.4.2-2.5 1.4-2.5 2.9 0 .5.1.9.3 1.3A3 3 0 0 0 4 12a3 3 0 0 0 1.3 2.5A2.9 2.9 0 0 0 8 19a2.5 2.5 0 0 0 4-2V5.5A2.5 2.5 0 0 0 9.5 3zM14.5 3A2.5 2.5 0 0 1 17 5.5c1.4.2 2.5 1.4 2.5 2.9 0 .5-.1.9-.3 1.3A3 3 0 0 1 20 12a3 3 0 0 1-1.3 2.5A2.9 2.9 0 0 1 16 19a2.5 2.5 0 0 1-4-2"/></svg>',
    "gauge": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M12 14a2 2 0 1 0 0-4 2 2 0 0 0 0 4z"/><path d="m13.4 12.6 3.6-3.6"/><path d="M3.5 18a9 9 0 1 1 17 0"/></svg>',
    "shield": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>',
    "book": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20V3H6.5A2.5 2.5 0 0 0 4 5.5z"/></svg>',
    "download": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>',
}

# ---- Navigation model --------------------------------------------------------
NAV = [
    ("Home", "index.html", None),
    ("About", "about.html", [
        ("Overview", "about.html"),
        ("Director's Message", "about.html#director"),
        ("Mission &amp; Vision", "about.html#mission"),
    ]),
    ("Research", "research.html", [
        ("Focus Areas", "research.html#focus"),
        ("Research Themes", "research.html#themes"),
        ("Current Projects", "research.html#projects"),
        ("Publications", "publications.html"),
    ]),
    ("People", "people.html", [
        ("Principal Investigator", "people.html#pi"),
        ("Research Scholars", "people.html#scholars"),
        ("Students", "people.html#students"),
        ("Alumni", "people.html#alumni"),
    ]),
    ("Facilities", "facilities.html", None),
    ("News", "news.html", None),
    ("Contact", "contact.html", None),
]


def nav_html(active):
    items = []
    for label, href, drop in NAV:
        is_active = (href == active)
        if drop:
            sub = "".join(f'<a href="{d[1]}">{d[0]}</a>' for d in drop)
            items.append(
                f'<li class="nav__item has-drop">'
                f'<a class="nav__link{" active" if is_active else ""}" href="{href}">{label}'
                f'<span class="chev">{IC["chev"]}</span></a>'
                f'<div class="nav__drop">{sub}</div></li>'
            )
        else:
            items.append(
                f'<li class="nav__item">'
                f'<a class="nav__link{" active" if is_active else ""}" href="{href}">{label}</a></li>'
            )
    return "".join(items)


def head(title, desc, active):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} · {SITE['name']} — {SITE['dept']}</title>
<meta name="description" content="{desc}">
<link rel="icon" type="image/svg+xml" href="assets/favicon.svg">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Source+Serif+4:ital,opsz,wght@0,8..60,400;0,8..60,600;0,8..60,700;1,8..60,400&family=Inter:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="css/style.css">
</head>
<body>
<div class="nav-overlay"></div>

<!-- Top utility bar -->
<div class="topbar">
  <div class="wrap">
    <div class="topbar__left">
      <span>{SITE['dept']}</span>
      <a href="mailto:{SITE['email']}">{SITE['email']}</a>
    </div>
    <div class="topbar__social" aria-label="Social links">
      <a href="#" aria-label="LinkedIn">{IC['linkedin']}</a>
      <a href="#" aria-label="Google Scholar">{IC['scholar']}</a>
      <a href="#" aria-label="ResearchGate">{IC['gate']}</a>
      <a href="#" aria-label="YouTube">{IC['youtube']}</a>
    </div>
  </div>
</div>

<!-- Main header -->
<header class="site-header">
  <div class="wrap">
    <nav class="nav" aria-label="Primary">
      <a class="brand" href="index.html">
        <span class="brand__mark"><img src="assets/favicon.svg" alt="{SITE['name']} logo" width="44" height="44"></span>
        <span class="brand__text">
          <span class="brand__name">{SITE['name']}</span>
          <span class="brand__sub">{SITE['sub']}</span>
        </span>
      </a>
      <ul class="nav__menu">
        {nav_html(active)}
      </ul>
      <a class="btn btn--primary nav__cta" href="contact.html">Join the Group {IC['arrow']}</a>
      <button class="nav__toggle" aria-label="Open menu" aria-expanded="false">{IC['menu']}</button>
    </nav>
  </div>
</header>
"""


def footer():
    quick = "".join(
        f'<li><a href="{h}">{l}</a></li>'
        for l, h, _ in NAV if l != "Home"
    )
    research_links = "".join(
        f'<li><a href="{h}">{l}</a></li>' for l, h in [
            ("Focus Areas", "research.html#focus"),
            ("Publications", "publications.html"),
            ("Facilities", "facilities.html"),
            ("Open Positions", "contact.html"),
            ("Annual Report", "#"),
        ])
    return f"""
<footer class="footer">
  <div class="wrap">
    <div class="footer__top">
      <div class="footer__brand">
        <div class="brand">
          <span class="brand__mark"><img src="assets/favicon.svg" alt="" width="40" height="40"></span>
          <span class="brand__text"><span class="brand__name">{SITE['name']}</span>
          <span class="brand__sub">{SITE['sub']}</span></span>
        </div>
        <p>{SITE['full']} — a research group at {SITE['dept']} advancing sensing, diagnostics and intelligent condition monitoring for engineered systems.</p>
        <div class="footer__social">
          <a href="#" aria-label="LinkedIn">{IC['linkedin']}</a>
          <a href="#" aria-label="Google Scholar">{IC['scholar']}</a>
          <a href="#" aria-label="ResearchGate">{IC['gate']}</a>
          <a href="#" aria-label="X">{IC['x']}</a>
          <a href="#" aria-label="YouTube">{IC['youtube']}</a>
        </div>
      </div>
      <div>
        <h4>Explore</h4>
        <ul class="footer__links">{quick}</ul>
      </div>
      <div>
        <h4>Research</h4>
        <ul class="footer__links">{research_links}</ul>
      </div>
      <div>
        <h4>Contact</h4>
        <ul class="footer__links">
          <li><a href="mailto:{SITE['email']}">{SITE['email']}</a></li>
          <li><a href="tel:+91484">{SITE['phone']}</a></li>
          <li style="color:#a89fa1;line-height:1.5;margin-top:.4rem">{SITE['addr']}</li>
        </ul>
      </div>
    </div>
    <div class="footer__bottom">
      <span>© <span id="year">2025</span> {SITE['full']}, {SITE['dept']}. All rights reserved.</span>
      <span>Placeholder content · Lorem ipsum &amp; Picsum imagery · <a href="#" class="ulink" style="color:#b6adaf">Privacy</a></span>
    </div>
  </div>
</footer>
<script src="js/main.js"></script>
</body>
</html>"""


def page(filename, title, desc, active, body):
    html = head(title, desc, active) + body + footer()
    with open(filename, "w", encoding="utf-8") as f:
        f.write(html)
    print("  wrote", filename)


# =============================================================================
#  Reusable content blocks
# =============================================================================
LOREM = ("Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod "
         "tempor incididunt ut labore et dolore magna aliqua.")
LOREM2 = ("Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut "
          "aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit.")


def img(seed, w, h):
    return f"https://picsum.photos/seed/{seed}/{w}/{h}"


def banner(title, sub, crumb, seed):
    return f"""
<section class="pagebanner">
  <div class="pagebanner__bg" style="background-image:url('{img(seed, 1600, 700)}')"></div>
  <div class="pagebanner__scrim"></div>
  <div class="wrap pagebanner__inner">
    <nav class="breadcrumb"><a href="index.html">Home</a><span>/</span>{crumb}</nav>
    <h1>{title}</h1>
    <p class="lede">{sub}</p>
  </div>
</section>"""


def cta_band():
    return f"""
<section class="section section--tight">
  <div class="wrap">
    <div class="cta-band reveal">
      <span class="eyebrow eyebrow--light">Work with us</span>
      <h2>Interested in sensing, diagnostics and machine learning for real systems?</h2>
      <p>We welcome motivated PhD, M.Tech and project candidates, along with academic and industry collaborators. Reach out to explore openings and joint research.</p>
      <div class="hero__actions">
        <a class="btn btn--light" href="contact.html">Get in touch {IC['arrow']}</a>
        <a class="btn btn--outline-light" href="people.html">Meet the team</a>
      </div>
    </div>
  </div>
</section>"""


# =============================================================================
#  PAGE: Home
# =============================================================================
def build_home():
    slides = "".join(
        f'<div class="hero__slide{" active" if i==0 else ""}" style="background-image:url(\'{img("hero"+str(i), 1800, 1000)}\')"></div>'
        for i in range(4)
    )
    dots = "".join(f'<button class="hero__dot{" active" if i==0 else ""}" aria-label="Slide {i+1}"></button>' for i in range(4))

    focus = [
        ("01", "structural", "Structural Health Monitoring", "Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae."),
        ("02", "diag", "Fault Diagnosis &amp; Prognosis", "Nunc dignissim risus id metus. Cras ornare tristique elit at bibendum finibus lorem."),
        ("03", "signal", "Signal Processing &amp; AI", "Curabitur sit amet mauris morbi in dui quis est pulvinar ullamcorper nulla facilisi."),
    ]
    focus_cards = "".join(
        f"""<article class="fcard reveal d{i%3+1}">
          <div class="fcard__media"><span class="fcard__index">{idx}</span><img src="{img(s,700,440)}" alt="{t}" loading="lazy"></div>
          <div class="fcard__body"><h3>{t}</h3><p>{d}</p>
          <a class="fcard__more" href="research.html">Explore theme {IC['arrow']}</a></div>
        </article>""" for i,(idx,s,t,d) in enumerate(focus)
    )

    tiles = [
        ("wave", "Vibration &amp; Acoustics", "Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque."),
        ("chip", "Sensor Systems", "Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit sed quia."),
        ("brain", "Machine Learning", "Neque porro quisquam est qui dolorem ipsum quia dolor sit amet consectetur adipisci."),
        ("gauge", "Condition Monitoring", "Ut enim ad minima veniam quis nostrum exercitationem ullam corporis suscipit laboriosam."),
        ("shield", "Reliability Engineering", "Quis autem vel eum iure reprehenderit qui in ea voluptate velit esse quam nihil."),
        ("flask", "Experimental Mechanics", "At vero eos et accusamus et iusto odio dignissimos ducimus qui blanditiis praesentium."),
    ]
    tile_html = "".join(
        f"""<div class="tile reveal d{i%3+1}"><div class="tile__icon">{IC[ic]}</div>
        <h3>{t}</h3><p>{d}</p></div>""" for i,(ic,t,d) in enumerate(tiles)
    )

    news = [
        ("news1", "Mar 2025", "Group paper accepted at leading diagnostics journal", LOREM),
        ("news2", "Feb 2025", "New sponsored project on intelligent monitoring begins", LOREM),
        ("news3", "Jan 2025", "Two scholars present at international conference", LOREM),
    ]
    news_html = "".join(
        f"""<article class="news-card reveal d{i%3+1}">
        <div class="news-card__media"><img src="{img(s,600,340)}" alt="" loading="lazy"></div>
        <div class="news-card__body"><span class="news-card__date">{dt}</span>
        <h3>{t}</h3><p>{d}</p><a class="fcard__more" href="news.html">Read more {IC['arrow']}</a></div>
        </article>""" for i,(s,dt,t,d) in enumerate(news)
    )

    logos = "".join(
        f'<div class="logos__cell"><img src="{img("logo"+str(i),200,90)}" alt="Partner logo"></div>'
        for i in range(6)
    )

    body = f"""
<!-- HERO -->
<section class="hero">
  <div class="hero__slides">{slides}</div>
  <div class="hero__scrim"></div>
  <div class="hero__grid-accent"></div>
  <div class="wrap hero__inner">
    <span class="eyebrow hero__eyebrow">{SITE['dept']}</span>
    <h1>Sensing the invisible, <span class="accent">diagnosing</span> the future of engineered systems.</h1>
    <p class="hero__lede">{SITE['full']} develops advanced sensing, signal processing and machine-learning methods to detect, diagnose and predict faults in mechanical and structural systems — before they fail.</p>
    <div class="hero__actions">
      <a class="btn btn--light" href="research.html">Explore our research {IC['arrow']}</a>
      <a class="btn btn--outline-light" href="people.html">Meet the team</a>
    </div>
  </div>
  <div class="hero__dots">{dots}</div>
</section>

<!-- STAT RIBBON -->
<section class="ribbon">
  <div class="wrap">
    <div class="ribbon__grid">
      <div class="ribbon__cell"><div class="ribbon__num">40+</div><div class="ribbon__label">Publications</div></div>
      <div class="ribbon__cell"><div class="ribbon__num">12</div><div class="ribbon__label">Research Scholars</div></div>
      <div class="ribbon__cell"><div class="ribbon__num">08</div><div class="ribbon__label">Funded Projects</div></div>
      <div class="ribbon__cell"><div class="ribbon__num">15+</div><div class="ribbon__label">Industry Partners</div></div>
    </div>
  </div>
</section>

<!-- INTRO SPLIT -->
<section class="section">
  <div class="wrap">
    <div class="split">
      <div class="reveal">
        <span class="eyebrow">Who we are</span>
        <h2>A research group where measurement meets intelligence.</h2>
        <p class="lede" style="margin-top:1rem">Led by {SITE['pi']}, the group brings together instrumentation, dynamics and data science to make machines observable, interpretable and trustworthy.</p>
        <p style="margin-top:1rem">{LOREM} {LOREM2}</p>
        <div class="chips">
          <span class="chip">Diagnostics</span><span class="chip">Prognostics</span>
          <span class="chip">Sensors</span><span class="chip">Signal Processing</span>
          <span class="chip">Deep Learning</span><span class="chip">Reliability</span>
        </div>
        <div style="margin-top:1.8rem"><a class="btn btn--primary" href="about.html">More about the group {IC['arrow']}</a></div>
      </div>
      <div class="split__media reveal d1"><img src="{img('labwork',760,570)}" alt="Researchers working in the laboratory"></div>
    </div>
  </div>
</section>

<!-- FOCUS AREAS -->
<section class="section section--paper2">
  <div class="wrap">
    <div class="section-head reveal">
      <span class="eyebrow">Research focus</span>
      <h2>Three pillars, one goal: engineered systems that never fail unexpectedly.</h2>
      <p>Our work spans the full pipeline — from placing the right sensor to raising the right alarm at the right time.</p>
    </div>
    <div class="grid grid--3">{focus_cards}</div>
  </div>
</section>

<!-- CAPABILITY TILES -->
<section class="section">
  <div class="wrap">
    <div class="section-head reveal">
      <span class="eyebrow">Capabilities</span>
      <h2>What we work on</h2>
    </div>
    <div class="grid grid--3">{tile_html}</div>
  </div>
</section>

<!-- MISSION preview on ink -->
<section class="section section--ink">
  <div class="wrap">
    <div class="split">
      <div class="reveal">
        <span class="eyebrow eyebrow--light">Our purpose</span>
        <h2 style="color:#fff">Deep-research diagnostics for safer, longer-living machines and structures.</h2>
        <p style="color:rgba(255,255,255,.82);margin-top:1rem">{LOREM}</p>
        <div style="margin-top:1.6rem"><a class="btn btn--light" href="about.html#mission">Mission, vision &amp; values {IC['arrow']}</a></div>
      </div>
      <div class="reveal d1">
        <div class="mv-list">
          <div class="mv-item"><span class="mv-item__badge">M</span><div><h4 style="color:#fff">Mission</h4><p style="color:rgba(255,255,255,.75)">{LOREM}</p></div></div>
          <div class="mv-item"><span class="mv-item__badge">V</span><div><h4 style="color:#fff">Vision</h4><p style="color:rgba(255,255,255,.75)">{LOREM2}</p></div></div>
        </div>
      </div>
    </div>
  </div>
</section>

<!-- NEWS -->
<section class="section section--paper2">
  <div class="wrap">
    <div class="section-head reveal" style="display:flex;justify-content:space-between;align-items:end;max-width:none;gap:1rem;flex-wrap:wrap">
      <div><span class="eyebrow">Latest</span><h2>News &amp; announcements</h2></div>
      <a class="btn btn--ghost" href="news.html">All news {IC['arrow']}</a>
    </div>
    <div class="grid grid--3">{news_html}</div>
  </div>
</section>

<!-- PARTNERS -->
<section class="section">
  <div class="wrap">
    <div class="section-head reveal" style="text-align:center;margin-inline:auto">
      <span class="eyebrow" style="justify-content:center">Collaborators</span>
      <h2>Trusted by partners in industry and academia</h2>
    </div>
    <div class="logos reveal">{logos}</div>
  </div>
</section>

{cta_band()}
"""
    page("index.html", "Home", "Advanced Sensing & Diagnostics Group at CUSAT — research in sensing, fault diagnosis, prognostics and machine learning for engineered systems.", "index.html", body)


# =============================================================================
#  PAGE: About
# =============================================================================
def build_about():
    values = ["Excellence", "Integrity", "Curiosity", "Rigour", "Collaboration", "Impact"]
    chips = "".join(f'<span class="chip">{v}</span>' for v in values)
    body = banner("About the Group",
                  f"{SITE['full']} unites instrumentation, dynamics and data science under one roof at {SITE['dept']}.",
                  "About", "aboutbn") + f"""
<section class="section">
  <div class="wrap">
    <div class="split">
      <div class="reveal">
        <span class="eyebrow">Overview</span>
        <h2>Making machines observable, interpretable and trustworthy.</h2>
        <p style="margin-top:1rem">{LOREM} {LOREM2}</p>
        <p style="margin-top:1rem">{LOREM}</p>
      </div>
      <div class="split__media reveal d1"><img src="{img('grouplab',760,570)}" alt="Group laboratory"></div>
    </div>
  </div>
</section>

<!-- DIRECTOR -->
<section id="director" class="section section--paper2">
  <div class="wrap">
    <div class="section-head reveal"><span class="eyebrow">Message</span><h2>From the Principal Investigator</h2></div>
    <div class="director reveal">
      <div class="director__photo"><img src="{img('director',400,520)}" alt="{SITE['pi']}"></div>
      <div>
        <div class="director__name">{SITE['pi']}</div>
        <div class="director__title">Principal Investigator · {SITE['sub']}</div>
        <p>{LOREM}</p>
        <blockquote>"Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam."</blockquote>
        <p>{LOREM2} {LOREM}</p>
        <div style="margin-top:1.4rem;display:flex;gap:.8rem;flex-wrap:wrap">
          <a class="btn btn--ghost" href="#">{IC['scholar']} Google Scholar</a>
          <a class="btn btn--ghost" href="#">{IC['gate']} ResearchGate</a>
        </div>
      </div>
    </div>
  </div>
</section>

<!-- MISSION / VISION / VALUES -->
<section id="mission" class="section">
  <div class="wrap">
    <div class="section-head reveal"><span class="eyebrow">Our purpose</span><h2>Mission, vision &amp; values</h2></div>
    <div class="grid grid--2" style="margin-bottom:1.5rem">
      <div class="tile reveal"><div class="tile__icon">{IC['gauge']}</div><h3>Mission</h3><p>{LOREM} {LOREM2}</p></div>
      <div class="tile reveal d1"><div class="tile__icon">{IC['brain']}</div><h3>Vision</h3><p>{LOREM2} {LOREM}</p></div>
    </div>
    <div class="reveal">
      <span class="eyebrow">Values</span>
      <div class="chips">{chips}</div>
    </div>
  </div>
</section>

<!-- TIMELINE / MILESTONES -->
<section class="section section--paper2">
  <div class="wrap">
    <div class="section-head reveal"><span class="eyebrow">Journey</span><h2>Milestones</h2></div>
    <div class="grid grid--4">
      <div class="tile reveal"><div class="pub__year">2018</div><p style="margin-top:.6rem">Group established at {SITE['dept']}.</p></div>
      <div class="tile reveal d1"><div class="pub__year">2020</div><p style="margin-top:.6rem">First major sponsored project awarded.</p></div>
      <div class="tile reveal d2"><div class="pub__year">2022</div><p style="margin-top:.6rem">Dedicated diagnostics laboratory commissioned.</p></div>
      <div class="tile reveal d3"><div class="pub__year">2024</div><p style="margin-top:.6rem">40+ publications and growing collaborations.</p></div>
    </div>
  </div>
</section>
{cta_band()}
"""
    page("about.html", "About", "About the Advanced Sensing & Diagnostics Group at CUSAT led by " + SITE['pi'] + ".", "about.html", body)


# =============================================================================
#  PAGE: Research
# =============================================================================
def build_research():
    focus = [
        ("wave", "Structural Health Monitoring", "Vestibulum ante ipsum primis in faucibus. Sensor networks and modal analysis for civil and mechanical structures."),
        ("gauge", "Machinery Fault Diagnosis", "Detecting and localising bearing, gear and rotor faults from vibration and acoustic signatures."),
        ("brain", "Prognostics &amp; RUL", "Data-driven and physics-informed models to estimate remaining useful life of critical components."),
        ("chip", "Smart Sensing Systems", "Low-cost, edge-capable sensor nodes and data-acquisition for field deployment."),
        ("wave", "Signal Processing", "Time-frequency, wavelet and empirical decomposition methods for non-stationary signals."),
        ("shield", "Reliability &amp; Safety", "Reliability modelling and risk assessment for engineered assets and infrastructure."),
    ]
    focus_html = "".join(
        f"""<div class="tile reveal d{i%3+1}"><div class="tile__icon">{IC[ic]}</div><h3>{t}</h3><p>{d}</p></div>"""
        for i,(ic,t,d) in enumerate(focus)
    )

    themes = [
        ("Theme 01", "Vibration-based Condition Monitoring", LOREM),
        ("Theme 02", "AI for Predictive Maintenance", LOREM2),
        ("Theme 03", "Sensor Fusion &amp; IoT", LOREM),
        ("Theme 04", "Digital Twins for Diagnostics", LOREM2),
    ]
    themes_html = ""
    for i,(tag,t,d) in enumerate(themes):
        media = f'<div class="split__media reveal d1"><img src="{img("theme"+str(i),760,570)}" alt="{t}"></div>'
        text = f"""<div class="reveal"><span class="eyebrow">{tag}</span><h2>{t}</h2>
        <p style="margin-top:1rem">{d} {LOREM2}</p>
        <ul style="margin-top:1.2rem;display:grid;gap:.6rem">
          <li style="display:flex;gap:.6rem"><span style="color:var(--red);font-weight:700">—</span> Lorem ipsum dolor sit amet consectetur.</li>
          <li style="display:flex;gap:.6rem"><span style="color:var(--red);font-weight:700">—</span> Sed do eiusmod tempor incididunt.</li>
          <li style="display:flex;gap:.6rem"><span style="color:var(--red);font-weight:700">—</span> Ut labore et dolore magna aliqua.</li>
        </ul></div>"""
        order = (text + media) if i % 2 == 0 else (media + text)
        themes_html += f'<div class="split" style="margin-bottom:clamp(2.5rem,5vw,4rem)">{order}</div>'

    projects = [
        ("Ongoing", "Intelligent Monitoring of Rotating Machinery", "Sponsored · 2023–2026", LOREM),
        ("Ongoing", "Edge-AI Sensor Network for Bridges", "Sponsored · 2024–2027", LOREM2),
        ("Completed", "Wavelet Diagnostics for Gear Systems", "2020–2023", LOREM),
        ("Completed", "Reliability Study of Industrial Pumps", "2019–2022", LOREM2),
    ]
    proj_html = "".join(
        f"""<article class="fcard reveal d{i%3+1}">
        <div class="fcard__media"><span class="fcard__index">{st}</span><img src="{img('proj'+str(i),700,440)}" alt="{t}" loading="lazy"></div>
        <div class="fcard__body"><h3>{t}</h3>
        <p style="font-family:var(--mono);font-size:.78rem;color:var(--red);letter-spacing:.04em">{meta}</p>
        <p style="margin-top:.6rem">{d}</p></div></article>"""
        for i,(st,t,meta,d) in enumerate(projects)
    )

    body = banner("Research",
                  "From the right sensor to the right alarm at the right time — our research covers the full diagnostics pipeline.",
                  "Research", "researchbn") + f"""
<section id="focus" class="section">
  <div class="wrap">
    <div class="section-head reveal"><span class="eyebrow">Focus areas</span>
      <h2>Six areas where we push the boundary</h2>
      <p>Each area combines experimental work on our test rigs with modelling and machine learning.</p></div>
    <div class="grid grid--3">{focus_html}</div>
  </div>
</section>

<section id="themes" class="section section--paper2">
  <div class="wrap">
    <div class="section-head reveal"><span class="eyebrow">Research themes</span><h2>How the pieces fit together</h2></div>
    {themes_html}
  </div>
</section>

<section id="projects" class="section">
  <div class="wrap">
    <div class="section-head reveal" style="display:flex;justify-content:space-between;align-items:end;max-width:none;gap:1rem;flex-wrap:wrap">
      <div><span class="eyebrow">Projects</span><h2>Current &amp; recent projects</h2></div>
      <a class="btn btn--ghost" href="publications.html">See publications {IC['arrow']}</a>
    </div>
    <div class="grid grid--2">{proj_html}</div>
  </div>
</section>
{cta_band()}
"""
    page("research.html", "Research", "Research focus areas, themes and projects of the ASDG group at CUSAT.", "research.html", body)


# =============================================================================
#  PAGE: People
# =============================================================================
def build_people():
    def person(seed, name, role, meta, links=True):
        lk = f"""<div class="person__links">
          <a href="#" aria-label="Email">{IC['mail']}</a>
          <a href="#" aria-label="Scholar">{IC['scholar']}</a>
          <a href="#" aria-label="LinkedIn">{IC['linkedin']}</a></div>""" if links else ""
        return f"""<article class="person reveal">
          <div class="person__photo"><img src="{img(seed,400,400)}" alt="{name}" loading="lazy"></div>
          <div class="person__body"><div class="person__name">{name}</div>
          <div class="person__role">{role}</div><div class="person__meta">{meta}</div>{lk}</div>
        </article>"""

    scholars = "".join(person(f"sch{i}", f"Researcher Name {i+1}", "PhD Scholar", "Lorem ipsum diagnostics") for i in range(8))
    students = "".join(person(f"stu{i}", f"Student Name {i+1}", "M.Tech / Project", "Signal processing") for i in range(4))
    alumni = "".join(person(f"alu{i}", f"Alumnus Name {i+1}", "Alumni · Year", "Now at Lorem Corp", links=False) for i in range(4))

    body = banner("People",
                  "The researchers, students and collaborators who make the group's work possible.",
                  "People", "peoplebn") + f"""
<!-- PI -->
<section id="pi" class="section">
  <div class="wrap">
    <div class="section-head reveal"><span class="eyebrow">Leadership</span><h2>Principal Investigator</h2></div>
    <div class="director reveal">
      <div class="director__photo"><img src="{img('director',400,520)}" alt="{SITE['pi']}"></div>
      <div>
        <div class="director__name">{SITE['pi']}</div>
        <div class="director__title">Principal Investigator · {SITE['dept']}</div>
        <p>{LOREM} {LOREM2}</p>
        <div class="facility__specs" style="margin-top:1.4rem;max-width:520px">
          <div class="facility__spec"><dt>Research</dt><dd>Diagnostics &amp; Sensing</dd></div>
          <div class="facility__spec"><dt>Publications</dt><dd>40+ peer-reviewed</dd></div>
          <div class="facility__spec"><dt>Teaching</dt><dd>Dynamics · Instrumentation</dd></div>
          <div class="facility__spec"><dt>Email</dt><dd style="font-size:.85rem">{SITE['email']}</dd></div>
        </div>
        <div style="margin-top:1.4rem;display:flex;gap:.8rem;flex-wrap:wrap">
          <a class="btn btn--ghost" href="#">{IC['scholar']} Scholar</a>
          <a class="btn btn--ghost" href="#">{IC['gate']} ResearchGate</a>
          <a class="btn btn--ghost" href="mailto:{SITE['email']}">{IC['mail']} Email</a>
        </div>
      </div>
    </div>
  </div>
</section>

<section id="scholars" class="section section--paper2">
  <div class="wrap">
    <div class="section-head reveal"><span class="eyebrow">Research scholars</span><h2>PhD researchers</h2></div>
    <div class="grid grid--4">{scholars}</div>
  </div>
</section>

<section id="students" class="section">
  <div class="wrap">
    <div class="section-head reveal"><span class="eyebrow">Students</span><h2>M.Tech &amp; project students</h2></div>
    <div class="grid grid--4">{students}</div>
  </div>
</section>

<section id="alumni" class="section section--paper2">
  <div class="wrap">
    <div class="section-head reveal"><span class="eyebrow">Alumni</span><h2>Where our graduates are now</h2></div>
    <div class="grid grid--4">{alumni}</div>
  </div>
</section>
{cta_band()}
"""
    page("people.html", "People", "The team behind the ASDG group at CUSAT — principal investigator, scholars, students and alumni.", "people.html", body)


# =============================================================================
#  PAGE: Publications
# =============================================================================
def build_publications():
    data = [
        ("2025", "journal", "Journal", "Lorem ipsum dolor sit amet: a novel approach to bearing fault diagnosis using deep learning",
         "Author A., <b>Prof. Biju N</b>, Author C.", "Mechanical Systems and Signal Processing, Vol. 210", ["Diagnostics","Deep Learning"]),
        ("2025", "conference", "Conference", "Sed do eiusmod: edge-AI sensor fusion for structural health monitoring",
         "Author D., Author E., <b>Prof. Biju N</b>", "Intl. Conf. on Condition Monitoring, pp. 45–52", ["SHM","Sensors"]),
        ("2024", "journal", "Journal", "Ut enim ad minim: prognostics of rotating machinery via physics-informed networks",
         "<b>Prof. Biju N</b>, Author F.", "Journal of Sound and Vibration, Vol. 560", ["Prognostics"]),
        ("2024", "journal", "Journal", "Duis aute irure: wavelet-based feature extraction for gear fault classification",
         "Author G., <b>Prof. Biju N</b>", "Measurement, Vol. 225", ["Signal Processing"]),
        ("2023", "conference", "Conference", "Excepteur sint occaecat: a low-cost DAQ framework for field diagnostics",
         "Author H., <b>Prof. Biju N</b>, Author I.", "IEEE Sensors Conference", ["Sensors","IoT"]),
        ("2023", "journal", "Journal", "Neque porro quisquam: reliability assessment of industrial pumps under variable load",
         "<b>Prof. Biju N</b>, Author J.", "Reliability Engineering &amp; System Safety, Vol. 230", ["Reliability"]),
        ("2022", "conference", "Conference", "Quis autem vel eum: empirical mode decomposition for non-stationary vibration",
         "Author K., <b>Prof. Biju N</b>", "Proc. Vibration Engineering Symposium", ["Signal Processing"]),
        ("2022", "journal", "Journal", "At vero eos: transfer learning for cross-machine fault diagnosis",
         "<b>Prof. Biju N</b>, Author L., Author M.", "Applied Soft Computing, Vol. 120", ["Deep Learning","Diagnostics"]),
    ]
    rows = ""
    for yr, typ, tlabel, title, auth, venue, tags in data:
        tag_html = "".join(f'<span class="pub__tag">{t}</span>' for t in tags)
        rows += f"""<article class="pub reveal" data-type="{typ}">
          <div><div class="pub__year">{yr}</div><span class="pub__type">{tlabel}</span></div>
          <div><h3 class="pub__title">{title}</h3>
          <p class="pub__authors">{auth}</p>
          <p class="pub__venue">{venue}</p>
          <div class="pub__tags">{tag_html}</div></div>
        </article>"""

    body = banner("Publications",
                  "Peer-reviewed journal articles and conference papers from the group. Placeholder entries shown below.",
                  "Publications", "pubbn") + f"""
<section class="section">
  <div class="wrap">
    <div class="pub-filter reveal">
      <button class="active" data-filter="all">All</button>
      <button data-filter="journal">Journal</button>
      <button data-filter="conference">Conference</button>
    </div>
    <div class="pub-list">{rows}</div>
    <div style="margin-top:2.5rem;text-align:center" class="reveal">
      <a class="btn btn--ghost" href="#">{IC['scholar']} Full list on Google Scholar</a>
    </div>
  </div>
</section>
{cta_band()}
"""
    page("publications.html", "Publications", "Journal and conference publications from the ASDG group at CUSAT.", "publications.html", body)


# =============================================================================
#  PAGE: Facilities
# =============================================================================
def build_facilities():
    facs = [
        ("Rotor Dynamics Test Rig", LOREM,
         [("Speed", "0–10,000 rpm"), ("Sensors", "Accelerometers, proximity probes"), ("DAQ", "24-bit, 16-channel"), ("Use", "Rotor &amp; bearing faults")]),
        ("Vibration &amp; Acoustics Lab", LOREM2,
         [("Instruments", "Modal shaker, LDV"), ("Microphones", "Free-field array"), ("Analysis", "Time-frequency suite"), ("Use", "Modal &amp; SHM studies")]),
        ("Smart Sensing &amp; Electronics", LOREM,
         [("Platforms", "Edge MCUs, FPGA"), ("Fabrication", "PCB prototyping"), ("Comms", "Wireless / IoT"), ("Use", "Sensor node design")]),
        ("Computing &amp; ML Cluster", LOREM2,
         [("GPUs", "Multi-GPU workstation"), ("Storage", "High-throughput NAS"), ("Stack", "PyTorch · TensorFlow"), ("Use", "Model training")]),
    ]
    fac_html = ""
    for i,(name, desc, specs) in enumerate(facs):
        spec_html = "".join(f'<div class="facility__spec"><dt>{k}</dt><dd>{v}</dd></div>' for k,v in specs)
        fac_html += f"""<div class="facility reveal">
          <div class="facility__media"><img src="{img('fac'+str(i),760,510)}" alt="{name}"></div>
          <div><span class="eyebrow">Facility {i+1:02d}</span><h2 style="font-size:clamp(1.5rem,3vw,2.1rem)">{name}</h2>
          <p style="margin-top:.8rem">{desc}</p>
          <div class="facility__specs">{spec_html}</div></div>
        </div>"""

    body = banner("Facilities",
                  "Dedicated laboratories and equipment for experimental diagnostics, sensing and computation.",
                  "Facilities", "facbn") + f"""
<section class="section">
  <div class="wrap">
    <div class="section-head reveal"><span class="eyebrow">Infrastructure</span>
      <h2>Where experiments meet computation</h2>
      <p>Our facilities let us take an idea from a bench test to a validated, deployable diagnostic method.</p></div>
    {fac_html}
  </div>
</section>
{cta_band()}
"""
    page("facilities.html", "Facilities", "Laboratory facilities and equipment of the ASDG group at CUSAT.", "facilities.html", body)


# =============================================================================
#  PAGE: News
# =============================================================================
def build_news():
    items = [
        ("news1","Mar 12, 2025","Award","Group paper wins best paper at diagnostics conference", LOREM),
        ("news2","Feb 28, 2025","Grant","New sponsored project on intelligent monitoring begins", LOREM2),
        ("news3","Feb 05, 2025","Publication","Journal article accepted in leading signal-processing venue", LOREM),
        ("news4","Jan 20, 2025","Event","Group hosts workshop on AI for predictive maintenance", LOREM2),
        ("news5","Dec 10, 2024","People","Two scholars complete their PhD defence successfully", LOREM),
        ("news6","Nov 18, 2024","Collaboration","MoU signed with industry partner for field trials", LOREM2),
    ]
    feat = items[0]
    feat_html = f"""<article class="split reveal" style="margin-bottom:clamp(2.5rem,5vw,4rem)">
      <div class="split__media"><img src="{img(feat[0],820,600)}" alt=""></div>
      <div><span class="news-card__date">{feat[1]} · {feat[2]}</span>
      <h2 style="margin-top:.6rem">{feat[3]}</h2>
      <p style="margin-top:1rem">{feat[4]} {LOREM2}</p>
      <div style="margin-top:1.4rem"><a class="btn btn--primary" href="#">Read full story {IC['arrow']}</a></div></div>
    </article>"""

    cards = "".join(
        f"""<article class="news-card reveal d{i%3+1}">
        <div class="news-card__media"><img src="{img(s,600,340)}" alt="" loading="lazy"></div>
        <div class="news-card__body"><span class="news-card__date">{dt} · {cat}</span>
        <h3>{t}</h3><p>{d}</p><a class="fcard__more" href="#">Read more {IC['arrow']}</a></div></article>"""
        for i,(s,dt,cat,t,d) in enumerate(items[1:])
    )

    body = banner("News &amp; Events",
                  "Announcements, awards, publications and events from the group.",
                  "News", "newsbn") + f"""
<section class="section">
  <div class="wrap">
    {feat_html}
    <div class="section-head reveal"><span class="eyebrow">More updates</span><h2>Recent activity</h2></div>
    <div class="grid grid--3">{cards}</div>
  </div>
</section>
{cta_band()}
"""
    page("news.html", "News", "News, awards and events from the ASDG group at CUSAT.", "news.html", body)


# =============================================================================
#  PAGE: Contact
# =============================================================================
def build_contact():
    body = banner("Contact",
                  "Get in touch about research collaborations, student positions or visiting the lab.",
                  "Contact", "contactbn") + f"""
<section class="section">
  <div class="wrap">
    <div class="contact-grid">
      <div class="reveal">
        <span class="eyebrow">Reach us</span>
        <h2>We'd love to hear from you</h2>
        <p style="margin-top:.8rem">{LOREM}</p>
        <div style="margin-top:1.5rem">
          <div class="contact-item"><div class="contact-item__icon">{IC['pin']}</div>
            <div><h4>Address</h4><p>{SITE['addr']}</p></div></div>
          <div class="contact-item"><div class="contact-item__icon">{IC['mail']}</div>
            <div><h4>Email</h4><p><a class="ulink" href="mailto:{SITE['email']}">{SITE['email']}</a></p></div></div>
          <div class="contact-item"><div class="contact-item__icon">{IC['phone']}</div>
            <div><h4>Phone</h4><p>{SITE['phone']}</p></div></div>
          <div class="contact-item"><div class="contact-item__icon">{IC['clock']}</div>
            <div><h4>Office hours</h4><p>Mon–Fri · 9:00 AM – 5:00 PM IST</p></div></div>
        </div>
      </div>

      <div class="reveal d1">
        <form id="contact-form" novalidate>
          <div class="field"><label for="c-name">Name *</label><input id="c-name" name="name" type="text" required placeholder="Your full name"></div>
          <div class="field"><label for="c-email">Email *</label><input id="c-email" name="email" type="email" required placeholder="you@example.com"></div>
          <div class="field"><label for="c-subject">Subject</label>
            <select id="c-subject" name="subject">
              <option>General enquiry</option><option>PhD / M.Tech position</option>
              <option>Research collaboration</option><option>Industry / consultancy</option>
            </select></div>
          <div class="field"><label for="c-msg">Message *</label><textarea id="c-msg" name="message" required placeholder="How can we help?"></textarea></div>
          <button type="submit" class="btn btn--primary">Send message {IC['arrow']}</button>
          <p class="form-note" style="margin-top:1rem;font-family:var(--mono);font-size:.8rem"></p>
        </form>
      </div>
    </div>

    <div class="map-embed reveal" style="margin-top:3rem">
      <iframe title="Map to CUSAT" loading="lazy" referrerpolicy="no-referrer-when-downgrade"
        src="https://www.openstreetmap.org/export/embed.html?bbox=76.31%2C10.03%2C76.36%2C10.06&amp;layer=mapnik&amp;marker=10.046%2C76.329"></iframe>
    </div>
  </div>
</section>
"""
    page("contact.html", "Contact", "Contact the ASDG group at CUSAT for collaborations and positions.", "contact.html", body)


# =============================================================================
if __name__ == "__main__":
    print("Building ASDG site…")
    build_home()
    build_about()
    build_research()
    build_people()
    build_publications()
    build_facilities()
    build_news()
    build_contact()
    print("Done.")
