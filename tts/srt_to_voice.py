#!/usr/bin/env python3
"""SRT -> narration audio with one fixed channel voice (Kokoro-82M, local).

Usage:
  srt_to_voice.py <video_dir | file.srt> [--mux] [--voice V] [--speed S] [--out DIR]

With a video folder (videos/NNN-slug/) it reads dialogue.srt, writes
audio/<segment_id>.wav per cue (ids from dialogue.json) plus audio/narration.wav
(all clips placed at their SRT start times), and with --mux combines the
narration with <slug>.mp4 into <slug>_narrated.mp4.

The voice, speed and loudness come from tts/voice.json so every video sounds the
same. A clip longer than its cue is re-spoken faster (up to max_speed); if it
still does not fit, a warning tells you which segment to lengthen.
"""

import argparse
import json
import pathlib
import re
import subprocess
import sys
import warnings

import numpy as np
import soundfile as sf

warnings.filterwarnings("ignore")
ROOT = pathlib.Path(__file__).resolve().parent
CONFIG = json.loads((ROOT / "voice.json").read_text())


def parse_time(t):
    h, m, rest = t.strip().split(":")
    s, ms = rest.replace(".", ",").split(",")
    return int(h) * 3600 + int(m) * 60 + int(s) + int(ms) / 1000


def parse_srt(path):
    cues = []
    for block in re.split(r"\n\s*\n", path.read_text(encoding="utf-8").strip()):
        lines = [l for l in block.strip().splitlines() if l.strip()]
        if len(lines) < 2 or "-->" not in lines[1]:
            continue
        a, b = lines[1].split("-->")
        cues.append({"start": parse_time(a), "end": parse_time(b), "text": " ".join(lines[2:]).strip()})
    return cues


def prepare(text):
    for rule in CONFIG.get("pronunciations", []):
        text = re.sub(rule["pattern"], rule["replace"], text)
    return text


class Voice:
    def __init__(self, voice, speed):
        from kokoro import KPipeline
        self.pipe = KPipeline(lang_code=CONFIG["lang_code"], repo_id=CONFIG["model"])
        self.voice, self.speed = voice, speed
        self.sr = CONFIG["sample_rate"]

    def say(self, text, speed=None):
        parts = [r.audio.numpy() for r in self.pipe(prepare(text), voice=self.voice,
                                                     speed=speed or self.speed) if r.audio is not None]
        audio = np.concatenate(parts) if parts else np.zeros(1, dtype=np.float32)
        return level(trim(audio, self.sr))


def trim(audio, sr, thresh=1e-3, pad=0.05):
    idx = np.where(np.abs(audio) > thresh)[0]
    if len(idx) == 0:
        return audio
    p = int(pad * sr)
    return audio[max(0, idx[0] - p): idx[-1] + p]


def level(audio):
    rms = np.sqrt(np.mean(audio ** 2)) or 1.0
    gain = 10 ** (CONFIG["target_rms_dbfs"] / 20) / rms
    out = audio * gain
    peak = np.max(np.abs(out))
    return out / peak * 0.98 if peak > 0.98 else out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("target")
    ap.add_argument("--mux", action="store_true", help="combine narration with the video folder's MP4")
    ap.add_argument("--voice", default=CONFIG["voice"])
    ap.add_argument("--speed", type=float, default=CONFIG["speed"])
    ap.add_argument("--out", help="output folder (default: <video_dir>/audio or next to the SRT)")
    args = ap.parse_args()

    target = pathlib.Path(args.target).resolve()
    vdir = target if target.is_dir() else None
    srt = target / "dialogue.srt" if vdir else target
    if not srt.exists():
        sys.exit(f"error: {srt} not found")
    out = pathlib.Path(args.out).resolve() if args.out else (vdir / "audio" if vdir else srt.parent / f"{srt.stem}_audio")
    out.mkdir(parents=True, exist_ok=True)

    cues = parse_srt(srt)
    ids = None
    if vdir and (vdir / "dialogue.json").exists():
        ids = [d["id"] for d in json.loads((vdir / "dialogue.json").read_text())]
        if len(ids) != len(cues):
            ids = None

    v = Voice(args.voice, args.speed)
    sr = v.sr
    total = max(c["end"] for c in cues)
    track = np.zeros(int(np.ceil(total * sr)) + sr, dtype=np.float32)
    problems = []
    for i, c in enumerate(cues):
        name = ids[i] if ids else f"cue_{i + 1:03d}"
        slot = c["end"] - c["start"]
        speed = args.speed
        audio = v.say(c["text"], speed)
        while len(audio) / sr > slot - 0.1 and speed < CONFIG["max_speed"] - 1e-6:
            speed = min(CONFIG["max_speed"], speed * len(audio) / sr / (slot - 0.2))
            audio = v.say(c["text"], speed)
        dur = len(audio) / sr
        flag = ""
        if dur > slot:
            flag = "  <-- TOO LONG: lengthen this segment"
            problems.append(name)
        elif speed != args.speed:
            flag = f"  (sped up to {speed:.2f})"
        print(f"{name:<22} {dur:5.2f}s / slot {slot:5.2f}s{flag}")
        sf.write(out / f"{name}.wav", audio, sr)
        s = int(c["start"] * sr)
        track[s:s + len(audio)] += audio[: len(track) - s]
    track = track[: int(np.ceil(total * sr))]
    sf.write(out / "narration.wav", track, sr)
    print(f"wrote {len(cues)} clips + narration.wav ({total:.1f}s) to {out}")
    if problems:
        print("warning: clips longer than their slot:", ", ".join(problems))

    if args.mux:
        if not vdir:
            sys.exit("error: --mux needs a video folder")
        slug = json.loads((vdir / "timeline.json").read_text())["slug"]
        vid = vdir / f"{slug}.mp4"
        if not vid.exists():
            sys.exit(f"error: {vid} not found (render the video first)")
        res = vdir / f"{slug}_narrated.mp4"
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(vid), "-i", str(out / "narration.wav"),
                        "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
                        "-shortest", str(res)], check=True)
        print(f"wrote {res}")


if __name__ == "__main__":
    main()
