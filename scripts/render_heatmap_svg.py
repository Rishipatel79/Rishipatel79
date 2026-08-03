import json
from pathlib import Path

# ==========================================
# File Paths
# ==========================================

DATA_FILE = Path("data/contributions.json")
OUTPUT_DIR = Path("images")
OUTPUT_FILE = OUTPUT_DIR / "contribution-heatmap.svg"

# ==========================================
# SVG Settings
# ==========================================

CELL_SIZE = 12
CELL_GAP = 3

LEFT_MARGIN = 35
TOP_MARGIN = 30

ROWS = 7
COLS = 53

SVG_WIDTH = LEFT_MARGIN + (COLS * (CELL_SIZE + CELL_GAP)) + 20
SVG_HEIGHT = TOP_MARGIN + (ROWS * (CELL_SIZE + CELL_GAP)) + 20

BACKGROUND = "#0d1117"

# GitHub Dark Theme Colors
LEVEL_COLORS = {
    "NONE": "#161b22",
    "FIRST_QUARTILE": "#0e4429",
    "SECOND_QUARTILE": "#006d32",
    "THIRD_QUARTILE": "#26a641",
    "FOURTH_QUARTILE": "#39d353",
}

# ==========================================
# Load Contribution Data
# ==========================================

def load_data():

    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

# ==========================================
# Create SVG Header
# ==========================================

def svg_header():

    return f"""<svg
xmlns="http://www.w3.org/2000/svg"
width="{SVG_WIDTH}"
height="{SVG_HEIGHT}"
viewBox="0 0 {SVG_WIDTH} {SVG_HEIGHT}">

<rect
width="100%"
height="100%"
fill="{BACKGROUND}"/>
"""

# ==========================================
# SVG Footer
# ==========================================

def svg_footer():

    return "</svg>"
if __name__ == "__main__":

    data = load_data()

    print("Loaded contribution data successfully!")

    print(type(data))
    # ==========================================
# Draw Heatmap
# ==========================================

def draw_heatmap(data):

    svg = []

    weeks = (
        data["data"]["user"]["contributionsCollection"]
            ["contributionCalendar"]["weeks"]
    )

    for week_index, week in enumerate(weeks):

        for day in week["contributionDays"]:

            x = LEFT_MARGIN + week_index * (CELL_SIZE + CELL_GAP)

            y = (
                TOP_MARGIN
                + day["weekday"] * (CELL_SIZE + CELL_GAP)
            )

            color = LEVEL_COLORS.get(
                day["contributionLevel"],
                LEVEL_COLORS["NONE"]
            )

            svg.append(f"""
<rect
    x="{x}"
    y="{y}"
    width="{CELL_SIZE}"
    height="{CELL_SIZE}"
    rx="2"
    fill="{color}"
    opacity="0">

    <animate
        attributeName="opacity"
        from="0"
        to="1"
        begin="{week_index * 0.03:.2f}s"
        dur="0.4s"
        fill="freeze"/>
</rect>
""")

    return "".join(svg)
if __name__ == "__main__":

    data = load_data()

    OUTPUT_DIR.mkdir(exist_ok=True)

    svg = []

    svg.append(svg_header())

    svg.append(draw_heatmap(data))

    svg.append(svg_footer())

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("".join(svg))

    print(f"✅ Heatmap saved to {OUTPUT_FILE}")