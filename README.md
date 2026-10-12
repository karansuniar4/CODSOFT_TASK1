# CleanSight — CodSoft Data Analytics Internship (Task 1)

CleanSight is a beginner-friendly data cleaning and preprocessing project built with Python, Pandas, and Streamlit. It helps users inspect messy datasets, identify common data-quality issues, apply transparent cleaning rules, compare original and cleaned data, manage customer records, and export cleaned datasets with quality reports.

The project demonstrates practical data analytics concepts, including data profiling, missing-value handling, duplicate detection, text standardization, numeric conversion, customer record management, and CSV export.

> **Scope note:** Recommendations and cleaning operations use transparent, rule-based logic. No external generative AI service or API is connected.

## Features

### 1. Data Upload and Preview

* Upload a CSV file for analysis.
* Use the included sample customer dataset.
* Preview original and cleaned datasets.
* Inspect records and column information.

### 2. Data Profiling

* Identify column names and data types.
* Check missing values and unique values.
* Inspect dataset dimensions.
* Review data-quality issues before cleaning.

### 3. Data Cleaning and Preprocessing

* Trim leading and trailing whitespace.
* Standardize text capitalization.
* Convert numeric-looking values using safe conversion.
* Identify missing and invalid values.
* Remove exact duplicate records.
* Choose strategies for handling missing numeric and text values.

### 4. Cleaning Report

* Review cleaning results.
* Compare data before and after cleaning.
* Inspect missing-value counts and duplicate records.
* Download a JSON quality report.

### 5. Customer Management

* View existing customer records.
* Add new customer records.
* Remove a selected customer record.
* Save customer changes to a local CSV file.
* Download customer data as a CSV file.

Customer management is designed for simple local record management and testing. It does not provide multi-user access, authentication, or database synchronization.

### 6. Data Export

* Download cleaned data as a CSV file.
* Export quality-report information as JSON.
* Generate cleaned output files using the standalone Python script.

## Project Structure

```text
CleanSight_CodSoft_Task1/
├── app.py
├── clean_data.py
├── requirements.txt
├── README.md
├── .gitignore
├── .vscode/
│   ├── settings.json
│   └── tasks.json
├── data/
│   └── messy_customers.csv
└── output/
    └── .gitkeep
```

**File descriptions**

* `app.py` — Streamlit dashboard for data cleaning, exploration, reports, exports, and customer management.
* `clean_data.py` — Standalone Pandas data-cleaning script.
* `requirements.txt` — Required Python packages.
* `data/messy_customers.csv` — Sample customer dataset used for testing.
* `output/` — Directory for generated cleaning results.
* `.gitignore` — Prevents selected local files and generated outputs from being tracked by Git.

The application may create `data/managed_customers.csv` when customer records are saved. This file stores locally managed customer data.

## Requirements

* Python 3.10 or newer.
* Visual Studio Code.
* The Microsoft Python extension for VS Code.
* Git installed on your computer.
* An internet connection for installing dependencies, if they are not already installed.

## Installation and Setup

### Step 1: Open the project

1. Open Visual Studio Code.
2. Select **File → Open Folder**.
3. Choose your `CleanSight_CodSoft_Task1` project folder.
4. Select **Terminal → New Terminal**.

### Step 2: Create a virtual environment

Run this command in the VS Code terminal:

```powershell
python -m venv .venv
```

Activate it using Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, you can use the virtual environment's Python executable directly in the following commands.

### Step 3: Install dependencies

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

If the virtual environment is not activated, use:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

### Step 4: Run the dashboard

```powershell
python -m streamlit run app.py
```

If the virtual environment is not activated, use:

```powershell
.\.venv\Scripts\python.exe -m streamlit run app.py
```

### Step 5: Open the application

Open the local URL displayed in your terminal, usually:

`http://localhost:8501`

Keep the terminal running while using the dashboard. To stop the application, press `Ctrl+C` in the terminal.

## How to Use the Dashboard

1. Start the Streamlit application.
2. Upload a CSV file or use the provided sample dataset.
3. Open **Overview** to review the dataset summary.
4. Open **Explore data** to inspect records and column profiles.
5. Open **Cleaning report** to review data-quality information.
6. Open **Export** to download cleaned data and reports.
7. Open **Manage customers** to add or remove customer records.
8. Save customer changes to a CSV file or download the current customer data.

The available cleaning options depend on the current implementation of `app.py`.

## Customer Management Workflow

The Customer Management section allows users to maintain a working customer dataset.

### Add a customer

1. Open the **Manage customers** tab.
2. Enter the values for the displayed customer fields.
3. Click **Add customer**.
4. Review the updated customer table.

### Remove a customer

1. Open the **Manage customers** tab.
2. Select the customer record to remove.
3. Click **Remove selected customer**.
4. Confirm that the record is no longer displayed.

### Save customer data

1. Click **Save changes to CSV**.
2. The application saves the managed dataset to `data/managed_customers.csv`.
3. Alternatively, click **Download customer data** to download the dataset.

**Important:** Save your changes before closing or restarting the application. Keep backups of important data.

## Run the Standalone Cleaning Script

The project also provides a standalone Pandas script for cleaning the included sample dataset.

Run:

```powershell
python clean_data.py
```

If the virtual environment is not activated:

```powershell
.\.venv\Scripts\python.exe clean_data.py
```

The script performs the cleaning and data-quality checks defined in `clean_data.py`. Its intended output files are:

* `output/cleaned_customers.csv`
* `output/quality_report.json`

Generated files can be recreated by running the script again.

## Cleaning Workflow

The standalone cleaning workflow is designed to:

1. Inspect rows, columns, data types, missing values, blank strings, and duplicate records.
2. Normalize blank strings and trim whitespace.
3. Convert numeric-looking values using safe numeric conversion.
4. Treat invalid ages outside the range 0–120 and negative purchase amounts as missing, as implemented in the standalone script.
5. Remove exact duplicate rows.
6. Fill missing numeric values with medians when available.
7. Label missing text values as `Unknown`.
8. Export the cleaned dataset and quality report.

The dashboard and standalone script may use different cleaning rules. Refer to the relevant code before assuming their results will be identical.

> **Data-quality note:** Imputation and duplicate-removal decisions can affect analysis. Keep an untouched copy of the source data and validate cleaning rules before applying them to important datasets.

## Testing the Application

Use sample data to verify that the cleaning and customer-management features work correctly.

Suggested test cases include:

* Names containing extra whitespace.
* Text values with inconsistent capitalization.
* Missing email addresses.
* Missing ages or purchase amounts.
* Invalid numeric values, such as `thirty`.
* Duplicate customer records.
* Ages outside the expected range.
* Negative purchase amounts in datasets where these are invalid.
* Adding a new customer.
* Removing an existing customer.
* Saving and downloading customer data.

After testing, verify that the downloaded files contain the expected records and values.

## GitHub Repository

Repository: [CODSOFT_TASK1](https://github.com/karansuniar4/CODSOFT_TASK1)

### Update the existing repository

If the repository is already connected to your project, you do not need to initialize Git again or add the remote again.

After saving your changes in VS Code, run:

```powershell
git add README.md
git commit -m "Update CleanSight project documentation"
git push
git status
```

If you also changed `app.py` or other tracked source files, stage those files as well, or use `git add .` after checking that you are not adding private data.

### Check your submission

Before submitting the project:

* Confirm that `app.py`, `clean_data.py`, `requirements.txt`, `README.md`, and the sample dataset are present in the repository.
* Run the dashboard locally.
* Run the standalone cleaning script.
* Test the customer-management workflow.
* Check that generated files and confidential data are not accidentally committed.
* Add screenshots if required by your internship instructions.
* Submit the repository URL according to the official CodSoft instructions.

## Data Privacy and Security

This is an educational project intended for local use and demonstration.

* Use synthetic or non-sensitive sample data for testing.
* Do not commit real customer information to a public repository.
* Add `data/managed_customers.csv` to `.gitignore` before saving real customer information.
* Keep backups of important datasets.
* Review cleaning rules before using the results for business decisions.

## Suggested Project Summary

**CleanSight — Data Cleaning and Preprocessing**

Developed a Python and Pandas data-cleaning workflow with a Streamlit dashboard to profile CSV datasets, identify missing and duplicate records, standardize inconsistent text, convert numeric fields, review data-quality reports, and export cleaned data. Added customer-management functionality to create, remove, save, and download customer records.

## Limitations

* The project is an educational demonstration using a small sample dataset.
* It does not connect to a database.
* It does not implement user authentication or role-based access.
* It does not synchronize customer records between different users or computers.
* Cleaning results depend on the selected options and rules implemented in the code.
* It does not connect to an external generative AI service or API.

## Acknowledgment

Created as part of the **CodSoft Data Analytics Internship — Task 1**, focusing on data cleaning and preprocessing with Python and Pandas.
