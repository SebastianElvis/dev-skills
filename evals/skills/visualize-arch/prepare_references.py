#!/usr/bin/env python3
"""This script caches authorized reference images outside the distributed skill."""

import argparse
import base64
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
import urllib.request

from PIL import Image

REVISION = "420b229ceaafed446bffd5504d877cbc92a6b6e4"


def prepare(output: Path) -> None:
    """This function downloads pinned references and records their sources."""
    output.mkdir(parents=True, exist_ok=True)
    records = []
    for name in ["system-architecture", "data-model", "submission-lifecycle"]:
        path = f"docs/assets/{name}.png"
        response = subprocess.run(["gh", "api", f"repos/SebastianElvis/kriterion/contents/{path}?ref={REVISION}"],
                                  capture_output=True, text=True, check=True)
        data = base64.b64decode(json.loads(response.stdout)["content"])
        target = output / "kriterion" / f"{name}.png"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
        records.append({"path": str(target.relative_to(output)), "source": f"https://github.com/SebastianElvis/kriterion/blob/{REVISION}/{path}",
                        "sha256": hashlib.sha256(data).hexdigest()})
    sources = [
        ("mooncake", "https://www.usenix.org/system/files/fast25-qin.pdf", 3, (125, 95, 815, 489)),
        ("ray", "https://www.usenix.org/system/files/osdi18-moritz.pdf", 9, (105, 98, 459, 506)),
    ]
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        for name, url, page, box in sources:
            pdf = root / f"{name}.pdf"
            pdf.write_bytes(urllib.request.urlopen(url, timeout=60).read())
            prefix = root / name
            subprocess.run(["pdftoppm", "-f", str(page), "-l", str(page), "-r", "220", "-png", "-singlefile", str(pdf), str(prefix)], check=True)
            target = output / "public/crops" / f"{name}-page-{page}.png"
            target.parent.mkdir(parents=True, exist_ok=True)
            with Image.open(prefix.with_suffix(".png")) as picture:
                picture.crop(tuple(x * 2 for x in box)).save(target)
            records.append({"path": str(target.relative_to(output)), "source": url, "page": page,
                            "sha256": hashlib.sha256(target.read_bytes()).hexdigest()})
    (output / "reference-sources.json").write_text(json.dumps(records, indent=2) + "\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    prepare(parser.parse_args().output)
