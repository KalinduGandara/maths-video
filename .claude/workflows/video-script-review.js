export const meta = {
  name: 'video-script-review',
  description: 'Independent reviewers check a maths video script (maths, steps, clarity, hook and tone, narration) and approve or reject it',
  whenToUse: 'manim-video step 5: after timeline.json and script.md are drafted and before any scene.py is written. args: {dir, round?, previous?}',
  phases: [
    { title: 'Review', detail: 'five independent reviewers, one lens each' },
  ],
}

// args: "videos/NNN-slug" or {dir, round, previous}. `previous` is the issue list
// from the last round, so reviewers confirm each one was fixed.
const A = typeof args === 'string' ? { dir: args } : (args || {})
if (!A.dir) throw new Error('pass args.dir = the video folder, e.g. videos/003-some-slug')
const dir = A.dir
const round = A.round || 1
const RUBRIC = '.claude/skills/manim-video/references/review-rubric.md'
const STYLE = '.claude/skills/manim-video/references/style-guide.md'

const ISSUE = {
  type: 'object',
  properties: {
    severity: { type: 'string', enum: ['blocker', 'major', 'minor'] },
    segment: { type: 'string', description: 'segment id, or "global"' },
    problem: { type: 'string' },
    fix: { type: 'string', description: 'concrete replacement text or change' },
  },
  required: ['severity', 'segment', 'problem', 'fix'],
}
const REVIEW = {
  type: 'object',
  properties: {
    approved: { type: 'boolean', description: 'true only if there are no blocker or major issues' },
    score: { type: 'integer', minimum: 1, maximum: 10 },
    summary: { type: 'string', description: 'two or three sentences' },
    issues: { type: 'array', items: ISSUE },
    previous_unfixed: { type: 'array', items: { type: 'string' }, description: 'issues from the previous round that are still not fixed' },
  },
  required: ['approved', 'score', 'summary', 'issues', 'previous_unfixed'],
}

const common = `You are an independent reviewer for a professional maths explainer channel. You did not write this script and you owe the writer nothing: be strict, specific and fair.
Video folder: ${dir}. Read ${dir}/timeline.json (source of truth: dialogue = exact spoken words, animation/on_screen = the visual plan), ${dir}/script.md, ${dir}/research.md and, if script.md names one, the channel brief.
Read ${RUBRIC} (your lens's checklist, the severity definitions and the approval rule) and ${STYLE}.
Do not edit any file. Report issues only for your own lens; each one needs a segment id and a concrete fix (replacement wording, an added step, a changed visual).
${A.previous ? `This is review round ${round}. Issues raised last round:\n${JSON.stringify(A.previous, null, 1)}\nCheck each one in your lens and list any that are still not fixed in previous_unfixed.` : 'This is review round 1; previous_unfixed is [].'}`

const LENSES = [
  {
    key: 'maths-solution',
    prompt: `Lens: MATHS SOLUTION. Before reading the script's working, solve the problem yourself from the problem statement only, preferably by a different method than the script uses. Check the result numerically with Python (.venv/bin/python, e.g. sympy or a direct numerical construction). Then compare with the script: is the final answer right, are all stated facts and theorems true and correctly applied, are cases/conditions handled (rejected roots, domain, units)? Is the chosen method the clearest one for the audience given research.md? A wrong answer or a false claim is a blocker.`,
  },
  {
    key: 'maths-steps',
    prompt: `Lens: STEP-BY-STEP RIGOUR. Go through every segment in order and check every equation, expansion, substitution and piece of arithmetic in the dialogue, on_screen and animation fields (recompute each with Python where useful). Flag any step that is wrong, any jump that skips work an average viewer needs to see, notation that changes meaning, and any mismatch between what is said and what the animation plan shows.`,
  },
  {
    key: 'clarity',
    prompt: `Lens: CLARITY FOR THE TARGET VIEWER. Read the narration as a viewer at the audience level in script.md (default: an average high-school student who is not a maths enthusiast). For each step ask: is it motivated (why are we doing this now?), are terms and notation defined before use, is there one idea per segment, does the visual plan actually show the idea, is the pacing right? Flag places where this viewer would get lost or bored, and missing intuition or a missing sanity check.`,
  },
  {
    key: 'hook-and-tone',
    prompt: `Lens: HOOK, RETENTION AND PROFESSIONAL TONE. Judge the first segment(s) against the hook rules in the style guide: does the opening make a curious viewer stay, using the real problem and a specific question or open loop, within about 10 seconds, without clickbait or hype? Check the title (timeline.json title, on-screen title, any title options), the signposting that keeps people watching to the end, that open loops are paid off, and the ending/CTA. Flag anything dramatic, cheeky, gimmicky, sensational or filler.`,
  },
  {
    key: 'narration',
    prompt: `Lens: NARRATION FOR TEXT-TO-SPEECH. The dialogue is spoken by a TTS voice (Kokoro, rules in tts/voice.json → pronunciations). Check it is written for the ear: maths spoken in words (no symbols, LaTeX, digits that read badly), short sentences, unambiguous phrasing ("one over x squared" vs "one over x, all squared"), consistent names, point letters that could be read as words (e.g. capital A, "I"), names and terms with risky pronunciation (list any that need a voice.json rule). Check the narration introduces each visual just before or as it appears. Run .venv/bin/python .claude/skills/manim-video/scripts/timeline_tool.py check ${dir} and report any errors.`,
  },
]

phase('Review')
const reviews = await parallel(LENSES.map(l => () =>
  agent(`${common}\n\n${l.prompt}`, { label: `review:${l.key}`, phase: 'Review', schema: REVIEW })
    .then(r => r && { lens: l.key, ...r })))

const done = reviews.filter(Boolean)
const missing = LENSES.map(l => l.key).filter(k => !done.some(r => r.lens === k))
if (missing.length) log(`reviewers that returned nothing: ${missing.join(', ')}`)
const issues = done.flatMap(r => r.issues.map(i => ({ lens: r.lens, ...i })))
const blocking = issues.filter(i => i.severity !== 'minor')
const unfixed = done.flatMap(r => r.previous_unfixed.map(p => ({ lens: r.lens, issue: p })))
const approved = !missing.length && done.every(r => r.approved) && !blocking.length && !unfixed.length

return {
  approved,
  round,
  scores: Object.fromEntries(done.map(r => [r.lens, r.score])),
  summaries: Object.fromEntries(done.map(r => [r.lens, r.summary])),
  blocking,
  minor: issues.filter(i => i.severity === 'minor'),
  previous_unfixed: unfixed,
  missing_reviewers: missing,
}
