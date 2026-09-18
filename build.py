#!/usr/bin/env python3
"""Generate static portfolio pages for joaquin-ps.github.io."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent

EMAIL = "joaquin.palacios@columbia.edu"
LINKEDIN = "https://www.linkedin.com/in/joaquin-b-palacios"

RESEARCH_LINKS = [
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


def depth_prefix(path: str) -> str:
    # path like "" or "research/roam-hand-3"
    parts = [p for p in path.strip("/").split("/") if p]
    return "../" * len(parts) if parts else "./"


def shell(title: str, path: str, current: str, body: str, description: str = "") -> str:
    prefix = depth_prefix(path)
    desc = description or f"{title} — Joaquin Palacios, robotics engineer and PhD candidate at Columbia University."
    research_items = "\n".join(
        f'          <a href="{prefix}{href.lstrip("/")}">{label}</a>' for label, href in RESEARCH_LINKS
    )
    portfolio_items = "\n".join(
        f'          <a href="{prefix}{href.lstrip("/")}">{label}</a>' for label, href in PORTFOLIO_LINKS
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
  <link rel="stylesheet" href="{prefix}assets/css/styles.css">
</head>
<body>
  <a class="skip-link" href="#content">Skip to content</a>
  <header class="site-header">
    <div class="nav-wrap">
      <a class="brand" href="{prefix}">Joaquin Palacios</a>
      <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="site-nav">Menu</button>
      <nav class="nav" id="site-nav" aria-label="Primary">
        <a href="{prefix}publications/"{cur("publications")}>Publications</a>
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
      <p>© Joaquin Palacios · Robotics · Columbia University / ROAM Lab</p>
    </div>
  </footer>
  <script src="{prefix}assets/js/main.js"></script>
</body>
</html>
"""


def write(rel: str, html: str) -> None:
    out = ROOT / rel
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8")
    print("wrote", rel)


def figure(src: str, caption: str = "", video: bool = False) -> str:
    if video:
        media = f'<video controls playsinline preload="metadata" src="{src}"></video>'
    else:
        media = f'<img src="{src}" alt="{caption or ""}" loading="lazy">'
    cap = f"<figcaption>{caption}</figcaption>" if caption else ""
    return f"<figure>{media}{cap}</figure>"


def meta_block(items: list[tuple[str, str]]) -> str:
    rows = "\n".join(
        f'    <div class="meta"><dt>{k}</dt><dd>{v}</dd></div>' for k, v in items if v
    )
    return f'<dl class="meta-grid">\n{rows}\n  </dl>'


# ---------- pages ----------

def home() -> None:
    featured = [
        ("research/roam-hand-3/", "media/home/highlight-roam-hand-3.png", "ROAM Hand 3",
         "Robot hand with 6-axis F/T sensorized fingertips and <strong>novel kinematics validated via RL policies.</strong>"),
        ("research/myhand-sci/", "media/home/highlight-myhand-sci.png", "MyHand SCI",
         "<strong>Wearable robot</strong> to assist grasping for individuals with <strong>Spinal Cord Injuries.</strong>"),
        ("portfolio/plan-bee/", "media/home/highlight-plan-bee.png", "Plan Bee",
         "<strong>Robotic crop pollination</strong> for Vertical Farming."),
    ]
    projects = [
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
    feature_slides = "\n".join(
        f'''        <a class="feature-slide{" is-active" if i == 0 else ""}" href="{href}" data-index="{i}">
          <img src="{img}" alt="{title}">
          <div class="feature-copy">
            <h3>{title}</h3>
            <p>{blurb}</p>
            <span class="feature-link">View project →</span>
          </div>
        </a>'''
        for i, (href, img, title, blurb) in enumerate(featured)
    )
    feature_dots = "\n".join(
        '          <button type="button" aria-label="Show slide {n}"{cls} data-index="{i}"></button>'.format(
            n=i + 1,
            i=i,
            cls=' class="is-active"' if i == 0 else "",
        )
        for i in range(len(featured))
    )
    project_cards = "\n".join(
        f'''      <a class="project-card reveal" href="{href}">
        <div class="project-media">
          <img src="{img}" alt="{title}">
        </div>
        <h3>{title}</h3>
        <p>{blurb}</p>
      </a>'''
        for href, img, title, blurb in projects
    )
    body = f"""
    <section class="hero">
      <div class="hero-copy">
        <p class="eyebrow">Robotics · Columbia University · ROAM Lab</p>
        <h1>Joaquin Palacios</h1>
        <p class="lede">
          Robotics engineer from <strong>Quito, Ecuador</strong>.
          PhD candidate in <strong>Mechanical Engineering</strong> at <strong>Columbia University</strong>,
          research assistant at <strong>ROAM Lab</strong>, advised by Matei Ciocarlie.
        </p>
        <p class="lede">
          Passionate about the full stack of robotics: mechanical design, firmware, controls, and robot learning.
          Research interests in <strong>autonomous robot manipulation</strong> and <strong>medical assistive robotics</strong>.
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

    <section class="section">
      <div class="section-head">
        <div>
          <h2>Highlights</h2>
          <p>Featured work in dexterous manipulation, assistive robotics, and agricultural robotics.</p>
        </div>
      </div>
      <div class="feature-carousel reveal" data-carousel>
        <div class="feature-track">
{feature_slides}
        </div>
        <div class="feature-nav">
          <button class="feature-btn" type="button" data-carousel-prev aria-label="Previous highlight">← Prev</button>
          <div class="feature-dots" data-carousel-dots>
{feature_dots}
          </div>
          <button class="feature-btn" type="button" data-carousel-next aria-label="Next highlight">Next →</button>
        </div>
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
        <a class="teaser reveal" href="publications/">
          <img class="teaser-thumb" src="media/home/cover-myhand-sci.jpg" alt="">
          <div class="teaser-body">
            <h3>Publications</h3>
            <p>Journal and workshop papers on assistive hand exoskeletons for SCI.</p>
            <span>Learn more →</span>
          </div>
        </a>
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


def publications() -> None:
    body = f"""
    <header class="page-hero">
      <p class="crumb"><a href="../">Home</a> / Publications</p>
      <h1>Publications</h1>
      <p class="tagline">Peer-reviewed journal and workshop publications on assistive robotics for spinal cord injury.</p>
    </header>

    <section class="section">
      <h2 class="reveal" style="font-family:var(--font-display);letter-spacing:-0.02em">Journal Publications</h2>
      <article class="pub reveal">
        <figure class="pub-thumb">
          <img src="../media/publications/myhand-sci-device.png" alt="MyHand-SCI device and grasp/maintain/release control diagram">
        </figure>
        <div class="pub-body">
          <div class="year-label">2024</div>
          <h3>Grasp Force Assistance via Throttle-based Wrist Angle Control on a Robotic Hand Orthosis for C6–C7 Spinal Cord Injury</h3>
          <p class="authors">Joaquin Palacios*, Alexandra Deli-Ivanov*, Ava Chen, Lauren Winterbottom, Dawn M. Nilsen, Joel Stein, and Matei Ciocarlie</p>
          <p class="venue">IEEE Transactions on Medical Robotics and Bionics (T-MRB) — Accepted</p>
          <div class="pub-links">
            <a class="btn btn-ghost" href="../media/publications/myhand-sci-device.png">Figure</a>
          </div>
        </div>
      </article>
    </section>

    <section class="section">
      <h2 class="reveal" style="font-family:var(--font-display);letter-spacing:-0.02em">Workshop Publications</h2>
      <article class="pub reveal">
        <figure class="pub-thumb">
          <img src="../media/publications/myhand-sci-figure.jpg" alt="MyHand-SCI assisting a grasp of a small can">
        </figure>
        <div class="pub-body">
          <div class="year-label">2023</div>
          <h3>Towards Tenodesis-Modulated Control of an Assistive Hand Exoskeleton for SCI</h3>
          <p class="authors">Joaquin Palacios*, Alexandra Deli-Ivanov*, Ava Chen, Lauren Winterbottom, Dawn M. Nilsen, Joel Stein, and Matei Ciocarlie</p>
          <p class="venue">IROS 2023 — Assistive Robots for Citizens Workshop (Accepted)</p>
          <div class="pub-links">
            <a class="btn btn-primary" href="../media/publications/iros-2023-workshop-paper.pdf">Paper (PDF)</a>
            <a class="btn btn-ghost" href="../media/publications/iros-2023-poster.pdf">Poster (PDF)</a>
          </div>
        </div>
      </article>
    </section>
"""
    write("publications/index.html", shell("Publications — Joaquin Palacios", "publications", "publications", body))


def research_index() -> None:
    body = f"""
    <header class="page-hero">
      <p class="crumb"><a href="../">Home</a> / Research</p>
      <h1>Research</h1>
      <p class="tagline">Hardware and controls research in dexterous manipulation and assistive robotics at ROAM Lab.</p>
    </header>
    <div class="project-list">
      <a class="project-row reveal" href="roam-hand-3/">
        <img src="../media/home/highlight-roam-hand-3.png" alt="ROAM Hand 3">
        <div>
          <h2>ROAM Hand 3</h2>
          <p>Novel dexterous hand kinematics with 6-axis F/T fingertips, validated via reinforcement learning.</p>
        </div>
        <span class="year">2024–2025</span>
      </a>
      <a class="project-row reveal" href="myhand-sci/">
        <img src="../media/research/myhand-sci.png" alt="MyHand-SCI">
        <div>
          <h2>MyHand-SCI</h2>
          <p>Wearable robot for grasping assistance using tenodesis-based user control for people with SCI.</p>
        </div>
        <span class="year">2022–2023</span>
      </a>
      <a class="project-row reveal" href="roam-hand/">
        <img src="../media/research/roam-hand.png" alt="ROAM Hand 1">
        <div>
          <h2>ROAM Hand 1</h2>
          <p>Tendon-driven robot hand exploring proprioception for dexterous manipulation.</p>
        </div>
        <span class="year">2023</span>
      </a>
    </div>
"""
    write("research/index.html", shell("Research — Joaquin Palacios", "research", "research", body))


def portfolio_index() -> None:
    items = [
        ("plan-bee/", "../media/portfolio/plan-bee.png", "Plan Bee",
         "Robotic crop pollination for vertical farms.", "2023"),
        ("crab-io/", "../media/portfolio/crab-io.png", "Crab.io",
         "A quadruped robot known for being cute and fast.", "2022"),
        ("button-pressing-machine/", "../media/portfolio/button-pressing-machine.png", "Button-Pressing Machine",
         "Mechatronics, machine design, controls, and machining.", "2022"),
        ("applied-robotics/", "../media/portfolio/applied-robotics.png", "Applied Robotics",
         "ROS 2 cartesian control, IK, and RRT path planning on UR5e and Franka Emika.", "2023"),
        ("digital-manufacturing/", "../media/portfolio/digital-manufacturing.png", "Digital Manufacturing",
         "Generative design, topology optimization, and additive manufacturing.", "2022–2023"),
    ]
    rows = "\n".join(
        f'''      <a class="project-row reveal" href="{href}">
        <img src="{img}" alt="{title}">
        <div>
          <h2>{title}</h2>
          <p>{blurb}</p>
        </div>
        <span class="year">{year}</span>
      </a>'''
        for href, img, title, blurb, year in items
    )
    body = f"""
    <header class="page-hero">
      <p class="crumb"><a href="../">Home</a> / Portfolio</p>
      <h1>Portfolio</h1>
      <p class="tagline">Course and personal projects spanning agricultural robotics, locomotion, mechatronics, and digital manufacturing.</p>
    </header>
    <div class="project-list">
{rows}
    </div>
"""
    write("portfolio/index.html", shell("Portfolio — Joaquin Palacios", "portfolio", "portfolio", body))


def project_page(
    rel_dir: str,
    current: str,
    title: str,
    crumb_parent: tuple[str, str],
    tagline: str,
    meta: list[tuple[str, str]],
    prose_html: str,
    gallery_html: str,
) -> None:
    parent_label, parent_href = crumb_parent
    prefix = depth_prefix(rel_dir)
    body = f"""
    <header class="page-hero">
      <p class="crumb"><a href="{prefix}">Home</a> / <a href="{prefix}{parent_href}">{parent_label}</a> / {title}</p>
      <h1>{title}</h1>
      <p class="tagline">{tagline}</p>
    </header>
    {meta_block(meta)}
    <div class="prose reveal">
{prose_html}
    </div>
    <section class="section reveal">
      <h2 style="font-family:var(--font-display);letter-spacing:-0.02em;margin:0 0 1rem">Gallery</h2>
      <div class="gallery wide">
{gallery_html}
      </div>
    </section>
"""
    write(f"{rel_dir}/index.html", shell(f"{title} — Joaquin Palacios", rel_dir, current, body, tagline))


def all_projects() -> None:
    m = lambda folder, name: f"../../media/{folder}/{name}"

    project_page(
        "research/roam-hand-3", "research", "ROAM Hand 3", ("Research", "research/"),
        "Robot hand with 6-axis F/T sensorized fingertips and novel kinematics validated via RL policies.",
        [
            ("Research area", "Autonomous robotic manipulation"),
            ("Contribution", "Mechanical design; kinematic validation via RL"),
            ("Years", "2024 – 2025"),
            ("Collaborators", "Eugene Sohn, Veronika Zam, Amr El-Azizi, Sharfin Islam, Dongxiao Yang, Eric Chang, Zhanpeng He, Pedro Piacenza, Matei Ciocarlie"),
            ("Press", 'Wall Street Journal (2025)'),
        ],
        """
      <p>Iterative design cycle with robot learning in-the-loop to develop a novel dexterous robot hand.
      Kinematics are validated by training dexterous in-hand manipulation skills via reinforcement learning.</p>
      <p>6-axis force/torque sensorized fingertip development is led by collaborators Amr El-Azizi, Sharfin Islam, and Pedro Piacenza.</p>
      <h2>Variants</h2>
      <ul>
        <li><strong>Anthropomorphic Hand (RH3-A)</strong></li>
        <li><strong>Non-Anthropomorphic Hand (RH3-NA)</strong></li>
      </ul>
""",
        "\n".join([
            figure(m("roam-hand-3", "ur5e-rubiks-cube.png"), "RH3 with UR5e"),
            figure(m("roam-hand-3", "rh3-anthropomorphic.png"), "Anthropomorphic hand (RH3-A)"),
            figure(m("roam-hand-3", "rh3-top-view.png"), "Top view"),
            figure(m("roam-hand-3", "ur5e-tennis-ball.png"), "Manipulation demo"),
            figure(m("roam-hand-3", "rh3-na-with-block.png"), "Non-anthropomorphic hand (RH3-NA)"),
            figure(m("roam-hand-3", "rh3-na-spread.png"), "RH3-NA spread"),
            figure(m("roam-hand-3", "in-hand-manipulation.mp4"), "In-hand manipulation", True),
            figure(m("roam-hand-3", "lug-nut-manipulation.mp4"), "Manipulation sequence", True),
            figure(m("roam-hand-3", "rh3-na-demo.mp4"), "RH3-NA demo", True),
            figure(m("roam-hand-3", "hardware-demo.mp4"), "Hardware video", True),
        ]),
    )

    project_page(
        "research/myhand-sci", "research", "MyHand-SCI", ("Research", "research/"),
        "A wearable robot that provides active grasping assistance for individuals with spinal cord injuries (SCI).",
        [
            ("Research area", "Assistive robotics"),
            ("Contribution", "Mechanical design, firmware, experiment design"),
            ("Years", "2022 – 2023"),
            ("Collaborators", "Alexandra Deli-Ivanov, Ava Chen, Lauren Winterbottom, Dawn M. Nilsen, Joel Stein, Matei Ciocarlie"),
        ],
        f"""
      <p>For MyHand-SCI we adopted a philosophy of augmenting, rather than overshadowing, an individual’s residual motor skills.
      The device aims to leverage the <strong>tenodesis grasp</strong>, a compensatory grasping pattern used by individuals with C5–C6 injuries, as a user control modality.</p>
      <p>This can make the device more intuitive, give the user more agency and direct feedback, and encourage adoption.</p>
      <h2>Publications</h2>
      <ul>
        <li>Journal paper, T-MRB (Nov 2024)</li>
        <li>Workshop abstract, IROS 2023 — spotlight and poster at the Assistive Robots for Citizens Workshop</li>
      </ul>
      <p><a href="https://www.youtube.com/watch?v=SEi8ZkJe4dQ" rel="noopener noreferrer">Watch the demo on YouTube</a></p>
""",
        figure(m("myhand-sci", "device.png"), "MyHand-SCI device"),
    )

    project_page(
        "research/roam-hand", "research", "ROAM Hand 1", ("Research", "research/"),
        "A tendon-driven robot hand exploring proprioception in dexterous manipulation.",
        [
            ("Research area", "Robotic manipulation"),
            ("Contribution", "Mechanical design; firmware implementation"),
            ("Year", "2023"),
        ],
        """
      <p>The ROAM Hand was developed as a hardware testbed to explore how proprioception can augment other sensing modalities—
      such as tactile sensing and computer vision—toward dexterous manipulation.</p>
      <p>Fingers are driven by tendons connected to servos inside the palm, with a load cell measuring the reaction torque of each motor,
      allowing joint torque sensing. This is robotic proprioception.</p>
      <h2>My role</h2>
      <ul>
        <li>Redesign of tendon routing and pulley transmission to reduce friction and improve torque sensing, keeping joints uncoupled.</li>
        <li>Firmware for position control and torque sensing, integrated with ROS.</li>
      </ul>
""",
        "\n".join([
            figure(m("roam-hand", "render.png"), "Render of ROAM Hand"),
            figure(m("roam-hand", "tendon-routing.png"), "Tendon routing"),
            figure(m("roam-hand", "joint-pulleys.jpg"), "Joint pulleys"),
            figure(m("roam-hand", "manufacturing-detail.png"), "Manufacturing detail"),
            figure(m("roam-hand", "roll-joint.jpg"), "Roll joint / floating piece"),
            figure(m("roam-hand", "finger-motion-b.gif"), "Motion GIF"),
            figure(m("roam-hand", "finger-motion-a.gif"), "Motion GIF"),
            figure(m("roam-hand", "hardware-demo.mp4"), "Hardware video", True),
        ]),
    )

    project_page(
        "portfolio/plan-bee", "portfolio", "Plan Bee", ("Portfolio", "portfolio/"),
        "An agricultural robot for pollination in enclosed vertical farms.",
        [
            ("Area", "Agricultural robotics"),
            ("Contribution", "Mechatronics; software (firmware, planning, computer vision)"),
            ("Year", "2023"),
            ("Award", "1st Place — Columbia Engineering 2023 Senior Design Expo"),
            ("Collaborators", "Valentina Gonzalez, Siddhanth Lath, Georgios Thomakos, Aiman Najah"),
        ],
        """
      <p>Plan Bee is a five-degree-of-freedom robot with onboard computer vision and a rotating brush end-effector.
      It identifies flowers in its workspace and pollinates them without humans or live bees, using an image segmentation network
      and a depth camera to localize flowers and deploy pollen-transfer routines.</p>
      <h2>The problem</h2>
      <p>Vertical farming is resource-efficient, but enclosed environments remove natural pollinators such as insects and wind,
      limiting which crops can be grown.</p>
      <h2>Personal contributions</h2>
      <ul>
        <li><strong>Software:</strong> flower detection model; depth-camera localization; kinematics, cartesian control, and path planning.</li>
        <li><strong>Electronics &amp; firmware:</strong> Arduino motor control; stepper/servo actuation; wiring.</li>
        <li><strong>Hardware:</strong> gantry-style 5-DOF kinematics; lead-screw actuators; CAD; manufacturing and assembly.</li>
      </ul>
""",
        "\n".join([
            figure(m("plan-bee", "vertical-farm.webp"), "Vertical farming context"),
            figure(m("plan-bee", "full-system.png"), "Full system"),
            figure(m("plan-bee", "system-view.png"), "System view"),
            figure(m("plan-bee", "end-effector.png"), "End-effector"),
            figure(m("plan-bee", "workspace.png"), "Workspace"),
            figure(m("plan-bee", "cad-design.png"), "CAD / design"),
            figure(m("plan-bee", "team-at-expo.jpg"), "Team at Senior Design Expo"),
            figure(m("plan-bee", "pollination-routine.mp4"), "Pollination routine", True),
            figure(m("plan-bee", "demo-broll.mp4"), "Demo b-roll", True),
        ]),
    )

    project_page(
        "portfolio/crab-io", "portfolio", "Crab.io", ("Portfolio", "portfolio/"),
        "A quadruped robot known for being cute and fast.",
        [
            ("Area", "Robotic locomotion"),
            ("Contribution", "Mechatronics design; firmware"),
            ("Year", "2022"),
            ("Context", "Robotics Studio, Columbia University — with Valentina Gonzalez"),
        ],
        """
      <p>Designed and built as part of Columbia’s Robotics Studio course. Topology optimization kept the robot lightweight for speed.</p>
""",
        "\n".join([
            figure(m("crab-io", "render.png"), "Crab.io render"),
            figure(m("crab-io", "topology-optimized-leg.jpg"), "Topology-optimized leg"),
            figure(m("crab-io", "gait.png"), "Gait"),
            figure(m("crab-io", "walking-demo.mp4"), "Walking demo", True),
            figure(m("crab-io", "locomotion-demo.mp4"), "Locomotion demo", True),
        ]),
    )

    project_page(
        "portfolio/button-pressing-machine", "portfolio", "Button-Pressing Machine", ("Portfolio", "portfolio/"),
        "An exploration of mechatronics, machine design, controls, and machining.",
        [
            ("Area", "Mechatronics"),
            ("Contribution", "Mechanical design and firmware"),
            ("Year", "2022"),
            ("Collaborators", "Valentina Gonzalez, Siddhanth Lath, Georgios Thomakos, Aiman Najah"),
        ],
        """
      <p>In an arcade-style button-pressing game, a four-bar linkage with a solenoid presses buttons as quickly as possible.
      A PID controller drives rapid motion between buttons.</p>
      <p>Responsibilities included Arduino firmware and gain tuning, four-bar linkage design for the required trajectory,
      and manufacturing aluminum links via waterjet cutting and CNC milling.</p>
""",
        "\n".join([
            figure(m("button-pressing-machine", "mechanism-closeup.png"), "Mechanism close-up"),
            figure(m("button-pressing-machine", "full-machine.jpg"), "Full machine"),
            figure(m("button-pressing-machine", "machine-in-action.mp4"), "Machine in action", True),
        ]),
    )

    project_page(
        "portfolio/applied-robotics", "portfolio", "Applied Robotics", ("Portfolio", "portfolio/"),
        "ROS 2 projects implementing cartesian control, inverse kinematics, and RRT path planning from scratch.",
        [
            ("Robots", "UR5e, Franka Emika"),
            ("Stack", "ROS 2"),
            ("Year", "2023"),
        ],
        """
      <h2>Cartesian control</h2>
      <p><strong>UR5e:</strong> end-effector pose controlled along one degree of freedom without influencing the rest.
      Singularities handled with the Jacobian pseudoinverse.</p>
      <p><strong>Franka Emika:</strong> as a redundant 7-DOF arm, joints can move in the Jacobian nullspace without changing end-effector pose.</p>
      <h2>Path planning</h2>
      <p>RRT-based planning on the UR5e, including scenes with obstacles.</p>
""",
        "\n".join([
            figure(m("applied-robotics", "ur5e-cartesian-control.mp4"), "Cartesian control — UR5e", True),
            figure(m("applied-robotics", "franka-cartesian-control.mp4"), "Cartesian control — Franka", True),
            figure(m("applied-robotics", "inverse-kinematics.mp4"), "Inverse kinematics", True),
            figure(m("applied-robotics", "teleop-screencast.mp4"), "Screencast", True),
            figure(m("applied-robotics", "rrt-no-obstacles.mp4"), "RRT — no obstacles", True),
            figure(m("applied-robotics", "rrt-simple-obstacle.mp4"), "RRT — simple obstacle", True),
            figure(m("applied-robotics", "rrt-hard-obstacle.mp4"), "RRT — hard obstacle", True),
        ]),
    )

    project_page(
        "portfolio/digital-manufacturing", "portfolio", "Digital Manufacturing", ("Portfolio", "portfolio/"),
        "Projects exploring generative design, topology optimization, additive manufacturing, and more.",
        [
            ("Years", "2022 – 2023"),
            ("Themes", "Generative design · topology optimization · additive manufacturing"),
        ],
        """
      <p>Leveraging modern software and manufacturing to create art and produce novel designs.</p>
      <h2>Topology optimization</h2>
      <p>Lightweight robotic arm designed in Altair Inspire as an educational model for topology optimization.</p>
      <h2>Generative design</h2>
      <p>Code-generated designs for laser cutting, computerized embroidery, and additive food printing.</p>
      <ul>
        <li><strong>Fractal puzzles:</strong> MATLAB → SVG for laser-cut jigsaws with fractal rasters.</li>
        <li><strong>Embroidery:</strong> Python → JEF files with Euler-spiral stems and parametric flowers.</li>
        <li><strong>Food printing:</strong> Python → G-code for decorative icing patterns.</li>
      </ul>
""",
        "\n".join([
            figure(m("digital-manufacturing", "topology-optimized-arm.png"), "Topology-optimized arm"),
            figure(m("digital-manufacturing", "generative-design.png"), "Generative design"),
            figure(m("digital-manufacturing", "generative-process.png"), "Process screenshot"),
            figure(m("digital-manufacturing", "manufacturing-output.png"), "Manufacturing output"),
        ]),
    )


def main() -> None:
    home()
    publications()
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
