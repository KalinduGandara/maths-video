#!/usr/bin/env python3
"""Static theme-compliance check for a video's scene.py.

Usage:
  theme_lint.py <video_dir>

ERROR (exit 1): hard-coded colours (hex, rgb, manim colour constants), hard-coded
font names, background changes. These must come from theme/theme.py tokens.
warn: literal font sizes, attention-grabbing animations that break the calm
professional style, and exclamation marks in on-screen text or the title.
"""

import json
import pathlib
import re
import sys

BASE = r"(?:WHITE|BLACK|RED|BLUE|GREEN|YELLOW|ORANGE|PURPLE|PINK|GRAY|GREY|TEAL|GOLD|MAROON|LIGHT_\w+|DARK_\w+|PURE_\w+)"
COLOUR_CONST = re.compile(rf"(?<![\w.]){BASE}(?:_[A-E])?(?!\w)")
ERRORS = [
    (re.compile(r"['\"]#[0-9a-fA-F]{3,8}['\"]"), "hex colour; use a theme colour role"),
    (COLOUR_CONST, "manim colour constant; use a theme colour role"),
    (re.compile(r"\b(?:rgb_to_color|rgba_to_color|ManimColor)\s*\("), "custom colour; use a theme colour role"),
    (re.compile(r"\bfont\s*=\s*['\"]"), "font name literal; use FONT_HEADING / FONT_BODY / FONT_MONO"),
    (re.compile(r"background_color"), "background is set by the theme"),
]
WARNS = [
    (re.compile(r"\bfont_size\s*=\s*\d"), "literal font size; prefer SIZE_* tokens"),
    (re.compile(r"\b(?:SpinInFromNothing|Wiggle|ApplyWave|WiggleOutThenIn|Rotating|TurnInsideOut)\b"),
     "showy animation; the style is calm and professional"),
    (re.compile(r"FadeIn\([^)]*scale\s*=\s*(?:1\.[2-9]|[2-9])"), "zoom-punch entrance; keep entrances calm"),
    (re.compile(r"(?:Text|Tex|caption|body|heading|tag)\(\s*r?['\"][^'\"]*!"), "exclamation mark in on-screen text"),
]


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    d = pathlib.Path(sys.argv[1]).resolve()
    scene = d / "scene.py"
    errors, warns = [], []
    for n, line in enumerate(scene.read_text().splitlines(), 1):
        code = line.split("#", 1)[0] if not re.search(r"['\"]#", line) else line
        for rx, msg in ERRORS:
            if rx.search(code):
                errors.append(f"scene.py:{n}: {msg}: {line.strip()}")
        for rx, msg in WARNS:
            if rx.search(code):
                warns.append(f"scene.py:{n}: {msg}: {line.strip()}")
    tl = d / "timeline.json"
    if tl.exists() and "!" in json.loads(tl.read_text()).get("title", ""):
        warns.append("timeline.json: title has an exclamation mark; titles are plain and descriptive")
    for w in warns:
        print("warn: ", w)
    for e in errors:
        print("ERROR:", e)
    print(f"{len(errors)} errors, {len(warns)} warnings")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
