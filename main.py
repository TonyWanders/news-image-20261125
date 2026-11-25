#!/usr/bin/env python3
# Entry for "Sum up 25 November's world news in one image".
# This script draws the finished picture with build_image.py (Pillow,
# fixed layout, no network, no clock, no random numbers) and writes it
# straight to the target: /output/entry.png (or a path given on the
# command line). It never writes into the repo directory, so it runs
# fine with the repo read-only. Every run writes exactly the same bytes.
import argparse
import os
import sys
from pathlib import Path

# The grader runs `python3 -P -s main.py`, and -P does not put this
# script's directory on sys.path, so a plain `import build_image`
# fails there. Put the script's own directory first explicitly.
sys.path.insert(0, str(Path(__file__).resolve().parent))

import build_image

PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


def run(target):
    target.parent.mkdir(parents=True, exist_ok=True)
    build_image.build(target)
    data = target.read_bytes()
    if not data.startswith(PNG_SIGNATURE):
        print("output is not a PNG", file=sys.stderr)
        return 1
    os.chmod(target, 0o644)
    print(f"wrote {target} ({len(data)} bytes)")
    return 0


def resolve_target(argv):
    parser = argparse.ArgumentParser(
        description="Draw the news image where the judge expects it."
    )
    parser.add_argument(
        "target",
        nargs="?",
        type=Path,
        default=Path("/output/entry.png"),
        help="where to write the entry (default: /output/entry.png)",
    )
    return parser.parse_args(argv[1:]).target


def main(argv):
    return run(resolve_target(argv))


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
