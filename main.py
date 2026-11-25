#!/usr/bin/env python3
# Entry for "Sum up 25 November's world news in one image".
#
# The grader runs this program with standard library only: nothing is
# installed before it runs, so it cannot import Pillow here. The image
# itself lives in this repository as entry.png (drawn with Pillow by
# build_image.py at build time), and this program just copies it to the
# target: /output/entry.png (or a path given on the command line, or
# $MAKEFUN_OUTPUT_DIR/entry.png). It never writes into the repo
# directory, so it runs fine with the repo read-only. Every run writes
# exactly the same bytes.
import argparse
import os
import shutil
import sys
from pathlib import Path

PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


def run(target):
    src = Path(__file__).resolve().parent / "entry.png"
    if not src.is_file():
        print(f"missing source image: {src}", file=sys.stderr)
        return 1
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(src, target)
    data = target.read_bytes()
    if not data.startswith(PNG_SIGNATURE):
        print("output is not a PNG", file=sys.stderr)
        return 1
    os.chmod(target, 0o644)
    print(f"wrote {target} ({len(data)} bytes)")
    return 0


def resolve_target(argv):
    parser = argparse.ArgumentParser(
        description="Copy the news image where the judge expects it."
    )
    parser.add_argument(
        "target",
        nargs="?",
        type=Path,
        default=None,
        help="where to write the entry (default: $MAKEFUN_OUTPUT_DIR/entry.png or /output/entry.png)",
    )
    target = parser.parse_args(argv[1:]).target
    if target is None:
        out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
        target = Path(out_dir) / "entry.png"
    return target


def main(argv):
    return run(resolve_target(argv))


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
