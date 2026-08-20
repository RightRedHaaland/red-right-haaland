# Red Right Haaland — live command centre

Self-updating FPL dashboard. GitHub Actions pulls the official FPL API every
30 minutes and rebuilds `index.html` from `template.html`; GitHub Pages serves it.

## One-time setup (after uploading these files)
1. **Settings → Pages** → Source: *Deploy from a branch* → Branch: `main`, folder `/ (root)` → Save.
2. **Actions tab** → enable workflows if prompted → open *Refresh FPL data* → *Run workflow* once.
3. Bookmark: `https://<your-username>.github.io/<repo-name>/`

## What updates automatically
Prices, ownership, injury flags/news, chance-of-playing, form, deadlines.

## What updates via Claude
Fixture/Elo model, DefCon history, squad, Expert Board, projections — these are
curated in Cowork sessions and land as edits to `template.html`.

Note: this site is public. Notes & Intel are stripped from this build on purpose.
