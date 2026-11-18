#!/usr/bin/env python3
"""Check Portable Document Format (PDF) text at the final width. Create color and grayscale previews."""

from __future__ import annotations

import argparse
import json
import math
import shutil
import subprocess
import xml.etree.ElementTree as ET
from pathlib import Path


def command(name: str) -> str:
    """Find a required command."""
    executable = shutil.which(name)
    if executable is None:
        raise RuntimeError(f"Install {name} before you check the figure.")
    return executable


def inspect(xml: str, width_mm: float, min_text_pt: float) -> dict:
    """Measure text after scaling to the requested width."""
    root = ET.fromstring(xml)
    pages = root.findall("page")
    if len(pages) != 1:
        raise ValueError("Give a PDF with exactly one page.")
    page = pages[0]
    width = float(page.attrib["width"])
    height = float(page.attrib["height"])
    if width <= 0 or height <= 0 or width_mm <= 0 or min_text_pt <= 0:
        raise ValueError("Use positive dimensions and text sizes.")
    scale = width_mm * 72 / 25.4 / width
    fonts = {f.attrib["id"]: float(f.attrib["size"]) for f in page.findall("fontspec")}
    labels = [t for t in page.findall("text") if "".join(t.itertext()).strip()]
    if not labels:
        raise ValueError("The PDF has no inspectable text.")
    minimum = min(fonts[t.attrib["font"]] * scale for t in labels)
    bounds = []
    outside = []
    for t in labels:
        x, y, w, h = (float(t.attrib[k]) for k in ("left", "top", "width", "height"))
        bounds.append((x, y, x + w, y + h))
        if x < -1 or y < -1 or x + w > width + 1 or y + h > height + 1:
            outside.append("".join(t.itertext()).strip())
    collisions = []
    for i, a in enumerate(bounds):
        for j in range(i + 1, len(bounds)):
            b = bounds[j]
            dx = min(a[2], b[2]) - max(a[0], b[0])
            dy = min(a[3], b[3]) - max(a[1], b[1])
            if dx > 1 and dy > 1:
                collisions.append([i, j])
    return {
        "width_mm": width_mm,
        "effective_min_text_pt": round(minimum, 2),
        "required_min_text_pt": min_text_pt,
        "text_size_pass": minimum >= min_text_pt - 0.15,
        "bounds_pass": not outside,
        "outside_labels": outside,
        "possible_text_collisions": collisions,
        "measurement_note": "Poppler rounds font sizes. A visual review must check collisions and glyphs.",
    }


def check(pdf: Path, width_mm: float, min_text_pt: float, preview_dir: Path | None = None) -> dict:
    """Inspect a PDF and render its previews."""
    pdf = pdf.resolve(strict=True)
    if not math.isfinite(width_mm) or not math.isfinite(min_text_pt) or width_mm <= 0 or min_text_pt <= 0:
        raise ValueError("Use positive finite dimensions and text sizes.")
    result = subprocess.run(
        [command("pdftohtml"), "-xml", "-zoom", "10", "-hidden", "-stdout", str(pdf)],
        capture_output=True, text=True, check=True,
    )
    report = inspect(result.stdout, width_mm, min_text_pt)
    directory = preview_dir or pdf.parent
    directory.mkdir(parents=True, exist_ok=True)
    pixels = str(round(width_mm / 25.4 * 150))
    for mode in ("color", "gray"):
        prefix = directory / f"{pdf.stem}-{mode}"
        args = [command("pdftoppm"), "-png", "-singlefile", "-scale-to-x", pixels, "-scale-to-y", "-1"]
        if mode == "gray":
            args.append("-gray")
        subprocess.run([*args, str(pdf), str(prefix)], capture_output=True, check=True)
        report[f"{mode}_preview"] = str(prefix.with_suffix(".png"))
    return report


def main() -> None:
    """Print measurements and return a failure status for invalid figures."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pdf", type=Path)
    parser.add_argument("--width-mm", type=float, required=True)
    parser.add_argument("--min-text-pt", type=float, default=8)
    parser.add_argument("--preview-dir", type=Path)
    args = parser.parse_args()
    try:
        report = check(args.pdf, args.width_mm, args.min_text_pt, args.preview_dir)
    except (OSError, ValueError, ET.ParseError, subprocess.CalledProcessError, RuntimeError) as error:
        parser.exit(1, f"The figure check failed: {error}\n")
    print(json.dumps(report, indent=2))
    raise SystemExit(0 if report["text_size_pass"] and report["bounds_pass"] else 1)


if __name__ == "__main__":
    main()
