# CleanSight — CodSoft Data Analytics Internship (Task 1)

CleanSight is a beginner-friendly data cleaning and preprocessing project built with Python, Pandas, and Streamlit. It demonstrates how to inspect a messy dataset, identify common quality issues, apply transparent cleaning rules, review before/after results, and export a cleaned CSV plus a JSON quality report.

> **Scope note:** Recommendations in this project are transparent rule-based suggestions. No external generative-AI service or API is connected.

## Features

- Upload a CSV file or use the included sample customer dataset.
- Preview source and cleaned data side by side.
- Profile columns, data types, missing values, and unique values.
- Optionally trim whitespace, standardize text capitalization, and remove exact duplicate rows.
- Choose strategies for missing numeric and text values.
- Inspect a cleaning report and download cleaned CSV and JSON report.
- Run a standalone Pandas cleaning script to save files under `output/`.

## Project structure

```text
CleanSight_CodSoft_Task1/
├── app.py                     # Streamlit dashboard
├── clean_data.py               # Standalone Pandas cleaning script
├── requirements.txt            # Python dependencies
├── README.md
├── .gitignore
├── .vscode/
│   ├── settings.json
│   └── tasks.json
├── data/
│   └── messy_customers.csv     # Sample input data
└── output/
    └── .gitkeep                # Generated outputs are ignored by Git
```

## Requirements

- Python 3.10 or newer (Python 3.13 should work with current dependencies)
- Visual Studio Code
- VS Code Python extension (Microsoft)
- Git installed and available in the VS Code terminal for GitHub submission

## Run everything from VS Code

1. Download and extract this project ZIP.
2. Open VS Code.
3. Select **File → Open Folder...** and choose `CleanSight_CodSoft_Task1`.
4. Open **Terminal → New Terminal**.
5. Create and activate a virtual environment (Windows PowerShell):

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

   If PowerShell blocks activation, use the environment's Python directly in the next commands: `\.venv\Scripts\python.exe -m pip install -r requirements.txt` and `\.venv\Scripts\python.exe -m streamlit run app.py`.

6. Install dependencies:

   ```powershell
   python -m pip install --upgrade pip
   python -m pip install -r requirements.txt
   ```

7. Start the dashboard:

   ```powershell
   python -m streamlit run app.py
   ```

8. Open the local URL printed in the terminal, usually `http://localhost:8501`. Keep the terminal running while using the dashboard. Press `Ctrl+C` in the terminal to stop it.

## Run the standalone cleaning script

In the VS Code terminal, run:

```powershell
python clean_data.py
```

The script prints the source structure and data-quality checks, cleans the sample dataset, and writes:

- `output/cleaned_customers.csv`
- `output/quality_report.json`

Generated output is intentionally excluded from Git by `.gitignore`; the script regenerates it when run.

## Cleaning workflow

1. Inspect rows, columns, data types, missing values, blank strings, and exact duplicates.
2. Normalize blank strings and trim leading/trailing whitespace.
3. Convert numeric-looking fields using safe numeric conversion.
4. Treat invalid ages outside 0–120 and negative purchase amounts as missing in the standalone script.
5. Remove exact duplicate rows.
6. Fill numeric missing values with medians when available and label missing text as `Unknown` in the standalone script.
7. Export the cleaned dataset and quality report.

**Important:** Imputation choices can affect analysis. Keep an untouched copy of source data and validate cleaning rules for the real dataset before relying on the results.

## GitHub submission from the VS Code terminal

### A. Create the repository

1. Sign in to GitHub in your browser.
2. Create a **new public repository** named `CODSOFT_TASK1` (or use the exact naming format required by your internship instructions).
3. Do not initialize it with a README, license, or `.gitignore` because this folder already contains those files.
4. Copy the repository's HTTPS URL, for example `https://github.com/YOUR-USERNAME/CODSOFT_TASK1.git`.

### B. Push this project

Open the VS Code terminal in the project folder and run these commands one at a time, replacing the URL with your own repository URL:

```powershell
git init
git add .
git commit -m "Complete CodSoft Task 1 data cleaning project"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/CODSOFT_TASK1.git
git push -u origin main
```

If Git asks you to identify yourself, configure your Git author name and email using the name/email you want on commits:

```powershell
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
```

Then repeat `git commit` and `git push`. GitHub may open a browser sign-in or require a credential flow; use GitHub's own sign-in prompt. Never paste a password or access token into project files.

### C. Check before submitting

- Open your GitHub repository page and confirm `app.py`, `clean_data.py`, `data/`, `requirements.txt`, and `README.md` are visible.
- Test the dashboard and standalone script locally.
- Add your own screenshots to the README if your internship instructions require them.
- Use the repository URL in your internship submission and LinkedIn post, following the official instructions and hashtags.

## Suggested project summary

**CleanSight — Data Cleaning & Preprocessing:** Developed a Python/Pandas workflow and Streamlit dashboard to profile CSV datasets, detect missing and duplicate records, normalize inconsistent text, convert numeric fields, review cleaning results, and export cleaned data with a quality report.

## Limitations

This is an educational demonstration using a small synthetic sample dataset. It does not connect to a database, authenticate users, or call a generative AI API. Review all cleaning decisions before applying them to important datasets.
