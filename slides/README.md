# Course Slide Decks

This directory contains Marp-based slide presentations for course kickoffs and block introductions.

---

## Available Slide Decks

### Course Kickoff

**`day1_kickoff.md`** (~10 minutes)
- Welcome and instructor introduction
- Course overview and objectives
- Grading and logistics
- Academic integrity policies
- Today's agenda

**Use this:** At the very start of Day 1, before diving into content.

---

### Optional Block Introductions

**`day1_block_a_intro.md`** (~3 minutes)
- Quick overview of tidy data foundations block
- Learning objectives
- Materials for the session

**`day1_block_b_intro.md`** (~3 minutes)
- Quick overview of SQL foundations block
- Introduction to DuckDB and the dataset
- Learning objectives

**Use these:** Optional quick intros at the start of each block if you want to set context before diving into the teaching notebooks.

---

## Setup (One-Time)

### Install Marp CLI

Marp CLI requires Node.js. Install via npm:

```bash
npm install -g @marp-team/marp-cli
```

**Verify installation:**
```bash
marp --version
```

---

## Building Slides

### Option 1: Use the Build Script (Recommended)

```bash
./scripts/build_slides.sh
```

This generates HTML files for all slide decks in `slides/output/`.

### Option 2: Build Individual Decks

**Generate HTML (standalone, works offline):**
```bash
marp slides/day1_kickoff.md -o slides/output/day1_kickoff.html
```

**Generate PDF:**
```bash
marp slides/day1_kickoff.md --pdf -o slides/output/day1_kickoff.pdf
```

**Generate PowerPoint:**
```bash
marp slides/day1_kickoff.md --pptx -o slides/output/day1_kickoff.pptx
```

---

## Presenting Slides

### Option 1: Open HTML in Browser (Recommended)

```bash
open slides/output/day1_kickoff.html
```

- Press **`F`** for fullscreen
- Press **`→`** or **`Space`** to advance
- Press **`←`** to go back
- Press **`Esc`** to exit fullscreen

### Option 2: VS Code Extension

Install **"Marp for VS Code"** extension:
1. Open VS Code
2. Extensions → Search "Marp for VS Code"
3. Install
4. Open any `.md` file in `slides/`
5. Click "Open Preview to the Side" icon

**Live editing:** Changes appear in real-time!

### Option 3: Marp CLI Preview Mode

```bash
marp -s slides/
```

Opens a local server. Navigate to the URL shown (usually `http://localhost:8080`).

---

## Customizing Slides

### Editing Content

Slides are written in **Markdown with Marp directives**.

**Slide separator:**
```markdown
---
```

**Speaker notes (not visible on slides):**
```markdown
<!-- This is a note for the presenter -->
```

**Classes for special layouts:**
```markdown
<!-- _class: lead -->
```

### Theme Customization

The custom CEU theme is defined in `themes/ceu-theme.css`.

**Colors:**
- Primary: `#1a4d7a` (CEU dark blue)
- Accent: `#3498db` (bright blue)
- Highlight: `#c0392b` (red for emphasis)
- Background: `#ffffff` (white)

**To modify:**
1. Edit `themes/ceu-theme.css`
2. Rebuild slides with `./scripts/build_slides.sh`

---

## File Structure

```
slides/
├── day1_kickoff.md              # Main course introduction
├── day1_block_a_intro.md        # Optional: Tidy data intro
├── day1_block_b_intro.md        # Optional: SQL intro
├── themes/
│   └── ceu-theme.css            # Custom CEU branding
├── output/                       # Generated HTML/PDF (gitignored)
│   ├── day1_kickoff.html
│   ├── day1_block_a_intro.html
│   └── day1_block_b_intro.html
└── README.md                    # This file
```

---

## Tips for Presenting

### Before Class
- Build slides: `./scripts/build_slides.sh`
- Open HTML file in browser
- Test fullscreen mode (`F` key)
- Check all code blocks are readable
- Have backup PDF in case of browser issues

### During Presentation
- **Keep it tight:** These are designed for 3-10 minute intros
- **Don't read slides:** Use them as talking points
- **Pause for questions:** Especially after policies/grading
- **Transition clearly:** "Now let's open the teaching notebook..."

### After Presenting
- HTML files can be shared with students (self-contained)
- Consider posting to Moodle for reference

---

## Evergreen Design

These slides are designed to be **reusable year after year**:
- ✅ No year-specific dates (just "Day 1, Day 2, Day 3")
- ✅ Generic "check syllabus.md" references
- ✅ Focus on timeless content and structure

**To reuse next year:**
1. Review content for any updates
2. Rebuild: `./scripts/build_slides.sh`
3. Done!

---

## Marp Resources

**Official Documentation:**
- [Marp Documentation](https://marpit.marp.app/)
- [Marp CLI](https://github.com/marp-team/marp-cli)
- [Marp for VS Code](https://marketplace.visualstudio.com/items?itemName=marp-team.marp-vscode)

**Markdown Cheat Sheet:**
- [CommonMark Spec](https://commonmark.org/help/)

---

## Troubleshooting

**"marp: command not found"**
→ Install Marp CLI: `npm install -g @marp-team/marp-cli`

**"npm: command not found"**
→ Install Node.js: [https://nodejs.org/](https://nodejs.org/)

**Slides look wrong in browser**
→ Make sure you're using the generated HTML from `output/`, not opening the `.md` file directly

**Theme not applying**
→ Check that `theme: ceu` is in the front matter of the `.md` file

**Code blocks too small**
→ Edit `themes/ceu-theme.css`, increase `pre { font-size: ... }`

---

## Advanced: Creating New Slide Decks

1. Create new `.md` file in `slides/`
2. Add front matter:
   ```markdown
   ---
   marp: true
   theme: ceu
   paginate: true
   header: 'Your Header'
   footer: 'Your Footer'
   ---
   ```
3. Write content with `---` between slides
4. Add to `scripts/build_slides.sh` to auto-build
5. Generate: `marp your_slides.md -o output/your_slides.html`

---

**Questions?** Contact the instructor or check [Marp documentation](https://marpit.marp.app/).
