#!/usr/bin/env python3
"""Generate static portfolio pages for joaquin-ps.github.io."""
import hashlib
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent

EMAIL = "joaquin.palacios@columbia.edu"
LINKEDIN = "https://www.linkedin.com/in/joaquin-b-palacios"
ROAM_LAB = "https://roam.me.columbia.edu/"
MATEI = "https://www.me.columbia.edu/faculty/matei-ciocarlie"

ROAM_LAB_HTML = f'<a href="{ROAM_LAB}" rel="noopener noreferrer">ROAM Lab</a>'
MATEI_HTML = f'<a href="{MATEI}" rel="noopener noreferrer">Matei Ciocarlie</a>'

RESEARCH_LINKS = [
    ("DITTO", "https://roamlab.github.io/ditto/"),
    ("ROAM Hand 3", "/research/roam-hand-3/"),
    ("MyHand-SCI", "/research/myhand-sci/"),
    ("ROAM Hand 1", "/research/roam-hand/"),
]

PORTFOLIO_LINKS = [
    ("Plan Bee", "/portfolio/plan-bee/"),
    ("Crab.io", "/portfolio/crab-io/"),
    ("Button-Pressing Machine", "/portfolio/button-pressing-machine/"),
    ("Applied Robotics", "/portfolio/applied-robotics/"),
    ("Digital Manufacturing", "/portfolio/digital-manufacturing/"),
]


def asset_version(rel: str) -> str:
    """Short content hash so browsers refetch CSS/JS whenever it changes."""
    return hashlib.sha1((ROOT / rel).read_bytes()).hexdigest()[:8]


def nav_href(prefix: str, href: str) -> str:
    if href.startswith("http://") or href.startswith("https://"):
        return href
    return f"{prefix}{href.lstrip('/')}"


def depth_prefix(path: str) -> str:
    # path like "" or "research/roam-hand-3"
    parts = [p for p in path.strip("/").split("/") if p]
    return "../" * len(parts) if parts else "./"


def shell(title: str, path: str, current: str, body: str, description: str = "") -> str:
    prefix = depth_prefix(path)
    desc = description or f"{title} — Joaquin Palacios, robotics engineer and PhD candidate at Columbia University."
    research_items_list = []
    for label, href in RESEARCH_LINKS:
        extra = ' rel="noopener noreferrer"' if href.startswith("http") else ""
        research_items_list.append(f'          <a href="{nav_href(prefix, href)}"{extra}>{label}</a>')
    research_items = "\n".join(research_items_list)
    portfolio_items = "\n".join(
        f'          <a href="{nav_href(prefix, href)}">{label}</a>' for label, href in PORTFOLIO_LINKS
    )

    def cur(name: str) -> str:
        return ' aria-current="page"' if current == name else ""

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <meta name="description" content="{desc}">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,500..800&family=IBM+Plex+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="{prefix}assets/css/styles.css?v={asset_version("assets/css/styles.css")}">
</head>
<body>
  <a class="skip-link" href="#content">Skip to content</a>
  <header class="site-header">
    <div class="nav-wrap">
      <a class="brand" href="{prefix}">Joaquin Palacios</a>
      <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="site-nav">Menu</button>
      <nav class="nav" id="site-nav" aria-label="Primary">
        <a href="{prefix}#publications">Publications</a>
        <details>
          <summary>Research</summary>
          <div class="submenu">
            <a href="{prefix}research/"{cur("research")}>Overview</a>
{research_items}
          </div>
        </details>
        <details>
          <summary>Portfolio</summary>
          <div class="submenu">
            <a href="{prefix}portfolio/"{cur("portfolio")}>Overview</a>
{portfolio_items}
          </div>
        </details>
      </nav>
    </div>
  </header>
  <main id="content">
{body}
  </main>
  <footer class="site-footer">
    <div class="footer-inner">
      <div>
        <a href="{LINKEDIN}" rel="noopener noreferrer">LinkedIn</a>
        <a href="mailto:{EMAIL}">Email</a>
      </div>
      <p>© Joaquin Palacios · Robotics · Columbia University / {ROAM_LAB_HTML}</p>
    </div>
  </footer>
  <script src="{prefix}assets/js/main.js?v={asset_version("assets/js/main.js")}"></script>
</body>
</html>
"""


def write(rel: str, html: str) -> None:
    out = ROOT / rel
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8")
    print("wrote", rel)


def media_tag(src: str, title: str, *, kind: str = "img") -> str:
    """Render image or muted looping video for cards/thumbnails."""
    if src.lower().endswith(".mp4") or src.lower().endswith(".webm"):
        return (
            f'<video class="thumb-video" src="{src}" autoplay muted loop playsinline '
            f'preload="metadata" aria-label="{title}"></video>'
        )
    return f'<img src="{src}" alt="{title}">'


# ---------- pages ----------

def home() -> None:
    ditto = "https://roamlab.github.io/ditto/"
    ditto_blurb = (
        "Co-designed <strong>dexterous hand</strong> and "
        "kinematically equivalent <strong>motorized exoskeleton</strong> for <strong>both</strong> "
        "<em>handheld</em> data collection and <em>bilateral teleoperation</em> "
        "with <strong>joint-level force feedback</strong>."
    )
    featured = [
        (ditto, "media/home/highlight-ditto.mp4", "DITTO", ditto_blurb),
        ("research/roam-hand-3/", "media/home/highlight-roam-hand-3.png", "ROAM Hand 3",
         "Robot hand with 6-axis F/T sensorized fingertips and <strong>novel kinematics validated via RL policies.</strong>"),
        ("research/myhand-sci/", "media/home/highlight-myhand-sci.png", "MyHand SCI",
         "<strong>Wearable robot</strong> to assist grasping for individuals with <strong>Spinal Cord Injuries.</strong>"),
        ("portfolio/plan-bee/", "media/home/highlight-plan-bee.png", "Plan Bee",
         "<strong>Robotic crop pollination</strong> for Vertical Farming."),
    ]
    projects = [
        (ditto, "media/home/highlight-ditto.jpg", "DITTO", ditto_blurb),
        ("research/roam-hand-3/", "media/home/highlight-roam-hand-3.png", "ROAM Hand 3",
         "Robot hand with 6-axis F/T sensorized fingertips and <strong>novel kinematics validated via RL policies.</strong>"),
        ("portfolio/plan-bee/", "media/home/highlight-plan-bee.png", "Plan Bee",
         "<strong>Robotic crop pollination</strong> for Vertical Farming."),
        ("research/myhand-sci/", "media/home/highlight-myhand-sci.png", "MyHand SCI",
         "<strong>Wearable robot</strong> to assist grasping for individuals with <strong>Spinal Cord Injuries.</strong>"),
        ("research/roam-hand/", "media/home/highlight-roam-hand.png", "ROAM Hand 1",
         "Developing a <strong>robot hand</strong> to explore proprioception in <strong>dexterous manipulation.</strong>"),
        ("portfolio/crab-io/", "media/home/highlight-crab-io.png", "Crab.io",
         "A <strong>quadruped robot</strong> known for being cute and fast!"),
        ("portfolio/button-pressing-machine/", "media/home/highlight-button-pressing-machine.png", "Button-Pressing Machine",
         "An exploration of <strong>mechatronics, machine design, controls,</strong> and <strong>machining.</strong>"),
        ("portfolio/digital-manufacturing/", "media/home/highlight-digital-manufacturing.png", "Digital Manufacturing",
         "A collection of projects exploring <strong>generative design, topology optimization, additive manufacturing,</strong> and more."),
        ("portfolio/applied-robotics/", "media/home/highlight-applied-robotics.png", "Applied Robotics",
         "Projects in applied robotics, leveraging <strong>ROS 2</strong> to implement (from scratch) <strong>cartesian control, inverse kinematics, path planning (using RRT algorithm)</strong>, and more.<br>Robots used: <strong>UR5e</strong>, <strong>Franka Emika.</strong>"),
    ]
    feature_slide_parts = []
    for i, (href, media, title, blurb) in enumerate(featured):
        active = " is-active" if i == 0 else ""
        rel = ' rel="noopener noreferrer"' if href.startswith("http") else ""
        cta = "Visit project site →" if href.startswith("http") else "View project →"
        feature_slide_parts.append(
            f'''        <a class="feature-slide{active}" href="{href}" data-index="{i}"{rel}>
          {media_tag(media, title)}
          <div class="feature-copy">
            <h3>{title}</h3>
            <p>{blurb}</p>
            <span class="feature-link">{cta}</span>
          </div>
        </a>'''
        )
    feature_slides = "\n".join(feature_slide_parts)
    feature_dots = "\n".join(
        '          <button type="button" aria-label="Show slide {n}"{cls} data-index="{i}"></button>'.format(
            n=i + 1,
            i=i,
            cls=' class="is-active"' if i == 0 else "",
        )
        for i in range(len(featured))
    )
    project_card_parts = []
    for href, media, title, blurb in projects:
        rel = ' rel="noopener noreferrer"' if href.startswith("http") else ""
        project_card_parts.append(
            f'''      <a class="project-card reveal" href="{href}"{rel}>
        <div class="project-media">
          {media_tag(media, title)}
        </div>
        <h3>{title}</h3>
        <p>{blurb}</p>
      </a>'''
        )
    project_cards = "\n".join(project_card_parts)
    pub_entries = "\n".join(pub_entry(p) for p in PUBLICATIONS)
    body = f"""
    <section class="hero">
      <div class="hero-copy">
        <p class="eyebrow">Robotics · Columbia University · {ROAM_LAB_HTML}</p>
        <h1>Joaquin Palacios</h1>
        <p class="lede">
          Hi there! I'm Joaquin, a Robotics Engineer from <strong>Quito, Ecuador</strong>.
        </p>
        <p class="lede">
          I'm currently a <strong>PhD candidate in Mechanical Engineering</strong> at <strong>Columbia University</strong>. I work at
          the <strong>{ROAM_LAB_HTML}</strong>, advised by <strong>{MATEI_HTML}</strong>.
        </p>
        <p class="lede">
          I am passionate about the full stack of robotics: mechanical design, electronics, controls, and robot learning.
          My research interests are in <strong>autonomous robotic manipulation</strong> and <strong>medical assistive robotics</strong>.
        </p>
        <div class="hero-actions">
          <a class="btn btn-primary" href="research/">Research</a>
          <a class="btn btn-ghost" href="portfolio/">Portfolio</a>
          <a class="btn btn-ghost" href="{LINKEDIN}" rel="noopener noreferrer">LinkedIn</a>
          <a class="btn btn-ghost" href="mailto:{EMAIL}">Email</a>
        </div>
      </div>
      <div class="hero-media">
        <img src="media/home/portrait.jpeg" alt="Portrait of Joaquin Palacios">
      </div>
    </section>

    <section class="section section-highlights">
      <div class="section-head">
        <div>
          <h2>Highlights</h2>
          <p>Featured work in dexterous manipulation, assistive robotics, and agricultural robotics.</p>
        </div>
      </div>
      <div class="feature-carousel-bleed reveal">
        <div class="feature-carousel" data-carousel>
          <div class="feature-viewport">
            <div class="feature-track">
{feature_slides}
            </div>
            <button class="feature-arrow feature-arrow-prev" type="button" data-carousel-prev aria-label="Previous highlight"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M15 5l-7 7 7 7"/></svg></button>
            <button class="feature-arrow feature-arrow-next" type="button" data-carousel-next aria-label="Next highlight"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M9 5l7 7-7 7"/></svg></button>
          </div>
          <div class="feature-nav">
            <div class="feature-dots" data-carousel-dots>
{feature_dots}
            </div>
          </div>
        </div>
      </div>
    </section>

    <section class="section section-publications" id="publications">
      <div class="section-head">
        <div>
          <h2>Publications</h2>
          <p>Dexterous manipulation, tactile sensing, and assistive robotics.</p>
        </div>
      </div>
      <div class="pub-list">
{pub_entries}
      </div>
    </section>

    <section class="section">
      <div class="section-head">
        <div>
          <h2>All Projects</h2>
          <p>Selected research and projects across dexterous manipulation, assistive robotics, and mechatronics.</p>
        </div>
      </div>
      <div class="project-grid">
{project_cards}
      </div>
    </section>

    <section class="section">
      <div class="teaser-row">
        <a class="teaser reveal" href="research/">
          <img class="teaser-thumb" src="media/home/cover-roam-hand.png" alt="">
          <div class="teaser-body">
            <h3>Research</h3>
            <p>ROAM Hand platforms and MyHand-SCI wearable grasping assistance.</p>
            <span>Learn more →</span>
          </div>
        </a>
        <a class="teaser reveal" href="portfolio/">
          <img class="teaser-thumb" src="media/home/cover-crab-io.png" alt="">
          <div class="teaser-body">
            <h3>Projects</h3>
            <p>Plan Bee, Crab.io, applied ROS 2 robotics, and digital manufacturing.</p>
            <span>Learn more →</span>
          </div>
        </a>
      </div>
    </section>
"""
    write("index.html", shell("Joaquin Palacios — Portfolio", "", "home", body,
                              "Portfolio of Joaquin Palacios, robotics PhD candidate at Columbia University ROAM Lab."))


ME = "Joaquin Palacios"

MYHAND_AUTHORS = [f"{ME}*", "Alexandra Deli-Ivanov*", "Ava Chen", "Lauren Winterbottom",
                  "Dawn M. Nilsen", "Joel Stein", MATEI_HTML]

# Newest first. thumb: (kind, src, alt); kind is "img" or "video". hover: optional video shown on hover.
# thumb_pad: add white space above/below diagrams that run edge to edge.
PUBLICATIONS = [
    {
        "title": "DITTO: Dexterous Interface for Transparent TeleOperation",
        "authors": [f"{ME}*", "Katelyn Lee*", "Cheng Zhang", "Zhanpeng He", MATEI_HTML],
        "note": "*joint first authorship",
        "venue": "arXiv preprint, 2026",
        "links": [("Project Page", "https://roamlab.github.io/ditto/"),
                  ("arXiv", "https://arxiv.org/abs/2609.19196")],
        "thumb": ("video", "media/home/highlight-ditto.mp4", "DITTO dexterous hand and motorized exoskeleton"),
    },
    {
        "title": "SpikeATac: A Multimodal Tactile Finger with Taxelized Dynamic Sensing for Dexterous Manipulation",
        "authors": ["Eric T. Chang*", "Peter Ballentine*", "Zhanpeng He*", "Do-Gon Kim", "Kai Jiang",
                    "Hua-Hsuan Liang", ME, "William Wang", "Pedro Piacenza", "Ioannis Kymissis", MATEI_HTML],
        "note": "*joint first authorship",
        "venue": "IEEE International Conference on Robotics and Automation (ICRA), 2026",
        "links": [("Project Page", "https://roamlab.github.io/spikeatac/"),
                  ("arXiv", "https://arxiv.org/abs/2510.27048"),
                  ("WSJ Coverage", "https://www.wsj.com/tech/the-hands-problem-holding-back-the-humanoid-revolution-c1aa6123")],
        "thumb": ("video", "spikeatac.mp4", "SpikeATac tactile finger"),
        "hover": "spikeatac-hover.mp4",
    },
    {
        "title": "Reciprocal Learning of Intent Inferral with Augmented Visual Feedback for Stroke",
        "authors": ["Jingxi Xu*", "Ava Chen*", "Lauren Winterbottom", ME, "Preethika Chivukula",
                    "Dawn M. Nilsen", "Joel Stein", MATEI_HTML],
        "note": "*equal contribution",
        "venue": "IEEE International Conference on Rehabilitation Robotics (ICORR), 2025",
        "links": [("arXiv", "https://arxiv.org/abs/2412.07956"),
                  ("Poster (PDF)", "media/publications/icorr-2025-poster.pdf")],
        "thumb": ("img", "reciprocal-learning.jpg",
                  "Reciprocal learning loop: EMG data feeds an intent classifier whose predictions are shown to the user on LED progress bars"),
        "thumb_pad": True,
    },
    {
        "title": "Train Robots in a JIF: Joint Inverse and Forward Dynamics with Human and Robot Demonstrations",
        "authors": ["Gagan Khandate*", "Boxuan Wang*", "Sarah Park*", "Weizhe Ni", ME, "Kathryn Lampo",
                    "Philippe Wu", "Rosh Ho", "Eric Chang", MATEI_HTML],
        "note": "*joint first authorship",
        "venue": "arXiv preprint, 2025",
        "links": [("arXiv", "https://arxiv.org/abs/2503.12297")],
        "thumb": ("img", "jif-demos.gif", "Human and robot manipulation demonstrations"),
        "thumb_pad": True,
    },
    {
        "title": "Grasp Force Assistance via Throttle-based Wrist Angle Control on a Robotic Hand Orthosis for C6–C7 Spinal Cord Injury",
        "authors": MYHAND_AUTHORS,
        "note": "*equal contribution",
        "venue": "IEEE Transactions on Medical Robotics and Bionics (T-MRB), 2024",
        "links": [("Paper", "https://pubmed.ncbi.nlm.nih.gov/40041101/"),
                  ("Project Page", "research/myhand-sci/")],
        "thumb": ("img", "myhand-sci-device.png", "MyHand-SCI device and grasp/maintain/release control diagram"),
    },
    {
        "title": "Towards Tenodesis-Modulated Control of an Assistive Hand Exoskeleton for SCI",
        "authors": MYHAND_AUTHORS,
        "note": "*equal contribution",
        "venue": "IROS 2023 Workshop on Assistive Robots for Citizens",
        "links": [("Paper (PDF)", "media/publications/iros-2023-workshop-paper.pdf"),
                  ("Poster (PDF)", "media/publications/iros-2023-poster.pdf")],
        "thumb": ("img", "myhand-sci-figure.jpg", "MyHand-SCI assisting a grasp of a small can"),
    },
]


def pub_media(kind: str, src: str, alt: str = "", cls: str = "") -> str:
    # Bare filenames live in media/publications/; paths with a folder are used as-is.
    path = src if "/" in src else f"media/publications/{src}"
    c = f' class="{cls}"' if cls else ""
    if kind == "video":
        label = f' aria-label="{alt}"' if alt else ' aria-hidden="true"'
        return f'<video{c} src="{path}" muted autoplay loop playsinline{label}></video>'
    return f'<img{c} src="{path}" alt="{alt}" loading="lazy">'


def pub_entry(pub: dict) -> str:
    authors = ",\n            ".join(
        f"<strong>{a}</strong>" if a.rstrip("*") == ME else a for a in pub["authors"]
    )
    links = " <span aria-hidden=\"true\">|</span>\n            ".join(
        f'<a href="{href}"' + (' rel="noopener noreferrer"' if href.startswith("http") else "") + f">{label}</a>"
        for label, href in pub["links"]
    )
    thumb = pub_media(*pub["thumb"])
    hover_cls = " pub-thumb--padded" if pub.get("thumb_pad") else ""
    if pub.get("hover"):
        thumb += "\n          " + pub_media("video", pub["hover"], cls="pub-thumb-hover")
        hover_cls += " has-hover"
    note = f'\n          <p class="pub-note">{pub["note"]}</p>' if pub.get("note") else ""
    return f"""      <article class="pub reveal">
        <figure class="pub-thumb{hover_cls}">
          {thumb}
        </figure>
        <div class="pub-body">
          <h3 class="pub-title">{pub["title"]}</h3>
          <p class="authors">
            {authors}
          </p>{note}
          <p class="venue">{pub["venue"]}</p>
          <p class="pub-links">
            {links}
          </p>
        </div>
      </article>"""


def publications_redirect() -> None:
    # Publications now live on the home page; keep old /publications/ links working.
    write("publications/index.html", """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Publications — Joaquin Palacios</title>
  <link rel="canonical" href="../#publications">
  <meta http-equiv="refresh" content="0; url=../#publications">
</head>
<body>
  <p>Publications have moved to the <a href="../#publications">home page</a>.</p>
</body>
</html>
""")


def overview_media(src: str, alt: str) -> str:
    if src.endswith(".mp4"):
        return f'<video src="{src}" autoplay muted loop playsinline preload="metadata" aria-label="{alt}"></video>'
    return f'<img src="{src}" alt="{alt}" loading="lazy">'


def research_index() -> None:
    # (href, media, title, years, summary, role); role may be empty.
    items = [
        ("https://roamlab.github.io/ditto/", "../media/research/ditto.mp4", "DITTO", "2025–",
         "Co-designed <strong>dexterous hand</strong> and kinematically equivalent <strong>motorized exoskeleton</strong> "
         "for <strong>both</strong> <em>handheld</em> data collection and <em>bilateral teleoperation</em> "
         "with <strong>joint-level force feedback</strong>.", ""),
        ("roam-hand-3/", "../media/home/highlight-roam-hand-3.png", "ROAM Hand 3", "2024–2025",
         "Robot hand with 6-axis F/T sensorized fingertips and <strong>novel kinematics validated via RL policies</strong>.",
         "Mechanical design and kinematic validation via reinforcement learning."),
        ("myhand-sci/", "../media/research/myhand-sci.png", "MyHand-SCI", "2022–2023",
         "Creating a <strong>wearable robot</strong> to assist in grasping for individuals with <strong>Spinal Cord Injuries</strong>.",
         "A study on <em>tenodesis</em>-based user control for grasping force modulation, promoting the development of intuitive assistive devices."),
        ("roam-hand/", "../media/research/roam-hand.png", "ROAM Hand 1", "2023",
         "Designing and building a robot hand to explore <em>proprioception</em> in dexterous robot manipulation.",
         "Mechanical design and firmware implementation for torque control of a tendon-driven robot hand."),
    ]
    cards = []
    for href, media, title, years, summary, role in items:
        rel = ' rel="noopener noreferrer"' if href.startswith("http") else ""
        role_html = f"\n          <p>{role}</p>" if role else ""
        cards.append(f'''      <article class="research-card reveal">
        <a class="research-media" href="{href}"{rel} tabindex="-1" aria-hidden="true">
          {overview_media(media, title)}
        </a>
        <div class="research-copy">
          <p class="overview-year">{years}</p>
          <h2><a href="{href}"{rel}>{title}</a></h2>
          <p>{summary}</p>{role_html}
        </div>
      </article>''')
    body = f"""
    <header class="page-hero">
      <p class="crumb"><a href="../">Home</a> / Research</p>
      <h1>Research</h1>
      <p class="tagline">Hardware and controls research in dexterous manipulation and assistive robotics at {ROAM_LAB_HTML}.</p>
    </header>
    <div class="research-grid">
{chr(10).join(cards)}
    </div>
"""
    write("research/index.html", shell("Research — Joaquin Palacios", "research", "research", body))


def portfolio_index() -> None:
    items = [
        ("plan-bee/", "../media/home/highlight-plan-bee.png", "Plan Bee", "2023",
         "Developing a robot to automate <strong>crop pollination</strong> in vertical farms."),
        ("crab-io/", "../media/home/highlight-crab-io.png", "Crab.io", "2022",
         "A <strong>quadruped robot</strong> known for being cute and being fast!"),
        ("button-pressing-machine/", "../media/home/highlight-button-pressing-machine.png", "Button-Pressing Machine", "2022",
         "An exploration of <strong>mechatronics, machine design, controls,</strong> and <strong>machining</strong>."),
        ("applied-robotics/", "../media/home/highlight-applied-robotics.png", "Applied Robotics", "2023",
         "Projects in applied robotics, leveraging <strong>ROS 2</strong> to implement from scratch cartesian control, "
         "inverse kinematics, and path planning (RRT).<br>Robots used: <strong>UR5e</strong>, <strong>Franka Emika</strong>."),
        ("digital-manufacturing/", "../media/home/highlight-digital-manufacturing.png", "Digital Manufacturing", "2022–2023",
         "A collection of projects exploring <strong>generative design, topology optimization, additive manufacturing,</strong> and more."),
    ]
    rows = "\n".join(
        f'''      <article class="showcase-row reveal">
        <a class="showcase-media" href="{href}" tabindex="-1" aria-hidden="true">
          {overview_media(img, title)}
        </a>
        <div class="showcase-copy">
          <p class="overview-year">{year}</p>
          <h2><a href="{href}">{title}</a></h2>
          <p>{blurb}</p>
          <a class="overview-link" href="{href}">View project →</a>
        </div>
      </article>'''
        for href, img, title, year, blurb in items
    )
    body = f"""
    <header class="page-hero">
      <p class="crumb"><a href="../">Home</a> / Portfolio</p>
      <h1>Portfolio</h1>
      <p class="tagline">Course and personal projects spanning agricultural robotics, locomotion, mechatronics, and digital manufacturing.</p>
    </header>
    <div class="showcase">
{rows}
    </div>
"""
    write("portfolio/index.html", shell("Portfolio — Joaquin Palacios", "portfolio", "portfolio", body))


# ---------- project pages ----------
# Layout mirrors joaquinpalacios.com: hero media, an intro (lead + description beside a
# details column), then sections that interleave text and media.

def ext(href: str, label: str) -> str:
    return f'<a href="{href}" rel="noopener noreferrer">{label}</a>'


def img(src: str, alt: str = "") -> str:
    return f'<img src="{src}" alt="{alt}" loading="lazy">'


def vid(src: str, label: str = "") -> str:
    aria = f' aria-label="{label}"' if label else ""
    return f'<video src="{src}" controls playsinline preload="metadata"{aria}></video>'


def youtube(video_id: str, title: str) -> str:
    return (
        f'<iframe class="pp-embed" src="https://www.youtube-nocookie.com/embed/{video_id}" title="{title}" '
        'loading="lazy" referrerpolicy="strict-origin-when-cross-origin" '
        'allow="accelerometer; encrypted-media; gyroscope; picture-in-picture; fullscreen" '
        'allowfullscreen></iframe>'
    )


def fig(media: str, caption: str = "", size: str = "") -> str:
    cls = f"pp-fig pp-{size}" if size else "pp-fig"
    cap = f"\n          <figcaption>{caption}</figcaption>" if caption else ""
    return f'''        <figure class="{cls}">
          {media}{cap}
        </figure>'''


def h2(text: str, center: bool = True, level: int = 2) -> str:
    cls = "pp-h2 center" if center else "pp-h2"
    if level == 3:
        cls += " pp-h3"
    return f"        <h{level} class=\"{cls}\">{text}</h{level}>"


def text(html: str, center: bool = False) -> str:
    cls = "pp-text center" if center else "pp-text"
    return f'        <div class="{cls}">\n{html}\n        </div>'


def split(text_html: str, media_html: str, media_left: bool = False) -> str:
    cls = "pp-split media-left" if media_left else "pp-split"
    return f'''        <div class="{cls}">
          <div class="pp-text">
{text_html}
          </div>
          <div class="pp-split-media">
{media_html}
          </div>
        </div>'''


def grid(items: list[str], cols: int = 2) -> str:
    return f'        <div class="pp-grid" style="--cols:{cols}">\n' + "\n".join(items) + "\n        </div>"


def section(*blocks: str) -> str:
    return '      <section class="pp-section reveal">\n' + "\n".join(blocks) + "\n      </section>"


def meta_list(items: list[tuple[str, object]]) -> str:
    rows = []
    for label, value in items:
        if label == "Collaborators":
            # Keep each name on one line so the list wraps between names, not inside them.
            names = [n for n in re.split(r",\s*(?:and\s+)?|\s+and\s+", str(value)) if n]
            spans = [f'<span class="pp-name">{n}</span>' for n in names]
            dd = ", ".join(spans[:-1]) + (", and " if len(spans) > 2 else " and ") + spans[-1] if len(spans) > 1 else spans[0]
            rows.append(f'        <div><dt>{label}:</dt><dd>{dd}</dd></div>')
            continue
        vals = value if isinstance(value, list) else [value]
        dd = "".join(f"<span>{v}</span>" for v in vals)
        rows.append(f"        <div><dt>{label}:</dt><dd>{dd}</dd></div>")
    return '      <dl class="pp-meta">\n' + "\n".join(rows) + "\n      </dl>"


def project_page(
    rel_dir: str,
    current: str,
    title: str,
    crumb_parent: tuple[str, str],
    summary: str,
    *,
    lead: str,
    description: list[str],
    meta: list[tuple[str, object]] | None = None,
    hero: str = "",
    body: list[str] | None = None,
) -> None:
    parent_label, parent_href = crumb_parent
    prefix = depth_prefix(rel_dir)
    hero_html = f'\n    <div class="pp-hero reveal">\n      {hero}\n    </div>' if hero else ""
    desc_label = '\n        <p class="pp-label">Description:</p>' if meta else ""
    desc = "\n".join(f"        <p>{p}</p>" for p in description)
    meta_html = "\n" + meta_list(meta) if meta else ""
    intro_cls = "pp-intro" if meta else "pp-intro no-meta"
    sections = "\n".join(body or [])
    page = f"""
    <header class="page-hero">
      <p class="crumb"><a href="{prefix}">Home</a> / <a href="{prefix}{parent_href}">{parent_label}</a> / {title}</p>
      <h1>{title}</h1>
    </header>{hero_html}
    <div class="{intro_cls} reveal">
      <div class="pp-intro-copy">
        <p class="pp-lead">{lead}</p>{desc_label}
{desc}
      </div>{meta_html}
    </div>
    <div class="pp-body">
{sections}
    </div>
"""
    write(f"{rel_dir}/index.html", shell(f"{title} — Joaquin Palacios", rel_dir, current, page, summary))


def all_projects() -> None:
    m = lambda folder, name: f"../../media/{folder}/{name}"

    # ---- Research ----
    rh3 = lambda name: m("roam-hand-3", name)
    project_page(
        "research/roam-hand-3", "research", "ROAM Hand 3", ("Research", "research/"),
        "Robot hand with 6-axis F/T sensorized fingertips and novel kinematics validated via RL policies.",
        hero=img(rh3("ur5e-rubiks-cube.png"), "ROAM Hand 3 on a UR5e arm holding a Rubik's cube"),
        lead="Robot hand with 6-axis F/T sensorized fingertips and <strong>novel kinematics validated via RL policies.</strong>",
        description=[
            "Iterative design cycle with robot learning in-the-loop to develop a novel dexterous robot hand. "
            "Validating kinematics by training dexterous in-hand manipulation skills via Reinforcement Learning.",
            "6 Axis Force/Torque sensorized fingertip development is being led by collaborators Amr El-Azizi, Sharfin Islam, and Pedro Piacenza.",
            "<strong>As seen in:</strong> " + ext("https://www.wsj.com/tech/the-hands-problem-holding-back-the-humanoid-revolution-c1aa6123", "Wall Street Journal (2025)"),
        ],
        meta=[
            ("Research Area", "Autonomous Robotic Manipulation"),
            ("Technical Contribution", "Mechanical Design, Kinematic Validation via RL Policies"),
            ("Years", "2024 – 2025"),
            ("Collaborators", f"Eugene Sohn, Veronika Zam, Amr El-Azizi, Sharfin Islam, Dongxiao Yang, Eric Chang, Zhanpeng He, Pedro Piacenza, and {MATEI_HTML}"),
        ],
        body=[
            section(
                h2("Anthropomorphic Hand (RH3-A)"),
                fig(vid(rh3("in-hand-manipulation.mp4"), "RH3-A in-hand manipulation policy in simulation"), size="medium"),
                grid([
                    fig(img(rh3("rh3-top-view.png"), "RH3-A top view")),
                    fig(img(rh3("rh3-anthropomorphic.png"), "RH3-A front view")),
                ]),
                fig(img(rh3("ur5e-tennis-ball.png"), "RH3-A on a UR5e holding a tennis racket"), size="narrow"),
            ),
            section(
                h2("Non-Anthropomorphic Hand (RH3-NA)"),
                fig(vid(rh3("lug-nut-manipulation.mp4"), "RH3-NA hardware manipulating a block"), size="medium"),
                fig(vid(rh3("rh3-na-demo.mp4"), "RH3-NA manipulation policy in simulation"), size="medium"),
                grid([
                    fig(img(rh3("rh3-na-spread.png"), "RH3-NA with fingers spread")),
                    fig(img(rh3("rh3-na-with-block.png"), "RH3-NA grasping a red block")),
                ]),
                fig(vid(rh3("hardware-demo.mp4"), "Running RH3-NA experiments at the lab"), size="medium"),
            ),
        ],
    )

    project_page(
        "research/myhand-sci", "research", "MyHand-SCI", ("Research", "research/"),
        "A wearable robot that provides active grasping assistance for individuals with spinal cord injuries (SCI).",
        hero=youtube("SEi8ZkJe4dQ", "MyHand SCI – A Robotic Hand Orthosis for Spinal Cord Injury"),
        lead="A <strong>wearable robot</strong> that provides <strong>active grasping assistance</strong> for individuals with Spinal Cord Injuries (SCI).",
        description=[
            "For the MyHand-SCI we adopted a philosophy of augmenting, rather than overshadowing, an individual’s residual motor skills. "
            "The MyHand-SCI aims to leverage the " + ext("https://en.wikipedia.org/wiki/Tenodesis_grasp", "tenodesis grasp")
            + ", a compensatory grasping pattern utilized by individuals with C5–C6 injuries, as a user control modality.",
            "We believe this can make the device more intuitive for this population, give the user more agency and direct feedback, "
            "and thus encourage user adoption.",
        ],
        meta=[
            ("Research Area", "Assistive Robotics"),
            ("Technical Contribution", "Mechanical Design, Firmware Implementation, Experiment Design"),
            ("Years", "2022 – 2023"),
            ("Collaborators", f"Alexandra Deli-Ivanov, Ava Chen, Lauren Winterbottom, Dawn M. Nilsen, Joel Stein, and {MATEI_HTML}"),
        ],
        body=[
            section(split(
                h2("Publications", center=False) + """
            <p>""" + ext("https://arxiv.org/abs/2402.08020", "Journal paper") + """, T-MRB [Nov, 2024]</p>
            <p><a href="../../#publications">Workshop abstract</a>, <strong>IROS 2023!</strong></p>
            <ul>
              <li>I gave a spotlight presentation and poster presentation at the <em>Assistive Robots for Citizens Workshop</em> at <em>IROS 2023</em>.</li>
            </ul>""",
                fig(img(m("myhand-sci", "device.png"), "MyHand-SCI device with grasp, maintain, and release control modes")),
                media_left=True,
            )),
        ],
    )

    rh1 = lambda name: m("roam-hand", name)
    project_page(
        "research/roam-hand", "research", "ROAM Hand 1", ("Research", "research/"),
        "A tendon-driven robot hand exploring proprioception in dexterous manipulation.",
        hero=vid(rh1("hardware-demo.mp4"), "ROAM Hand hardware demo"),
        lead="A tendon-driven robot hand, exploring <em>proprioception</em> in <strong>dexterous manipulation.</strong>",
        description=[
            "The ROAM Hand was developed as a hardware testbed to explore how <em>proprioception</em> can augment other sensing modalities, like "
            + ext("https://roam.me.columbia.edu/research-projects/tactile-sensing", "tactile sensing")
            + " and computer vision, in an effort to achieve dexterous manipulation.",
            "The fingers are driven by tendons connected to servos inside the palm, with a load cell measuring the reaction torque of each motor, "
            "allowing us to sense the torque at each joint. This is robotic <em>proprioception</em>.",
        ],
        meta=[
            ("Research Area", "Robotic Manipulation"),
            ("Technical Contributions", ["Mechanical Design", "Firmware Implementation"]),
            ("Year", "2023"),
        ],
        body=[
            section(split(
                h2("My Role", center=False) + """
            <p>Redesign of tendon routing and pulley transmission to reduce friction and improve torque sensing. A key challenge I had to overcome was routing tendons in such a way each joint remains uncoupled.</p>
            <p>Implementing firmware for position control and torque sensing. Integrating with ROS architecture.</p>""",
                fig(img(rh1("tendon-routing.png"), "Tendon routing diagrams a–d")),
            )),
            section(
                h2("Gallery", center=False),
                '        <div class="pp-grid pp-grid-2-1">\n'
                + fig(img(rh1("joint-pulleys.jpg"), "Tendon routing for proximal and distal links"), "Tendon routing for proximal and distal links.") + "\n"
                + fig(img(rh1("render.png"), "Render of ROAM Hand"), "Render of ROAM Hand.") + "\n        </div>",
                grid([
                    '        <div class="pp-stack">\n'
                    + fig(img(rh1("manufacturing-detail.png"), "Joint pulley diagrams"),
                          "<strong>Joint Pulleys:</strong> The distal tendon has to run exactly through the center of the proximal joint or else it creates joint coupling. "
                          "To accomplish this, I placed the proximal tendon off the central axis, and added a second tendon to balance out the moments.") + "\n"
                    + fig(img(rh1("roll-joint.jpg"), "3D-printed finger components"),
                          "<strong>Manufacturing:</strong> 3D printing using FDM and SLA printers. Pulleys and teflon tubing added in critical friction locations.")
                    + "\n        </div>",
                    '        <div class="pp-stack">\n'
                    + fig(img(rh1("finger-motion-b.gif"), "Finger roll joint rotating"),
                          "<strong>Roll Joint:</strong> To allow the finger to rotate about the base without affecting the proximal and distal tendons, "
                          "a «floating piece» sandwiched between bearings routes the tendons.") + "\n"
                    + fig(img(rh1("finger-motion-a.gif"), "Finger roll joint, front view"))
                    + "\n        </div>",
                ]),
            ),
        ],
    )

    # ---- Portfolio ----
    pb = lambda name: m("plan-bee", name)
    project_page(
        "portfolio/plan-bee", "portfolio", "Plan Bee", ("Portfolio", "portfolio/"),
        "An agricultural robot for pollination in enclosed vertical farms.",
        hero=vid(pb("demo-broll.mp4"), "Plan Bee demo"),
        lead="An <strong>agricultural robot</strong> intended to increase the diversity of crop production in vertical farms by enabling pollination in enclosed environments.",
        description=[
            "Plan Bee is a five degree of freedom robot with on-board computer vision and a rotating brush end-effector. "
            "Plan Bee successfully identifies flowers within its workplace and pollinates them without the need for humans or live bees. "
            "It leverages an image segmentation neural network and a depth perception camera to identify flowers, determine their location, "
            "and automatically plan and deploy pollen transfer routines.",
            "<strong>Awards:</strong> 1st Place Winners at Columbia Engineering 2023 Senior Design Expo!",
        ],
        meta=[
            ("Research Area", "Agricultural Robotics"),
            ("Technical Contribution", ["Mechatronics Design", "Software (Firmware, Path Planning, Computer Vision, &amp; more)"]),
            ("Year", "2023"),
            ("Collaborators", "Valentina Gonzalez, Siddhanth Lath, Georgios Thomakos, and Aiman Najah"),
        ],
        body=[
            section(split(
                h2("The Problem", center=False) + """
            <p>Vertical farming presents a sustainable, resource-efficient alternative to conventional agricultural practices, but growing crops in an enclosed environment removes access to natural pollinators such as insects and wind.</p>
            <p>Many fruits and vegetables that are staples of our diets require pollination to grow, thus the absence of pollinators limits the variety of crops vertical farming can produce.</p>""",
                fig(img(pb("vertical-farm.webp"), "Rows of crops in a vertical farm")),
            )),
            section(
                h2("Our Solution"),
                fig(vid(pb("pollination-routine.mp4"), "Plan Bee pollination routine"), "Pollination Routine (x2 speed)"),
            ),
            section(
                h2("Personal Contributions"),
                h2("Software", level=3),
                text("          <p>As the software developer for this project, my responsibilities included:</p>", center=True),
                grid([
                    fig(img(pb("system-view.png"), "Flower detections on the plant"),
                        "<strong>Machine Learning:</strong> Implementing and training flower detection model."),
                    fig(img(pb("end-effector.png"), "Depth camera view with flower coordinates"),
                        "<strong>Computer Vision:</strong> Interfacing with the depth perception camera to extract flower locations."),
                    fig(img(pb("workspace.png"), "3D plot of the planned path"),
                        "<strong>Robotics Planning:</strong> Writing software for kinematic analysis, cartesian control, and path planning."),
                ], cols=3),
            ),
            section(split(
                h2("Electronics &amp; Firmware", center=False, level=3) + """
            <p>I was also in charge of the electronics and firmware for the system, including:</p>
            <ul>
              <li>Embedded firmware for lower-level motor control (Arduino).</li>
              <li>Selecting motors and motor drivers (actuation scheme consisting of a mix of stepper motors and servos).</li>
              <li>Electronics design and wire management.</li>
            </ul>""",
                fig(img(pb("full-system.png"), "Plan Bee robot with its electronics box")),
                media_left=True,
            )),
            section(split(
                h2("Hardware", center=False, level=3) + """
            <p>I also contributed to the hardware, including:</p>
            <ul>
              <li>Selecting robot kinematics suited for this task (gantry based, 5 DOF leveraging flowers’ axial symmetry).</li>
              <li>Designing and modelling lead screw actuators.</li>
              <li>Creating CAD for multiple components.</li>
              <li>Manufacturing and assembly.</li>
            </ul>""",
                fig(img(pb("cad-design.png"), "CAD of a large-scale Plan Bee over a grow bed"),
                    "In real application, we envision a large scale version of our robot."),
            )),
            section(
                h2("Our Team"),
                fig(img(pb("team-at-expo.jpg"), "The Plan Bee team at the Senior Design Expo"), size="medium"),
            ),
        ],
    )

    cb = lambda name: m("crab-io", name)
    project_page(
        "portfolio/crab-io", "portfolio", "Crab.io", ("Portfolio", "portfolio/"),
        "A quadruped robot known for being cute and fast.",
        hero=vid(cb("walking-demo.mp4"), "Crab.io walking"),
        lead="A <strong>quadruped robot</strong> known for being cute and being fast!",
        description=[
            "As part of the Robotics Studio course at Columbia University, my partner Valentina Gonzalez and I designed and built this unique walking robot.",
        ],
        meta=[
            ("Area", "Robotic Locomotion"),
            ("Technical Contribution", ["Mechatronics Design", "Software (Firmware Implementation)"]),
            ("Year", "2022"),
        ],
        body=[
            section(split(
                h2("Topology Optimization", center=False) + """
            <p>To go fast, crab.io had to be light, and topology optimization allowed us to keep the robot lightweight!</p>""",
                fig(img(cb("topology-optimized-leg.jpg"), "Topology-optimized leg")),
            )),
            section(
                h2("Gallery"),
                '        <div class="pp-stack pp-narrow">\n'
                + fig(img(cb("render.png"), "Crab.io render")) + "\n"
                + fig(vid(cb("locomotion-demo.mp4"), "Crab.io locomotion demo")) + "\n"
                + fig(img(cb("gait.png"), "Gait diagram")) + "\n        </div>",
            ),
        ],
    )

    project_page(
        "portfolio/button-pressing-machine", "portfolio", "Button-Pressing Machine", ("Portfolio", "portfolio/"),
        "An exploration of mechatronics, machine design, controls, and machining.",
        hero=vid(m("button-pressing-machine", "machine-in-action.mp4"), "Button-pressing machine in action"),
        lead="An exploration of <strong>mechatronics, machine design, controls,</strong> and <strong>machining.</strong>",
        description=[
            "In an arcade-style button pressing game, this device uses a four bar linkage equipped with a solenoid to press buttons as fast as possible. "
            "A PID controller makes it rapidly move between the different buttons.",
            "I was responsible for coding the <strong>Arduino firmware</strong> and <strong>tuning the controller gains.</strong> "
            "I also <strong>designed the four bar linkage</strong>, ensuring a trajectory that reached all required positions, "
            "and helped in manufacturing the aluminum links, which involved <strong>waterjet cutting and CNC milling.</strong>",
        ],
        meta=[
            ("Research Area", "Mechatronics"),
            ("Technical Contribution", "Mechanical Design and Firmware Implementation"),
            ("Year", "2022"),
            ("Collaborators", "Valentina Gonzalez, Siddhanth Lath, Georgios Thomakos, and Aiman Najah"),
        ],
        body=[
            section(grid([
                fig(img(m("button-pressing-machine", "mechanism-closeup.png"), "Four-bar linkage mechanism render")),
                fig(img(m("button-pressing-machine", "full-machine.jpg"), "Machined button-pressing machine")),
            ])),
        ],
    )

    ar = lambda name: m("applied-robotics", name)
    project_page(
        "portfolio/applied-robotics", "portfolio", "Applied Robotics", ("Portfolio", "portfolio/"),
        "ROS 2 projects implementing cartesian control, inverse kinematics, and RRT path planning from scratch.",
        lead="Projects in applied robotics, leveraging <strong>ROS 2</strong> to implement from scratch "
             "<strong>cartesian control, inverse kinematics, path planning (using RRT algorithm)</strong>, and more.",
        description=[
            "Robots used: " + ext("https://www.universal-robots.com/products/ur5-robot/", "UR5e") + ", "
            + ext("https://www.franka.de/production", "Franka Emika") + ".",
        ],
        body=[
            section(
                h2("Cartesian Control"),
                grid([
                    fig(vid(ar("ur5e-cartesian-control.mp4"), "Cartesian control on UR5e"),
                        "Cartesian Control on UR5e. End effector pose can be controlled along one degree of freedom, without influencing the rest."
                        "<br><br>Can handle singularities by using the pseudoinverse of the jacobian."),
                    fig(vid(ar("franka-cartesian-control.mp4"), "Cartesian control on Franka Emika"),
                        "Cartesian Control on Franka Emika."
                        "<br><br>As a redundant robot (7 joints for 6 DOF), one of the joints can be moved without influencing the end-effector pose "
                        "(by moving in the nullspace of the jacobian)."),
                ]),
            ),
            section(
                h2("Numerical Inverse Kinematics"),
                fig(vid(ar("inverse-kinematics.mp4"), "Numerical inverse kinematics"), size="medium"),
            ),
            section(
                h2("Path Planning Using RRT (2D Demonstration)"),
                fig(vid(ar("teleop-screencast.mp4"), "2D RRT path planning demonstration"), size="medium"),
            ),
            section(
                h2("Path Planning Using RRT on UR5e"),
                grid([
                    fig(vid(ar("rrt-no-obstacles.mp4"), "RRT on UR5e without obstacles")),
                    fig(vid(ar("rrt-simple-obstacle.mp4"), "RRT on UR5e with a simple obstacle")),
                ]),
                fig(vid(ar("rrt-hard-obstacle.mp4"), "RRT on UR5e with a hard obstacle"), size="medium"),
            ),
        ],
    )

    dm = lambda name: m("digital-manufacturing", name)
    project_page(
        "portfolio/digital-manufacturing", "portfolio", "Digital Manufacturing", ("Portfolio", "portfolio/"),
        "Projects exploring generative design, topology optimization, additive manufacturing, and more.",
        lead="A collection of projects exploring <strong>generative design, topology optimization, additive manufacturing</strong>, and more.",
        description=["Leveraging modern software and manufacturing to create art and produce novel designs."],
        body=[
            section(split(
                h2("Topology Optimization", center=False, level=3) + """
            <p>Designed a lightweight robotic arm using """ + ext("https://altair.com/inspire", "<strong>Altair Inspire</strong>")
                + """ as an educational model to showcase how to perform <strong>Topology Optimization</strong> to improve mechanical designs.</p>""",
                fig(img(dm("topology-optimized-arm.png"), "Topology-optimized robotic arm")),
            )),
            section(
                h2("Generative Design"),
                text("          <p>Using code to generate designs for laser cutting, computerized embroidery, and additive food printing.</p>", center=True),
                split(
                    h2("Auto-Generated Fractal Puzzles", center=False, level=3) + """
            <p>Created a <strong>MATLAB</strong> script that takes in user inputs (dimensions, design parameters, size of stock) and outputs an <strong>SVG file</strong> encoding the instructions to laser cut a jigsaw puzzle.</p>
            <p>A selection of fractals can be selected to raster onto the pieces, creating an almost impossible to decipher puzzle!</p>""",
                    fig(img(dm("generative-design.png"), "Fractal puzzle SVG and laser-cut pieces")),
                ),
                split(
                    h2("Auto-Generated Embroidery Patterns", center=False, level=3) + """
            <p>Created a <strong>Python</strong> script that takes in user size and color parameters and generates a <strong>JEF file</strong> with a pattern of flowers. The JEF file encodes a stitching pattern to decorate a garment using a Computerized Embroidery Machine.</p>
            <p>The designs are made using mathematical functions, with """ + ext("https://en.wikipedia.org/wiki/Euler_spiral", "Euler Spirals")
                    + " as stems and " + ext("https://demonstrations.wolfram.com/FlowerPetalsUsingParametricEquations/", "parametric flowers") + ".</p>",
                    fig(img(dm("generative-process.png"), "Embroidered flowers on a garment and the generated pattern")),
                ),
                split(
                    h2("Food Printing", center=False, level=3) + """
            <p>Created a <strong>Python</strong> script that takes in user parameters and generates <strong>G-code</strong> for a food printer.</p>
            <p>The designs can be used as decorative icing patterns for cookies and cakes.</p>""",
                    fig(img(dm("manufacturing-output.png"), "Printed chocolate icing pattern")),
                ),
            ),
        ],
    )


def main() -> None:
    home()
    publications_redirect()
    research_index()
    portfolio_index()
    all_projects()
    # GitHub Pages: no Jekyll processing needed for plain HTML
    (ROOT / ".nojekyll").write_text("", encoding="utf-8")
    (ROOT / "README.md").write_text(
        "# Joaquin Palacios — Portfolio\n\n"
        "Personal academic portfolio site (GitHub Pages).\n\n"
        "Regenerate pages: `python3 build.py`\n",
        encoding="utf-8",
    )
    print("done")


if __name__ == "__main__":
    main()
