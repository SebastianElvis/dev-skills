#!/usr/bin/env python3
"""This script caches authorized reference images outside the distributed skill."""

import argparse
import base64
import hashlib
import json
from pathlib import Path
import subprocess


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
    (output / "reference-sources.json").write_text(json.dumps(records, indent=2) + "\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    prepare(parser.parse_args().output)
