#!/usr/bin/env python3
"""make.fun bounty news-image-20261122 (v2).

Copies the bundled editorial poster to /output/entry.png.
No network, no randomness, no timestamps: two runs write identical bytes.
"""
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "assets", "entry.png")
DST = "/output/entry.png"


def main() -> int:
    os.makedirs(os.path.dirname(DST), exist_ok=True)
    shutil.copyfile(SRC, DST)
    return 0


if __name__ == "__main__":
    sys.exit(main())
