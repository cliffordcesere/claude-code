# Studio Brief

House art direction for Claude Code: flyers, posters and the motion version of the same flyer.

A design skill that behaves like an art director with a print vendor on speed dial. It refuses to start before the brief is real, names a single material per project, caps the number of typefaces and accents, states the print specs that are not negotiable (300 DPI, CMJN, 3 mm bleed, 5 mm safety), and forces a render → inspect → fix loop before delivery.

## Install

```bash
# As a local plugin in this repo
/plugin marketplace add ./
/plugin install studio-brief@claude-code-plugins
```

Or copy the skill into a project:

```bash
cp -R plugins/studio-brief/skills/studio-brief .claude/skills/
```

## Use

```text
Use studio-brief. Flyer A3 pour une soirée techno le 14 novembre à Port-au-Prince,
promesse « une nuit, trois scènes ». Matière : sérigraphie sur kraft.
Exigence : objet de collection. Déclinaison 9:16 de 8 s.
```

It answers with six lines — direction, idea, grid, palette, typography, blockers — and only then builds.

## What is inside

| File | Role |
|---|---|
| `SKILL.md` | The working rules: intake, one idea, restraint caps, print and motion invariants. |
| `references/palettes.md` | Six named materials with full palettes and type voices, plus a list of palettes to avoid. |
| `references/print-specs.md` | Formats, bleed, rich black, ink limits, PDF/X-4 export, control commands. |
| `references/motion-specs.md` | Durations, easing, safe zones, ffmpeg exports, Remotion vs HyperFrames. |
| `references/tells.md` | The blacklist and six validation tests, including the 15 % shrink test. |
| `references/intake.md` | A ten-line brief form to paste into a client thread. |
| `scripts/preflight.mjs` | Checks bleed, effective DPI, colour space and embedded fonts before the file reaches the printer. |

## Preflight

```bash
node plugins/studio-brief/scripts/preflight.mjs poster.pdf --trim 297 420
node plugins/studio-brief/scripts/preflight.mjs flyer.png --trim 148 210
```

Exit `0` conforms, `1` has blockers, `2` is missing ImageMagick/poppler.

## Pair it with

The skill decides; these render.

```bash
npx skills add remotion-dev/skills        # React → MP4
npx hyperframes skills update             # HTML/CSS → MP4, Apache-2.0
npx skills add greensock/gsap-skills      # timing and easing, MIT
npx skills add anthropics/skills --skill canvas-design --agent claude-code   # static PNG/PDF
npx skills add nutlope/hallmark -g        # anti-slop lint in a real browser
```

## Editing

`references/palettes.md` is meant to be rewritten with your own material, palette and typefaces. That file, more than any other, is what makes the output look like your studio and not like everyone's.

## Licence

MIT for this plugin. Fonts mentioned in `references/palettes.md` are SIL Open Font License; check the licence before shipping a modified copy.
