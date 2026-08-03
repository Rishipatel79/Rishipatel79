from pathlib import Path

# ------------------------------------------------------------
# Project paths
# ------------------------------------------------------------

ROOT = Path(__file__).resolve().parent.parent
README_PATH = ROOT / "README.md"

ASCII_SVG = "images/avi-ascii.svg"
INFO_CARD_SVG = "images/info-card.svg"
HEATMAP_SVG = "images/contribution-heatmap.svg"

# ------------------------------------------------------------
# README template
# ------------------------------------------------------------

README = f"""<div align="center">

<h3><code>Rishipatel79@github ~ $ ./contributions.sh</code></h3>

<img src="{HEATMAP_SVG}" width="860">

<br><br>

<h3><code>Rishipatel79@github ~ $ whoami</code></h3>

<table>
<tr>

<td valign="top">
<img src="{ASCII_SVG}" width="370">
</td>

<td valign="top">
<img src="{INFO_CARD_SVG}" width="490">
</td>

</tr>
</table>

</div>
"""

# ------------------------------------------------------------
# Write README.md
# ------------------------------------------------------------

README_PATH.write_text(README, encoding="utf-8")

print(f"✅ README generated successfully!")
print(f"Location: {README_PATH}")