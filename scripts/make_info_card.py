from pathlib import Path
from xml.sax.saxutils import escape

# ============================================
# Output
# ============================================

OUTPUT = Path("images/info-card.svg")
OUTPUT.parent.mkdir(parents=True, exist_ok=True)

# ============================================
# Profile
# ============================================

PROFILE = {
    "Name": "Rishi Changela",
    "Role": "Computer Science & Engineering Student",
    "Location": "India",
    "Education": "B.Tech (ISE)",
    "Learning": "Full Stack • Python • Java • React",
    "Email": "rishichangela79@gmail.com",
    "GitHub": "@Rishipatel79",
    "LinkedIn": "linkedin.com/in/rishi-changela-a49484375",
}

STATUS = "Building projects, exploring AI, and growing one commit at a time."

# ============================================
# Skills
# ============================================

SKILLS = [
    ("Python", 92),
    ("Java", 82),
    ("React", 76),
    ("HTML/CSS", 90),
    ("Git", 85),
]

# ============================================
# Card Settings
# ============================================

WIDTH = 920
HEIGHT = 620

BACKGROUND = "#0d1117"
CARD = "#161b22"
BORDER = "#30363d"

TEXT = "#c9d1d9"
MUTED = "#8b949e"
GREEN = "#3fb950"
BLUE = "#58a6ff"

FONT = "Cascadia Mono, Consolas, monospace"

# ============================================
# Layout
# ============================================

LEFT = 70
VALUE_X = 260

START_Y = 150
LINE_GAP = 36

BAR_X = 260
BAR_WIDTH = 320
BAR_HEIGHT = 12

# ============================================
# SVG Buffer
# ============================================

svg = []
# ============================================
# Start SVG
# ============================================

svg.append(f"""<?xml version="1.0" encoding="UTF-8"?>

<svg xmlns="http://www.w3.org/2000/svg"
     width="{WIDTH}"
     height="{HEIGHT}"
     viewBox="0 0 {WIDTH} {HEIGHT}">

<rect width="100%" height="100%" fill="{BACKGROUND}"/>

<!-- Terminal Window -->

<rect
    x="20"
    y="20"
    width="{WIDTH-40}"
    height="{HEIGHT-40}"
    rx="18"
    fill="{CARD}"
    stroke="{BORDER}"
    stroke-width="2"/>

<!-- Window Buttons -->

<circle cx="55" cy="50" r="8" fill="#ff5f56"/>
<circle cx="80" cy="50" r="8" fill="#ffbd2e"/>
<circle cx="105" cy="50" r="8" fill="#27c93f"/>

<!-- Window Title -->

<text
    x="140"
    y="56"
    font-family="{FONT}"
    font-size="18"
    fill="{MUTED}">

terminal

</text>

<!-- Animated whoami -->

<text
    x="70"
    y="110"
    font-family="{FONT}"
    font-size="28"
    font-weight="bold"
    fill="{TEXT}">

&gt;

<tspan>

 whoami

<animate
    attributeName="opacity"
    values="0;1"
    dur="1.2s"
    fill="freeze"/>

</tspan>

<tspan fill="{GREEN}">

█

<animate
    attributeName="opacity"
    values="1;0;1"
    dur="0.8s"
    repeatCount="indefinite"/>

</tspan>

</text>

<!-- Divider -->

<line
    x1="60"
    y1="125"
    x2="{WIDTH-60}"
    y2="125"
    stroke="{BORDER}"
    stroke-width="1"/>

""")
# ============================================
# Profile Information
# ============================================

y = START_Y

for key, value in PROFILE.items():

    svg.append(f"""
<text
    x="{LEFT}"
    y="{y}"
    font-family="{FONT}"
    font-size="16"
    fill="{GREEN}"
    font-weight="bold">

{escape(key)}:

</text>

<text
    x="{VALUE_X}"
    y="{y}"
    font-family="{FONT}"
    font-size="16"
    fill="{TEXT}">

{escape(value)}

</text>
""")

    y += LINE_GAP

# ============================================
# Skills
# ============================================

y += 25

svg.append(f"""
<text
    x="{LEFT}"
    y="{y}"
    font-family="{FONT}"
    font-size="20"
    fill="{BLUE}"
    font-weight="bold">

Skills

</text>
""")

y += 35

for skill, percent in SKILLS:

    width = int(BAR_WIDTH * percent / 100)

    svg.append(f"""
<text
    x="{LEFT}"
    y="{y}"
    font-family="{FONT}"
    font-size="15"
    fill="{TEXT}">

{skill}

</text>

<rect
    x="{BAR_X}"
    y="{y-11}"
    width="{BAR_WIDTH}"
    height="{BAR_HEIGHT}"
    rx="6"
    fill="#30363d"/>

<rect
    x="{BAR_X}"
    y="{y-11}"
    width="{width}"
    height="{BAR_HEIGHT}"
    rx="6"
    fill="{GREEN}">

<animate
    attributeName="width"
    from="0"
    to="{width}"
    dur="1.5s"
    fill="freeze"/>

</rect>

<text
    x="{BAR_X + BAR_WIDTH + 15}"
    y="{y}"
    font-family="{FONT}"
    font-size="14"
    fill="{GREEN}">

{percent}%

</text>
""")

    y += 34

# ============================================
# Status
# ============================================

y += 25

svg.append(f"""
<line
    x1="60"
    y1="{y-20}"
    x2="{WIDTH-60}"
    y2="{y-20}"
    stroke="{BORDER}"/>

<text
    x="{LEFT}"
    y="{y}"
    font-family="{FONT}"
    font-size="16"
    fill="{BLUE}"
    font-weight="bold">

Status

</text>

<text
    x="{VALUE_X}"
    y="{y}"
    font-family="{FONT}"
    font-size="16"
    fill="{TEXT}">

{escape(STATUS)}

</text>
""")

# ============================================
# Footer
# ============================================

svg.append(f"""
<text
    x="{LEFT}"
    y="{HEIGHT-30}"
    font-family="{FONT}"
    font-size="14"
    fill="{GREEN}">

rishi@github:~$

<tspan>

█

<animate
    attributeName="opacity"
    values="1;0;1"
    dur="0.8s"
    repeatCount="indefinite"/>

</tspan>

</text>

</svg>
""")

# ============================================
# Save SVG
# ============================================

OUTPUT.write_text("".join(svg), encoding="utf-8")

print("=" * 50)
print("Info card generated successfully!")
print(f"Saved to: {OUTPUT}")
print("=" * 50)