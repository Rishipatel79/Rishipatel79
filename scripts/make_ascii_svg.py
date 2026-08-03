from PIL import Image
from xml.sax.saxutils import escape

# ============================================
# Configuration
# ============================================

INPUT_IMAGE = "assets/source-prepped.png"
OUTPUT_SVG = "images/avi-ascii.svg"

# More detail
ASCII_WIDTH = 115

# Better font settings
FONT_SIZE = 7
LINE_HEIGHT = 8
CHAR_WIDTH = 4.8

FONT_FAMILY = "'Cascadia Mono','Consolas','Courier New',monospace"

# Character ramp
RAMP = " .`:-=+*cs#%@"

# GitHub Dark Theme
BACKGROUND = "#0d1117"
TEXT_COLOR = "#c9d1d9"

# ============================================
# Load image
# ============================================

print("Loading image...")

image = Image.open(INPUT_IMAGE).convert("L")

width, height = image.size

aspect_ratio = height / width

ASCII_HEIGHT = int(ASCII_WIDTH * aspect_ratio * 0.55)

image = image.resize((ASCII_WIDTH, ASCII_HEIGHT))

print(f"ASCII Size : {ASCII_WIDTH} x {ASCII_HEIGHT}")

# ============================================
# Convert image to ASCII
# ============================================

pixels = list(image.getdata())

ascii_chars = []

for pixel in pixels:

    index = int((255 - pixel) / 255 * (len(RAMP) - 1))

    ascii_chars.append(RAMP[index])

ascii_rows = []

for i in range(0, len(ascii_chars), ASCII_WIDTH):

    row = "".join(ascii_chars[i:i + ASCII_WIDTH])

    ascii_rows.append(row)

print("ASCII conversion completed.")

# ============================================
# SVG Size
# ============================================

SVG_WIDTH = int(ASCII_WIDTH * CHAR_WIDTH + 40)
SVG_HEIGHT = ASCII_HEIGHT * LINE_HEIGHT + 30

svg = []

svg.append(f'''<svg xmlns="http://www.w3.org/2000/svg"
width="{SVG_WIDTH}"
height="{SVG_HEIGHT}"
viewBox="0 0 {SVG_WIDTH} {SVG_HEIGHT}">

<rect width="100%" height="100%" fill="{BACKGROUND}"/>

<style>
text{{
font-family:{FONT_FAMILY};
font-size:{FONT_SIZE}px;
fill:{TEXT_COLOR};
white-space:pre;
dominant-baseline:hanging;
}}
</style>
''')

# ============================================
# Draw ASCII
# ============================================

START_X = 20
START_Y = 15
ROW_DELAY = 0.05

for row_index, row in enumerate(ascii_rows):

    y = START_Y + row_index * LINE_HEIGHT

    safe_row = escape(row)

    svg.append(f'''
<text x="{START_X}" y="{y}" opacity="0">
<animate
attributeName="opacity"
from="0"
to="1"
begin="{row_index * ROW_DELAY:.2f}s"
dur="0.01s"
fill="freeze"/>
{safe_row}
</text>
''')

# ============================================
# Blinking Cursor
# ============================================

cursor_y = START_Y + ASCII_HEIGHT * LINE_HEIGHT

svg.append(f'''
<text x="{START_X}" y="{cursor_y}" fill="#39d353">
█
<animate
attributeName="opacity"
values="1;0;1"
dur="1s"
repeatCount="indefinite"/>
</text>
''')

# ============================================
# Finish SVG
# ============================================

svg.append("</svg>")

with open(OUTPUT_SVG, "w", encoding="utf-8") as f:
    f.write("".join(svg))

print(f"\nSVG saved to: {OUTPUT_SVG}")