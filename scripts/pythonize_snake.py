#!/usr/bin/env python3
"""Turn the Platane/snk snake into the Python-logo snake and drop the bar.

Works on snk's svg-only output: every snake segment is a `<rect class="s sN">`
driven by its own CSS keyframes, and the eaten-cells progress bar is a row of
`<rect class="u uN">` under the grid.

  * front half of the body Python blue, back half Python yellow
  * one white eye on the head (a circle sharing the head's classes, so it
    inherits the head's animation)
  * --no-bar: remove the progress bar and crop the empty space under the grid

Usage: pythonize_snake.py [--no-bar] SVG...
Idempotent: a file that already carries the eye is left untouched.
"""
import argparse
import pathlib
import re

BLUE, YELLOW, EYE = "#3776AB", "#FFD43B", "#FFFFFF"
EYE_SHAPE = '<circle class="s s0 eye" cx="10.8" cy="5.4" r="1.9"/>'
CELL = 16  # snk cell pitch


def pythonize(svg: str, no_bar: bool) -> str:
    if ".eye{" in svg:
        return svg
    segs = sorted({int(n) for n in re.findall(r'class="s s(\d+)"', svg)})
    if not segs or "</style>" not in svg:
        raise SystemExit("not an snk svg-only snake file")
    half = (len(segs) + 1) // 2
    css = (",".join(f".s{n}" for n in segs[:half]) + f"{{fill:{BLUE}}}"
           + ",".join(f".s{n}" for n in segs[half:]) + f"{{fill:{YELLOW}}}.eye{{fill:{EYE}}}")

    if no_bar:
        svg = re.sub(r'<rect class="u u[0-9a-z]+"[^>]*/>', "", svg)
        svg = re.sub(r"@keyframes u[0-9a-z]+\{.*?\}\}", "", svg)          # keyframe blocks
        svg = re.sub(r"\.u(?:\.u[0-9a-z]+|[0-9a-z]*)\{[^}]*\}", "", svg)  # .u / .uN / .u.uN rules
        vb = re.search(r'viewBox="(-?[0-9.]+) (-?[0-9.]+) ([0-9.]+) ([0-9.]+)"', svg)
        x0, y0, w, _ = map(float, vb.groups())
        h = 7 * CELL + CELL - y0                                          # grid + one cell of air
        svg = svg.replace(vb.group(0), f'viewBox="{x0:g} {y0:g} {w:g} {h:g}"', 1)
        svg = re.sub(r'\bheight="[0-9.]+"(?=[^>]*xmlns)', f'height="{h:g}"', svg, count=1)

    svg = svg.replace("</style>", css + "</style>", 1)
    head = re.search(r'<rect class="s s0"[^>]*/>', svg)
    return svg[: head.end()] + EYE_SHAPE + svg[head.end():]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--no-bar", action="store_true")
    ap.add_argument("svgs", nargs="+", type=pathlib.Path)
    a = ap.parse_args()
    for path in a.svgs:
        path.write_text(pythonize(path.read_text(encoding="utf-8"), a.no_bar), encoding="utf-8")
        print("pythonized", path, "(bar removed)" if a.no_bar else "")


if __name__ == "__main__":
    main()
