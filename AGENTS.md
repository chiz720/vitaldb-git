# AGENTS.md — VitalDBGit

## Build Command

```bash
source ~/miniconda3/etc/profile.d/conda.sh && conda activate vitaldb && jupyter-book build .
```

Not `conda activate` directly (requires init first on this machine).

## Critical Rules

- **Never edit `_build/`** — generated output, do not touch
- **Never re-execute notebooks at build time** — execution mode is "off" in `_config.yml`
- **Always use relative data paths** (`vital_db/` not `/Volumes/iDrisAI/...`)
- **Keep `_toc.yml` in sync** when adding/removing chapters — jupyter-book fails hard on missing files
- **All code cells must have `"tags": ["hide-input"]`** in cell metadata for the show/hide toggle to work
- **Duplicate file entries in `_toc.yml` cause build failure** with "document file used multiple times" error

## Environment

- Conda env: `vitaldb` at `~/miniconda3`
- Python: 3.12.12
- Key packages: vitaldb, pandas, numpy, scipy, matplotlib, seaborn, scikit-learn, statsmodels

## TOC / Chapter Structure

- Prose chapters: `notebooks/partN_name/chNN_slug.md`
- Root-level notebooks: `*.ipynb` at book root
- Sections under chapters: `sections: - file: notebook_name`
- `[EXISTS]` / `[PLANNED]` markers in `_toc.yml` comments are informational only

## Data Loading

```python
from pathlib import Path
DATA_DIR = Path('vital_db')
cases  = pd.read_csv(DATA_DIR / 'all_cases.csv')
labs   = pd.read_csv(DATA_DIR / 'labs.csv')
tracks = pd.read_csv(DATA_DIR / 'tracks.csv')
```

## Git

- This was not a git repo originally — required `git init`
- GitHub remote: `https://github.com/chiz720/vitaldb-git`
- Run `git add -A && git commit -m "..."` after building and verifying changes