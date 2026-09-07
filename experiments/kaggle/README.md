# Kaggle

Workspace for Kaggle competitions and projects. Each competition lives in its own subfolder.

## Structure

```
kaggle/
├── README.md
├── CLAUDE.md
└── <competition-name>/
    ├── data/          # raw + processed data (gitignored)
    ├── notebooks/     # exploration & EDA
    ├── src/           # reusable code: features, models, training
    ├── submissions/   # generated submission files
    └── README.md      # competition-specific notes
```

## Getting started

1. Create a folder for the competition:

   ```bash
   mkdir -p <competition-name>/{data,notebooks,src,submissions}
   ```

2. Download the data with the Kaggle CLI:

   ```bash
   kaggle competitions download -c <competition-name> -p <competition-name>/data
   unzip '<competition-name>/data/*.zip' -d <competition-name>/data
   ```

3. Explore in `notebooks/`, promote stable code into `src/`.

4. Submit:

   ```bash
   kaggle competitions submit -c <competition-name> \
     -f <competition-name>/submissions/submission.csv -m "description"
   ```

## Setup

```bash
pip install -r requirements.txt   # kaggle, pandas, numpy, scikit-learn, torch, etc.
```

Configure Kaggle API credentials at `~/.kaggle/kaggle.json` (chmod 600).

## Conventions

- Keep raw data out of version control; commit small artifacts and code only.
- Set a global random seed for reproducibility.
- Track CV scores vs. leaderboard scores in each competition's README.
