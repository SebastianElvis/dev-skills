#!/usr/bin/env python3
"""Render TikZ as Portable Document Format (PDF) and Scalable Vector Graphics (SVG) files."""

from __future__ import annotations

import argparse
import shutil
import subprocess
import xml.etree.ElementTree as ET
from pathlib import Path


def require_command(name: str) -> str:
    """Return the command path or stop with an actionable error."""
    path = shutil.which(name)
    if path is None:
        raise SystemExit(f"Install {name} before you render the diagram.")
    return path


def render(source: Path) -> tuple[Path, Path]:
    """Render the source and validate the Scalable Vector Graphics structure."""
    source = source.resolve()
    if source.suffix != ".tex" or not source.is_file():
        raise SystemExit(f"Give a TeX source file that exists: {source}")

    latexmk = require_command("latexmk")
    pdftocairo = require_command("pdftocairo")
    pdf = source.with_suffix(".pdf")
    svg = source.with_suffix(".svg")

    subprocess.run(
        [latexmk, "-pdf", "-interaction=nonstopmode", "-halt-on-error", source.name],
        cwd=source.parent,
        check=True,
    )
    subprocess.run(
        [pdftocairo, "-svg", pdf.name, svg.name],
        cwd=source.parent,
        check=True,
    )
    ET.parse(svg)
    subprocess.run([latexmk, "-c", source.name], cwd=source.parent, check=True)
    return pdf, svg


def main() -> None:
    """Read the source path and print each generated file."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    args = parser.parse_args()
    pdf, svg = render(args.source)
    print(pdf)
    print(svg)


if __name__ == "__main__":
    main()
