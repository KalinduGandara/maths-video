#!/usr/bin/env python3
"""SRT -> narration audio with one fixed channel voice (Kokoro-82M, local).

Usage:
  srt_to_voice.py <video_dir | file.srt> [--mux] [--voice V] [--speed S] [--out DIR]

With a video folder (videos/NNN-slug/) it reads dialogue.srt and writes:
  audio/<segment_id>.wav   one clip per cue (ids from dialogue.json)
  audio/narration.wav      all clips placed at their SRT start times
  voice_timing.json        per segment: clip length, every spoken word with its
                           start/end time from the segment start, and the phonemes.
                           ThemedScene.cue() uses it to lock animations to words,
                           and `timeline_tool.py fit` uses it to size segments.
With --mux it also combines narration.wav with <slug>.mp4 into <slug>_narrated.mp4.

Every clip is spoken at the channel speed from tts/voice.json, never sped up.
A clip longer than its slot is reported; fix it with `timeline_tool.py fit`.
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

    def say(self, text):
        """Returns (audio, words, phonemes); word times are seconds from the clip start."""
        parts, words, phonemes, offset = [], [], [], 0.0
        for r in self.pipe(prepare(text), voice=self.voice, speed=self.speed):
            if r.audio is None:
                continue
            a = r.audio.numpy()
            for t in r.tokens or []:
                if t.start_ts is not None and re.search(r"\w", t.text):
                    words.append({"word": t.text, "start": offset + t.start_ts,
                                  "end": offset + (t.end_ts or t.start_ts), "phonemes": t.phonemes})
            phonemes.append(r.phonemes)
            parts.append(a)
            offset += len(a) / self.sr
        audio = np.concatenate(parts) if parts else np.zeros(1, dtype=np.float32)
        audio, lead = trim(audio, self.sr)
        for w in words:
            w["start"] = max(0.0, w["start"] - lead)
            w["end"] = max(0.0, w["end"] - lead)
        return level(audio), words, " ".join(phonemes)


def trim(audio, sr, thresh=1e-3, pad=0.05):
    """Cut leading/trailing silence. Returns (audio, seconds removed from the front)."""
    idx = np.where(np.abs(audio) > thresh)[0]
    if len(idx) == 0:
        return audio, 0.0
    a = max(0, idx[0] - int(pad * sr))
    return audio[a: idx[-1] + int(pad * sr)], a / sr


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
    timing, problems = {}, []
    for i, c in enumerate(cues):
        name = ids[i] if ids else f"cue_{i + 1:03d}"
        slot = c["end"] - c["start"]
        audio, words, phonemes = v.say(c["text"])
        dur = len(audio) / sr
        flag = ""
        if dur > slot:
            flag = "  <-- TOO LONG: run timeline_tool.py fit"
            problems.append(name)
        print(f"{name:<22} {dur:5.2f}s / slot {slot:5.2f}s{flag}")
        sf.write(out / f"{name}.wav", audio, sr)
        s = int(c["start"] * sr)
        track[s:s + len(audio)] += audio[: len(track) - s]
        timing[name] = {
            "start": c["start"], "clip": round(dur, 3), "text": c["text"], "phonemes": phonemes,
            "words": [{"word": w["word"], "start": round(w["start"], 3), "end": round(w["end"], 3),
                       "phonemes": w["phonemes"]} for w in words],
        }
    track = track[: int(np.ceil(total * sr))]
    sf.write(out / "narration.wav", track, sr)
    print(f"wrote {len(cues)} clips + narration.wav ({total:.1f}s) to {out}")
    if vdir:
        meta = {"voice": args.voice, "speed": args.speed, "segments": timing}
        (vdir / "voice_timing.json").write_text(json.dumps(meta, indent=1, ensure_ascii=False) + "\n")
        print(f"wrote {vdir / 'voice_timing.json'}")
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
