"""Draw the profile's two graphics as SVG, in a light and a dark variant.

    python scripts/build_assets.py

Standard library only. GitHub shows READMEs as static images, so the header's
animation is plain CSS inside the SVG, and every element is drawn in its final
position first: a viewer that ignores the animation still sees the finished
picture.
"""
import csv
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"
DATA = ROOT / "data" / "graduates_at_or_below_rm2500.csv"

FONT = "system-ui, -apple-system, 'Segoe UI', Helvetica, Arial, sans-serif"
THEMES = {
    "light": {
        "surface": "#ffffff", "ink": "#1f2328", "secondary": "#59636e", "muted": "#818b98",
        "grid": "#d9dee3", "axis": "#b7bfc8", "series": "#2a78d6", "accent": "#eb6834",
        "border": "#d1d9e0",
    },
    "dark": {
        "surface": "#0d1117", "ink": "#f0f6fc", "secondary": "#9198a1", "muted": "#7d8590",
        "grid": "#262c36", "axis": "#3d444d", "series": "#3987e5", "accent": "#d95926",
        "border": "#3d444d",
    },
}
MY_FIELD = "Natural sciences, mathematics and statistics"
OVERALL_SHARE = 49.7  # all first-degree graduates, from the report's overall row


def fmt(number):
    return f"{number:.1f}".rstrip("0").rstrip(".")


def card(theme, width, height):
    """The graphic's own background.

    README images cannot see the page they sit on, and a visitor whose GitHub
    theme differs from their system theme may be served the other variant. A
    filled card keeps either variant legible on either page.
    """
    return (
        f'<rect x="0.5" y="0.5" width="{width - 1}" height="{height - 1}" rx="10" '
        f'fill="{theme["surface"]}" stroke="{theme["border"]}"/>'
    )


def least_squares(xs, ys):
    mean_x, mean_y = sum(xs) / len(xs), sum(ys) / len(ys)
    slope = sum((x - mean_x) * (y - mean_y) for x, y in zip(xs, ys)) / sum((x - mean_x) ** 2 for x in xs)
    return mean_y - slope * mean_x, slope


def header(theme):
    """A scatter plot with its fitted line and residuals, beside the name."""
    width, height = 880, 230
    left, right, top, bottom = 500, 846, 34, 190

    rng = random.Random(27)
    xs = sorted(rng.uniform(0.04, 0.96) for _ in range(17))
    ys = [0.2 + 0.5 * x + rng.gauss(0, 0.05) for x in xs]
    ys[8] += 0.34  # one point the line does not explain
    intercept, slope = least_squares(xs, ys)  # the line drawn is the real fit

    def px(x):
        return left + x * (right - left)

    def py(y):
        return bottom - y * (bottom - top)

    residuals = [y - (intercept + slope * x) for x, y in zip(xs, ys)]
    outlier = max(range(len(xs)), key=lambda i: abs(residuals[i]))
    line_length = ((px(1) - px(0)) ** 2 + (py(intercept + slope) - py(intercept)) ** 2) ** 0.5

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" '
        f'height="{height}" role="img" aria-labelledby="t d" font-family="{FONT}">',
        '<title id="t">Luqman Syahrulnizam</title>',
        '<desc id="d">A scatter plot with a fitted regression line. One point sits far above the line; '
        'the gap between it and the line is labelled the residual.</desc>',
        "<style>",
        f".fit{{stroke-dasharray:{line_length:.0f};animation:draw 1.6s ease-out both}}",
        ".dot{animation:pop .5s ease-out both}",
        ".res{animation:fade .6s ease-out both}",
        ".note{animation:fade .8s ease-out 2.9s both}",
        f"@keyframes draw{{from{{stroke-dashoffset:{line_length:.0f}}}to{{stroke-dashoffset:0}}}}",
        "@keyframes pop{from{opacity:0;transform:scale(.2)}to{opacity:1;transform:scale(1)}}",
        "@keyframes fade{from{opacity:0}to{opacity:1}}",
        "@media (prefers-reduced-motion:reduce){*{animation:none!important}}",
        "</style>",
        card(theme, width, height),
        # Name and line, set as real text so it stays sharp at any size.
        f'<text x="32" y="74" font-size="12.5" font-weight="600" letter-spacing="1.6" fill="{theme["muted"]}">'
        "STATISTICS · KUALA LUMPUR</text>",
        f'<text x="31" y="118" font-size="38" font-weight="700" fill="{theme["ink"]}">Luqman Syahrulnizam</text>',
        f'<text x="32" y="153" font-size="17" fill="{theme["secondary"]}">I look for the residual:</text>',
        f'<text x="32" y="177" font-size="17" fill="{theme["secondary"]}">'
        "the part the headline doesn’t explain.</text>",
        # Recessive axes.
        f'<path d="M{left} {top - 6}V{bottom}H{right + 6}" fill="none" stroke="{theme["axis"]}" stroke-width="1"/>',
    ]

    for index, (x, y, residual) in enumerate(zip(xs, ys, residuals)):
        fitted = intercept + slope * x
        delay = 1.5 + index * 0.05
        colour = theme["accent"] if index == outlier else theme["secondary"]
        dash = "" if index == outlier else ' stroke-dasharray="2 3"'
        stroke = 2 if index == outlier else 1
        parts.append(
            f'<line class="res" style="animation-delay:{delay:.2f}s" x1="{px(x):.1f}" y1="{py(y):.1f}" '
            f'x2="{px(x):.1f}" y2="{py(fitted):.1f}" stroke="{colour}" stroke-width="{stroke}"{dash}/>'
        )

    parts.append(
        f'<line class="fit" x1="{px(0):.1f}" y1="{py(intercept):.1f}" x2="{px(1):.1f}" '
        f'y2="{py(intercept + slope):.1f}" stroke="{theme["ink"]}" stroke-width="2" stroke-linecap="round"/>'
    )

    for index, (x, y) in enumerate(zip(xs, ys)):
        colour = theme["accent"] if index == outlier else theme["series"]
        radius = 5.5 if index == outlier else 4.5
        parts.append(
            f'<circle class="dot" style="animation-delay:{0.25 + index * 0.06:.2f}s;'
            f'transform-origin:{px(x):.1f}px {py(y):.1f}px" cx="{px(x):.1f}" cy="{py(y):.1f}" r="{radius}" '
            f'fill="{colour}" stroke="{theme["surface"]}" stroke-width="2"/>'
        )

    # Direct label on the one highlighted point, so colour is not the only cue.
    label_x = px(xs[outlier]) + 11
    label_y = (py(ys[outlier]) + py(intercept + slope * xs[outlier])) / 2 - 2
    parts.append(
        f'<text class="note" x="{label_x:.1f}" y="{label_y:.1f}" font-size="13" '
        f'font-weight="600" fill="{theme["ink"]}">the residual</text>'
    )
    parts.append("</svg>")
    return "\n".join(parts)


def bar(x, y, length, thickness, radius):
    """A bar squared at the baseline and rounded at the data end."""
    radius = min(radius, length, thickness / 2)
    return (
        f"M{x:.1f} {y:.1f}h{length - radius:.1f}a{radius} {radius} 0 0 1 {radius} {radius}"
        f"v{thickness - 2 * radius:.1f}a{radius} {radius} 0 0 1 -{radius} {radius}h-{length - radius:.1f}z"
    )


def chart(theme, rows):
    """Share of graduates at or below RM2,500, one bar per field of study."""
    width = 880
    label_edge, plot_left, plot_right = 338, 350, 800
    top, row_height, thickness = 86, 30, 14
    plot_bottom = top + len(rows) * row_height
    height = plot_bottom + 78

    def px(share):
        return plot_left + share / 100 * (plot_right - plot_left)

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" '
        f'height="{height}" role="img" aria-labelledby="t d" font-family="{FONT}">',
        '<title id="t">Share of 2024 first-degree graduates earning RM2,500 a month or less, by field of study</title>',
        '<desc id="d">'
        + "; ".join(f"{name} {fmt(share)} per cent" for name, share in rows)
        + f". All first-degree graduates: {fmt(OVERALL_SHARE)} per cent.</desc>",
        card(theme, width, height),
        f'<text x="24" y="30" font-size="17" font-weight="700" fill="{theme["ink"]}">'
        "Who a RM2,500 graduate wage floor reaches</text>",
        f'<text x="24" y="52" font-size="13.5" fill="{theme["secondary"]}">'
        "Share of 2024 first-degree graduates earning RM2,500 a month or less, by field of study</text>",
    ]

    for tick in (0, 25, 50, 75, 100):
        colour = theme["axis"] if tick == 0 else theme["grid"]
        parts.append(
            f'<line x1="{px(tick):.1f}" y1="{top - 8}" x2="{px(tick):.1f}" y2="{plot_bottom}" '
            f'stroke="{colour}" stroke-width="1"/>'
        )
        parts.append(
            f'<text x="{px(tick):.1f}" y="{plot_bottom + 18}" text-anchor="middle" font-size="12" '
            f'fill="{theme["muted"]}">{tick}%</text>'
        )

    # The all-graduates figure as a reference line, labelled where it stands.
    x = px(OVERALL_SHARE)
    parts.append(
        f'<line x1="{x:.1f}" y1="{top - 8}" x2="{x:.1f}" y2="{plot_bottom}" stroke="{theme["ink"]}" '
        'stroke-width="1.5" stroke-dasharray="4 4"/>'
    )
    parts.append(
        f'<text x="{x + 6:.1f}" y="{top - 12}" font-size="12.5" font-weight="600" fill="{theme["ink"]}">'
        f"All first-degree graduates: {fmt(OVERALL_SHARE)}%</text>"
    )
    for index, (name, share) in enumerate(rows):
        y = top + index * row_height
        mine = name == MY_FIELD
        weight = "600" if mine else "400"
        parts.append(
            f'<text x="{label_edge}" y="{y + thickness / 2 + 4.5:.1f}" text-anchor="end" font-size="13" '
            f'font-weight="{weight}" fill="{theme["ink"] if mine else theme["secondary"]}">{name}</text>'
        )
        parts.append(
            f'<path d="{bar(plot_left, y, px(share) - plot_left, thickness, 4)}" '
            f'fill="{theme["accent"] if mine else theme["series"]}"/>'
        )
        note = "  ← my degree" if mine else ""
        parts.append(
            # The surface-coloured outline keeps the label legible where the
            # reference line passes behind it.
            f'<text x="{px(share) + 8:.1f}" y="{y + thickness / 2 + 4.5:.1f}" font-size="13" '
            f'font-weight="600" fill="{theme["ink"]}" stroke="{theme["surface"]}" stroke-width="5" '
            f'stroke-linejoin="round" paint-order="stroke" xml:space="preserve">{share:.1f}%'
            f'<tspan font-weight="400" fill="{theme["secondary"]}">{note}</tspan></text>'
        )

    parts.append(
        f'<text x="24" y="{plot_bottom + 46}" font-size="11.5" fill="{theme["muted"]}">'
        "Source: Kementerian Pendidikan Tinggi, Laporan Kajian Pengesanan Graduan 2024, Jadual 4o. "
        "Fields with 1,000 or more respondents.</text>"
    )
    parts.append(
        f'<text x="24" y="{plot_bottom + 62}" font-size="11.5" fill="{theme["muted"]}">'
        "Each field’s published income bands are rescaled to sum to 100% before adding the bands "
        "up to RM2,500.</text>"
    )
    parts.append("</svg>")
    return "\n".join(parts)


def main():
    with open(DATA, encoding="utf-8", newline="") as handle:
        rows = [(row["field"], float(row["share_at_or_below_rm2500"])) for row in csv.DictReader(handle)]
    rows.sort(key=lambda row: -row[1])

    ASSETS.mkdir(exist_ok=True)
    for name, theme in THEMES.items():
        (ASSETS / f"header-{name}.svg").write_text(header(theme), encoding="utf-8")
        (ASSETS / f"graduate-floor-{name}.svg").write_text(chart(theme, rows), encoding="utf-8")
        print(f"wrote {name} header and chart")


if __name__ == "__main__":
    main()
