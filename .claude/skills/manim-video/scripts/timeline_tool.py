#!/usr/bin/env python3
"""Timeline helper for manim-video projects.

Usage:
  timeline_tool.py check  <video_dir>   validate timeline.json (and narration fit, once voiced)
  timeline_tool.py retime <video_dir>   make segments contiguous & long enough for their words
  timeline_tool.py export <video_dir>   write dialogue.srt / .txt / .json and chapters.txt
  timeline_tool.py fit    <video_dir>   grow segments to the real clip lengths in voice_timing.json
  timeline_tool.py verify <video_dir>   compare rendered <slug>.mp4 length with the timeline
  timeline_tool.py frames <video_dir>   extract review stills (mid + end of every segment)
  timeline_tool.py mux    <video_dir>   place audio/ clips at segment starts -> narration.wav + _narrated.mp4
"""

import json
import math
import pathlib
import re
import shutil
import subprocess
import sys

PAD = 0.8  # seconds of slack required beyond pure speaking time
TAIL = 0.6  # seconds of silence kept after a voiced clip before the next segment
AUDIO_EXTS = (".wav", ".mp3", ".m4a", ".aac", ".flac", ".ogg")


def load(d):
    path = d / "timeline.json"
    if not path.exists():
        sys.exit(f"error: {path} not found")
    return path, json.loads(path.read_text())


def words(text):
    return len(re.findall(r"[A-Za-z0-9']+", text or ""))


def needed(seg, wps):
    w = words(seg.get("dialogue", ""))
    return 0.0 if w == 0 else w / wps + PAD


def fmt(t, sep=","):
    ms = int(round(t * 1000))
    h, ms = divmod(ms, 3_600_000)
    m, ms = divmod(ms, 60_000)
    s, ms = divmod(ms, 1000)
    return f"{h:02}:{m:02}:{s:02}{sep}{ms:03}"


def short(t):
    m, s = divmod(t, 60)
    return f"{int(m):02}:{s:06.3f}"


def voice_timing(d):
    p = d / "voice_timing.json"
    return json.loads(p.read_text())["segments"] if p.exists() else {}


def check(d):
    _, tl = load(d)
    segs = tl.get("segments", [])
    voiced = voice_timing(d)
    wps = tl.get("words_per_second", 2.5)
    errors, warns = [], []
    if not segs:
        errors.append("no segments")
    seen, prev_end = set(), 0.0
    for i, s in enumerate(segs):
        sid = s.get("id", f"#{i}")
        for k in ("id", "start", "end", "dialogue", "animation"):
            if k not in s:
                errors.append(f"{sid}: missing '{k}'")
        if sid in seen:
            errors.append(f"{sid}: duplicate id")
        seen.add(sid)
        if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", str(sid)):
            errors.append(f"{sid}: id must be a valid Python identifier suffix")
        start, end = s.get("start", 0), s.get("end", 0)
        if abs(start - prev_end) > 1e-6:
            errors.append(f"{sid}: starts at {start} but previous ends at {prev_end} (gap/overlap)")
        if end <= start:
            errors.append(f"{sid}: end ({end}) must be after start ({start})")
        v = voiced.get(sid)
        need = needed(s, wps)
        if not v and end - start + 1e-6 < need:
            errors.append(f"{sid}: {words(s.get('dialogue'))} words need ≥{need:.1f}s, slot is {end - start:.1f}s")
        if re.search(r"[\\$^_{}]", s.get("dialogue", "")):
            warns.append(f"{sid}: dialogue contains LaTeX-like characters; write maths as spoken words")
        if v and v["text"] != s.get("dialogue", "").strip():
            errors.append(f"{sid}: dialogue changed since it was voiced; re-run tts/srt_to_voice.py")
        elif v and v["clip"] + TAIL > end - start + 1e-6:
            errors.append(f"{sid}: voice clip {v['clip']:.2f}s + {TAIL}s tail exceeds slot "
                          f"{end - start:.2f}s; run `fit`")
        if end - start > 25:
            warns.append(f"{sid}: {end - start:.1f}s is long; consider splitting")
        prev_end = end
    total = segs[-1]["end"] if segs else 0
    spoken = sum(words(s.get("dialogue")) for s in segs)
    for w in warns:
        print("warn: ", w)
    for e in errors:
        print("ERROR:", e)
    print(f"{len(segs)} segments, {spoken} words, total {short(total)} ({total:.1f}s)")
    if errors:
        sys.exit(1)
    print("OK")


def retime(d):
    path, tl = load(d)
    wps = tl.get("words_per_second", 2.5)
    t = 0.0
    for s in tl["segments"]:
        dur = max(s.get("end", 0) - s.get("start", 0), needed(s, wps), 1.0)
        dur = math.ceil(dur * 2) / 2  # round up to 0.5s
        s["start"], s["end"] = round(t, 3), round(t + dur, 3)
        t += dur
    path.write_text(json.dumps(tl, indent=2, ensure_ascii=False) + "\n")
    print(f"retimed {len(tl['segments'])} segments, total {short(t)}")


def export(d):
    _, tl = load(d)
    spoken = [s for s in tl["segments"] if s.get("dialogue", "").strip()]
    srt, txt, js = [], [], []
    for n, s in enumerate(spoken, 1):
        text = s["dialogue"].strip()
        srt.append(f"{n}\n{fmt(s['start'])} --> {fmt(s['end'])}\n{text}\n")
        txt.append(f"[{short(s['start'])} - {short(s['end'])}] {text}")
        js.append({"id": s["id"], "start": s["start"], "end": s["end"],
                   "duration": round(s["end"] - s["start"], 3), "text": text})
    (d / "dialogue.srt").write_text("\n".join(srt), encoding="utf-8")
    header = f"# {tl.get('title', '')} — narration (total {short(tl['segments'][-1]['end'])})\n"
    (d / "dialogue.txt").write_text(header + "\n".join(txt) + "\n", encoding="utf-8")
    (d / "dialogue.json").write_text(json.dumps(js, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote dialogue.srt / dialogue.txt / dialogue.json ({len(spoken)} lines)")
    chapters = [(s["start"], s["chapter"]) for s in tl["segments"] if s.get("chapter")]
    if chapters:
        if chapters[0][0] != 0:
            print("warn: the first chapter must start at 0:00 (put a chapter on the first segment)")
        lines = [f"{int(t // 60)}:{int(t % 60):02} {name}" for t, name in chapters]
        (d / "chapters.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
        print(f"wrote chapters.txt ({len(chapters)} chapters)")


def fit(d):
    """Make every voiced segment at least clip + TAIL long, then shift later segments."""
    path, tl = load(d)
    voiced = voice_timing(d)
    if not voiced:
        sys.exit("error: voice_timing.json not found; run tts/srt_to_voice.py first")
    t, grown = 0.0, []
    for s in tl["segments"]:
        dur = s["end"] - s["start"]
        v = voiced.get(s["id"])
        if v and v["clip"] + TAIL > dur:
            dur = math.ceil((v["clip"] + TAIL) * 2) / 2
            grown.append(f"{s['id']} -> {dur:.1f}s")
        s["start"], s["end"] = round(t, 3), round(t + dur, 3)
        t += dur
    path.write_text(json.dumps(tl, indent=2, ensure_ascii=False) + "\n")
    print("grew: " + (", ".join(grown) if grown else "nothing, every clip already fits"))
    print(f"total {short(t)}")
    export(d)


def probe(path):
    if not shutil.which("ffprobe"):
        sys.exit("error: ffprobe not found (brew install ffmpeg)")
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)],
        capture_output=True, text=True, check=True)
    return float(out.stdout.strip())


def video_path(d, tl):
    p = d / f"{tl.get('slug', d.name)}.mp4"
    if not p.exists():
        cands = sorted(d.glob("*.mp4"))
        cands = [c for c in cands if not c.stem.endswith("_narrated")]
        if not cands:
            sys.exit(f"error: no rendered mp4 in {d}")
        p = cands[0]
    return p


def verify(d):
    _, tl = load(d)
    vid = video_path(d, tl)
    actual, expected = probe(vid), tl["segments"][-1]["end"]
    diff = actual - expected
    print(f"{vid.name}: {actual:.2f}s, timeline {expected:.2f}s, diff {diff:+.2f}s")
    if abs(diff) > 0.5:
        sys.exit("ERROR: video length does not match timeline")
    print("OK")


def frames(d):
    _, tl = load(d)
    vid = video_path(d, tl)
    out = d / "review" / "frames"
    out.mkdir(parents=True, exist_ok=True)
    for old in out.glob("*.png"):
        old.unlink()
    for s in tl["segments"]:
        for tag, t in (("mid", (s["start"] + s["end"]) / 2), ("end", s["end"] - 0.25)):
            subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", f"{t:.3f}", "-i", str(vid),
                            "-frames:v", "1", "-vf", "scale=960:-2", str(out / f"{s['id']}_{tag}.png")],
                           check=True)
    print(f"wrote {2 * len(tl['segments'])} stills to {out}")


def mux(d):
    """Per-segment clips win over a single narration file, because they follow
    the current timeline; a single file is laid at 0:00 unchanged."""
    _, tl = load(d)
    vid = video_path(d, tl)
    adir = d / "audio"
    if not adir.is_dir():
        sys.exit(f"error: put TTS clips in {adir}/<segment_id>.mp3 or {adir}/narration.mp3")
    files = {p.stem: p for p in adir.iterdir() if p.suffix.lower() in AUDIO_EXTS}
    clips = []
    for s in tl["segments"]:
        if s["id"] in files:
            dur = probe(files[s["id"]])
            slot = s["end"] - s["start"]
            if dur > slot + 0.05:
                print(f"warn: {s['id']} audio {dur:.2f}s exceeds slot {slot:.2f}s — run `fit`")
            clips.append((files[s["id"]], s["start"]))
        elif s.get("dialogue", "").strip() and "narration" not in files:
            print(f"warn: no audio for {s['id']}")
    if clips:
        wav = adir / "narration.wav"
        total = tl["segments"][-1]["end"]
        cmd = ["ffmpeg", "-y"]
        for f, _ in clips:
            cmd += ["-i", str(f)]
        parts = [f"[{i}:a]adelay={int(t * 1000)}:all=1[a{i}]" for i, (_, t) in enumerate(clips)]
        mix = "".join(f"[a{i}]" for i in range(len(clips)))
        parts.append(f"{mix}amix=inputs={len(clips)}:normalize=0:dropout_transition=0,apad[aout]")
        cmd += ["-filter_complex", ";".join(parts), "-map", "[aout]", "-t", f"{total:.3f}", str(wav)]
        subprocess.run(cmd, check=True, capture_output=True)
        print(f"wrote {wav}")
    elif "narration" in files:
        wav = files["narration"]
    else:
        sys.exit("error: no matching audio clips found")
    out = d / f"{vid.stem}_narrated.mp4"
    subprocess.run(["ffmpeg", "-y", "-i", str(vid), "-i", str(wav), "-map", "0:v", "-map", "1:a",
                    "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-t", f"{probe(vid):.3f}", str(out)],
                   check=True, capture_output=True)
    print(f"wrote {out}")

if __name__ == "__main__":
    cmds = {"check": check, "retime": retime, "export": export, "fit": fit, "verify": verify,
            "frames": frames, "mux": mux}
    if len(sys.argv) != 3 or sys.argv[1] not in cmds:
        sys.exit(__doc__)
    cmds[sys.argv[1]](pathlib.Path(sys.argv[2]).resolve())
