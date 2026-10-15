export const meta = {
  name: 'video-qa',
  description: 'Independent QA of a rendered maths video: pronunciation, theme compliance and visual quality, picture-narration sync',
  whenToUse: 'manim-video step 9: after the final render, review/frames, voice_timing.json and review/pronunciation.json exist. args: {dir}',
  phases: [
    { title: 'QA', detail: 'three independent reviewers, one lens each' },
  ],
}

const A = typeof args === 'string' ? { dir: args } : (args || {})
if (!A.dir) throw new Error('pass args.dir = the video folder, e.g. videos/003-some-slug')
const dir = A.dir
const RUBRIC = '.claude/skills/manim-video/references/review-rubric.md'

const ISSUE = {
  type: 'object',
  properties: {
    severity: { type: 'string', enum: ['blocker', 'major', 'minor'] },
    segment: { type: 'string', description: 'segment id, or "global"' },
    problem: { type: 'string' },
    fix: { type: 'string', description: 'concrete change: scene.py edit, voice.json rule, timeline change' },
  },
  required: ['severity', 'segment', 'problem', 'fix'],
}
const REVIEW = {
  type: 'object',
  properties: {
    approved: { type: 'boolean', description: 'true only if there are no blocker or major issues' },
    summary: { type: 'string' },
    issues: { type: 'array', items: ISSUE },
  },
  required: ['approved', 'summary', 'issues'],
}

const common = `You are an independent QA reviewer for a professional maths explainer channel. You did not make this video. Be strict and specific.
Video folder: ${dir}. timeline.json is the source of truth (dialogue = exact spoken words with start/end times). Stills of the rendered video are in ${dir}/review/frames/<segment_id>_mid.png and _end.png (middle and end of each segment).
Read ${RUBRIC} for your lens's checklist, the severity definitions and the approval rule. Do not edit any file; every issue needs a segment id and a concrete fix.`

const LENSES = [
  {
    key: 'pronunciation',
    prompt: `Lens: PRONUNCIATION. Read ${dir}/review/pronunciation.json (each narration clip transcribed back by Whisper and diffed against the script, with the phonemes Kokoro actually spoke for each mismatch) and ${dir}/voice_timing.json (phonemes for every word). For each mismatch decide: real mispronunciation, or only an ASR spelling difference (number formats, homophones, letter names)? Use the IPA phonemes to decide. Also scan voice_timing.json phonemes for risky words the ASR may have accepted anyway: point letters (a capital A read as the article /ɐ/), Greek letters, names, maths terms, heteronyms (read, minute, live). For every real problem give the exact tts/voice.json pronunciations rule to add ({"pattern": regex, "replace": "[word](/IPA/)"}), checked against the existing rules.`,
  },
  {
    key: 'theme-visual',
    prompt: `Lens: THEME COMPLIANCE AND VISUAL QUALITY. Run .venv/bin/python .claude/skills/manim-video/scripts/theme_lint.py ${dir} (errors are blockers). Read theme/THEME.md, then look at every frame image. Check: colour roles are used as specified (PRIMARY for the current object, HIGHLIGHT only for the one key insight, POSITIVE for final answers, NEGATIVE for removed parts), backdrop present, text and maths inside the safe area, nothing overlapping or clipped, no clutter (at most about three equations), text large enough to read on a phone, consistent layout from segment to segment, and a calm, professional look (no gimmicky or dramatic titles or effects).`,
  },
  {
    key: 'sync',
    prompt: `Lens: PICTURE MATCHES NARRATION. For each segment compare its dialogue (and the on_screen/animation plan) with its _mid and _end frames. Flag: something the narrator talks about that is not visible by the end of its segment; the screen showing a later step before it is narrated; maths on screen that differs from what is said (wrong number, sign, label or typo in the rendered MathTex); labels pointing at the wrong object; a segment that is visually static for a long narration. Also run .venv/bin/python .claude/skills/manim-video/scripts/timeline_tool.py check ${dir} and .venv/bin/python .claude/skills/manim-video/scripts/timeline_tool.py verify ${dir} and report any failure as a blocker.`,
  },
]

phase('QA')
const reviews = await parallel(LENSES.map(l => () =>
  agent(`${common}\n\n${l.prompt}`, { label: `qa:${l.key}`, phase: 'QA', schema: REVIEW })
    .then(r => r && { lens: l.key, ...r })))

const done = reviews.filter(Boolean)
const missing = LENSES.map(l => l.key).filter(k => !done.some(r => r.lens === k))
if (missing.length) log(`reviewers that returned nothing: ${missing.join(', ')}`)
const issues = done.flatMap(r => r.issues.map(i => ({ lens: r.lens, ...i })))
const blocking = issues.filter(i => i.severity !== 'minor')

return {
  approved: !missing.length && done.every(r => r.approved) && !blocking.length,
  summaries: Object.fromEntries(done.map(r => [r.lens, r.summary])),
  blocking,
  minor: issues.filter(i => i.severity === 'minor'),
  missing_reviewers: missing,
}
