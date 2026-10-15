#!/usr/bin/env python3
"""Check narration pronunciation by transcribing it back (ASR round trip).

Usage:
  check_pronunciation.py <video_dir> [--model small.en]

Transcribes every audio/<segment_id>.wav with faster-whisper (no prompt, so the
recogniser is not biased towards the script), normalises both texts (numbers
to words, case, punctuation) and diffs them word by word. Each mismatch is
printed with the phonemes Kokoro spoke for the expected words (from
voice_timing.json), so a reviewer can tell a real mispronunciation from an ASR
spelling difference. Writes review/pronunciation.json. Exit code 1 if any
segment has mismatches.

Fix real mispronunciations with a rule in tts/voice.json -> pronunciations,
never by misspelling the script.
"""

import argparse
import difflib
import json
import pathlib
import re
import sys
import warnings

from num2words import num2words

warnings.filterwarnings("ignore")
SAME = {"okay": "ok", "centre": "center", "centres": "centers", "metre": "meter"}
# letter names: ASR often writes the spoken name of a point letter (B -> "be", R -> "are")
LETTERS = {"ay": "a", "be": "b", "bee": "b", "see": "c", "sea": "c", "dee": "d", "gee": "g",
           "eye": "i", "jay": "j", "kay": "k", "oh": "o", "pee": "p", "pea": "p", "queue": "q",
           "cue": "q", "are": "r", "tee": "t", "tea": "t", "you": "u", "ex": "x", "why": "y"}
SAME.update(LETTERS)


def num_words(m):
    s = m.group(0).replace(",", "")
    try:
        return " " + num2words(float(s) if "." in s else int(s)) + " "
    except (ValueError, OverflowError):
        return " " + s + " "


def normalise(text):
    text = re.sub(r"(\d)/(\d)", r"\1 over \2", text)
    text = text.replace("%", " percent").replace("²", " squared").replace("³", " cubed")
    text = re.sub(r"\b[A-Z]{2,3}\b", lambda m: " ".join(m.group(0)), text)  # "AB" -> "A B"
    text = re.sub(r"\d[\d,]*(\.\d+)?", num_words, text)
    words = [w.strip("'") for w in re.findall(r"[a-z0-9']+", text.lower().replace("-", " "))]
    return [SAME.get(w, w) for w in words if w and w != "and"]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("video_dir")
    ap.add_argument("--model", default="small.en")
    args = ap.parse_args()
    d = pathlib.Path(args.video_dir).resolve()
    timing_path = d / "voice_timing.json"
    if not timing_path.exists():
        sys.exit(f"error: {timing_path} not found (run tts/srt_to_voice.py first)")
    timing = json.loads(timing_path.read_text())["segments"]

    from faster_whisper import WhisperModel
    model = WhisperModel(args.model, device="cpu", compute_type="int8")

    report, flagged = [], 0
    for sid, seg in timing.items():
        clip = d / "audio" / f"{sid}.wav"
        if not clip.exists():
            print(f"{sid}: missing {clip.name}")
            continue
        parts, _ = model.transcribe(str(clip), language="en", beam_size=5, condition_on_previous_text=False)
        heard = " ".join(p.text.strip() for p in parts)
        exp, got = normalise(seg["text"]), normalise(heard)
        sm = difflib.SequenceMatcher(a=exp, b=got, autojunk=False)
        diffs = []
        for op, i1, i2, j1, j2 in sm.get_opcodes():
            if op == "equal":
                continue
            span = " ".join(exp[i1:i2])
            ph = [w["phonemes"] for w in seg["words"] if w["word"].lower().strip("'") in exp[i1:i2]]
            diffs.append({"expected": span, "heard": " ".join(got[j1:j2]), "phonemes": " ".join(ph)})
        score = round(sm.ratio(), 3)
        report.append({"id": sid, "score": score, "script": seg["text"], "heard": heard, "mismatches": diffs})
        mark = "ok " if not diffs else "CHECK"
        flagged += bool(diffs)
        print(f"{mark} {sid:<22} {score:.2f}")
        for x in diffs:
            print(f"      expected '{x['expected']}'  heard '{x['heard']}'  phonemes /{x['phonemes']}/")
    out = d / "review" / "pronunciation.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(report, indent=1, ensure_ascii=False) + "\n")
    print(f"{flagged}/{len(report)} segments to check; wrote {out}")
    sys.exit(1 if flagged else 0)


if __name__ == "__main__":
    main()
