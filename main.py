#!/usr/bin/env python3
"""news-image-20261118 entrypoint (Python 3.13, standard library only).

Writes the 18 November 2026 world-news front page to /output/entry.png.
The image itself is drawn by draw_news.py (Pillow, offline) and shipped as
entry.png beside this file; this program only copies it, so both graded
runs write byte-identical output. Outside the grader, MAKEFUN_OUTPUT_DIR
stands in for /output:

    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""

import hashlib
import os
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "entry.png"


def main() -> None:
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    dest = out_dir / "entry.png"
    # Copy, never re-render: the shipped PNG is the graded artifact, so
    # both runs produce exactly the same bytes.
    shutil.copyfile(SOURCE, dest)
    data = dest.read_bytes()
    assert data[:8] == b"\x89PNG\r\n\x1a\n", "entry.png is not a PNG"
    assert len(data) <= 1_048_576, "entry.png exceeds the 1 MiB gate"
    digest = hashlib.sha256(data).hexdigest()
    print(f"wrote {dest} ({len(data)} bytes, sha256 {digest})")


if __name__ == "__main__":
    main()
