#!/usr/bin/env python3
"""Entry program for make.fun's "Sum up 22 November's world news in one image".

The repository ships the finished poster as entry.png, drawn for this contest
in the build session recorded in the transcripts. The grader's container has
no network and nothing is installed before the run, so this program does the
whole job with the standard library alone: it proves the shipped file is a
whole PNG or JPEG inside the gate's size limit, then copies it, byte for
byte, to /output/entry.png (MAKEFUN_OUTPUT_DIR stands in for /output when
run locally). Same input file, same output bytes, every run.
"""

import os
import shutil
import sys

MAX_BYTES = 1_048_576  # the gate's cap: 1 MiB
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
JPEG_SIGNATURE = b"\xff\xd8\xff"


def main() -> int:
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, "entry.png")

    with open(source, "rb") as fh:
        head = fh.read(8)
        fh.seek(-12, os.SEEK_END)
        tail = fh.read(12)
    if head.startswith(PNG_SIGNATURE):
        # a whole PNG ends with the IEND chunk: length 0, "IEND", its CRC
        if not tail.endswith(b"IEND\xaeB\x60\x82"):
            print("entry.png is a PNG but looks truncated", file=sys.stderr)
            return 1
    elif head.startswith(JPEG_SIGNATURE):
        if not tail.endswith(b"\xff\xd9"):
            print("entry.png is a JPEG but looks truncated", file=sys.stderr)
            return 1
    else:
        print("entry.png is neither a PNG nor a JPEG", file=sys.stderr)
        return 1

    size = os.path.getsize(source)
    if size > MAX_BYTES:
        print(f"entry.png is {size} bytes, over the 1 MiB gate limit",
              file=sys.stderr)
        return 1

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, "entry.png")
    shutil.copyfile(source, target)
    print(f"wrote {target} ({size} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
