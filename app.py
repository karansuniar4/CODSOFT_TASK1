import hashlib
import io
import json
import os

import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="CleanSight | Data Quality Studio",
    page_icon="🧹",
    layout="wide",
)

st.markdown(
    """
    <style>
    .block-container {
        padding-top: 1.8rem;
        max-width: 1400px;
    }
    .hero {
        padding: 1.5rem 1.7rem;
        border-radius: 18px;
        background: linear-gradient(120deg, #101c35, #245b82);
        color: white;
        margin-bottom: 1rem;
    }
    .hero h1 {
        color: white;
        margin: 0;
        font-size: 2.2rem;
    }
    .hero p {
        color: #dce9f8;
        margin: .4rem 0 0 0;
    }
    div[data-testid="stMetric"] {
        background: rgba(128,128,128,.08);
        border: 1px solid rgba(128,128,128,.18);
        padding: 14px 16px;
        border-radius: 14px;
    }
    </style>

    <div class="hero">
        <h1>CleanSight</h1>
        <p>AI-assisted data cleaning · Explore, validate, clean, and export your dataset</p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.caption(
    "CodSoft Data Analytics Internship · Task 1 — Data Cleaning & Preprocessing"
)

# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

with st.sidebar:
    st.header("Workspace")

    uploaded = st.file_uploader(
        "Upload a CSV file",
        type=["csv"],
    )

    st.divider()
    st.subheader("Cleaning options")

    trim_text = st.checkbox(
        "Trim extra whitespace",
        value=True,
    )

    standardize_text = st.checkbox(
        "Standardize text capitalization",
        value=True,
    )

    remove_duplicates = st.checkbox(
        "Remove exact duplicate rows",
        value=True,
    )

    numeric_strategy = st.selectbox(
        "Missing numeric values",
        [
            "Keep missing",
            "Fill with median",
            "Fill with mean",
            "Fill with zero",
        ],
    )

    text_strategy = st.selectbox(
        "Missing text values",
        [
            "Keep missing",
            "Fill with Unknown",
            "Fill with mode",
        ],
    )

    st.caption(
        "Review each choice before applying it to important business data."
    )


# --------------------------------------------------
# LOAD CSV
# --------------------------------------------------

@st.cache_data(show_spinner=False)
def load_csv(data):
    return pd.read_csv(
        io.BytesIO(data),
        encoding="utf-8-sig",
        on_bad_lines="error",
    )


# --------------------------------------------------
# DATA CLEANING FUNCTION
# --------------------------------------------------

def clean_frame(source):
    df = source.copy()

    # Convert blank cells into missing values.
    df = df.replace(r"^\s*$", pd.NA, regex=True)

    # Remove extra spaces.
    if trim_text:
        for col in df.select_dtypes(
            include=["object", "string"]
        ).columns:
            df[col] = df[col].astype("string").str.strip()

    # Standardize capitalization except for emails.
    if standardize_text:
        for col in df.select_dtypes(
            include=["object", "string"]
        ).columns:
            if col.lower() != "email":
                df[col] = df[col].map(
                    lambda value: value.title()
                    if isinstance(value, str)
                    and value.lower() != "unknown"
                    else value
                )

    # Convert suitable columns to numeric values.
    text_columns = {
        "email",
        "name",
        "city",
        "address",
        "phone",
    }

    for col in df.columns:
        if (
            pd.api.types.is_object_dtype(df[col])
            or pd.api.types.is_string_dtype(df[col])
        ) and col.lower() not in text_columns:

            nonmissing = df[col].dropna()

            if not nonmissing.empty:
                converted = pd.to_numeric(
                    df[col]
                    .astype("string")
                    .str.replace(",", "", regex=False),
                    errors="coerce",
                )

                threshold = max(
                    1,
                    int(0.7 * len(nonmissing)),
                )

                if converted.notna().sum() >= threshold:
                    df[col] = converted

    # Validate ages between 0 and 120.
    age_columns = [
        col for col in df.columns
        if col.lower() == "age"
    ]

    if age_columns:
        age_col = age_columns[0]

        df[age_col] = pd.to_numeric(
            df[age_col],
            errors="coerce",
        )

        df.loc[
            ~df[age_col].between(0, 120),
            age_col,
        ] = pd.NA

    # Remove exact duplicate rows when enabled.
    if remove_duplicates:
        df = df.drop_duplicates().copy()

    # Handle missing numeric and text values.
    for col in df.columns:
        if (
            pd.api.types.is_numeric_dtype(df[col])
            and df[col].isna().any()
        ):
            if (
                numeric_strategy == "Fill with median"
                and df[col].notna().any()
            ):
                df[col] = df[col].fillna(
                    df[col].median()
                )

            elif (
                numeric_strategy == "Fill with mean"
                and df[col].notna().any()
            ):
                df[col] = df[col].fillna(
                    df[col].mean()
                )

            elif numeric_strategy == "Fill with zero":
                df[col] = df[col].fillna(0)

        elif (
            (
                pd.api.types.is_object_dtype(df[col])
                or pd.api.types.is_string_dtype(df[col])
            )
            and df[col].isna().any()
        ):
            if text_strategy == "Fill with Unknown":
                df[col] = df[col].fillna("Unknown")

            elif text_strategy == "Fill with mode":
                modes = df[col].mode(dropna=True)

                if not modes.empty:
                    df[col] = df[col].fillna(
                        modes.iloc[0]
                    )

    return df


# --------------------------------------------------
# FILE PATHS
# --------------------------------------------------

project_dir = os.path.dirname(
    os.path.abspath(__file__)
)

data_dir = os.path.join(
    project_dir,
    "data",
)

sample_path = os.path.join(
    data_dir,
    "messy_customers.csv",
)

managed_path = os.path.join(
    data_dir,
    "managed_customers.csv",
)


# --------------------------------------------------
# LOAD THE ACTIVE DATASET
# --------------------------------------------------

if uploaded is not None:
    try:
        uploaded_bytes = uploaded.getvalue()
        source_df = load_csv(uploaded_bytes)

        dataset_key = (
            "upload:"
            + hashlib.sha256(
                uploaded_bytes
            ).hexdigest()
        )

        dataset_label = uploaded.name

    except Exception as exc:
        st.error(
            f"Could not read this CSV: {exc}"
        )
        st.stop()

else:
    st.info(
        "Upload your own CSV using the sidebar, "
        "or start with the included sample dataset."
    )

    if not os.path.isfile(sample_path):
        st.error(
            "Sample dataset not found. Please add "
            "data/messy_customers.csv or upload a CSV file."
        )
        st.stop()

    try:
        with open(sample_path, "rb") as file:
            sample_bytes = file.read()

        source_df = load_csv(sample_bytes)

        dataset_key = (
            "sample:"
            + hashlib.sha256(
                sample_bytes
            ).hexdigest()
        )

        dataset_label = "messy_customers.csv"

    except Exception as exc:
        st.error(
            f"Could not read the sample CSV: {exc}"
        )
        st.stop()


# --------------------------------------------------
# IMPORTANT FIX:
# RESET CUSTOMER DATA WHEN A DIFFERENT CSV IS UPLOADED
# --------------------------------------------------

if (
    st.session_state.get("managed_dataset_key")
    != dataset_key
):
    if uploaded is None and os.path.isfile(managed_path):
        try:
            saved_df = pd.read_csv(
                managed_path,
                encoding="utf-8-sig",
            )

            if list(saved_df.columns) == list(
                source_df.columns
            ):
                st.session_state.managed_customers = (
                    saved_df
                )
            else:
                st.session_state.managed_customers = (
                    source_df.copy()
                )

        except Exception:
            st.session_state.managed_customers = (
                source_df.copy()
            )

    else:
        # Uploaded CSV always becomes the active dataset.
        st.session_state.managed_customers = (
            source_df.copy()
        )

    st.session_state.managed_dataset_key = (
        dataset_key
    )

elif "managed_customers" not in st.session_state:
    st.session_state.managed_customers = (
        source_df.copy()
    )


# Use the current active dataset.
original = (
    st.session_state.managed_customers.copy()
)

cleaned = clean_frame(original)

rows_before = len(original)
rows_after = len(cleaned)

duplicate_count = int(
    original.duplicated().sum()
)

missing_before = int(
    original.replace(
        r"^\s*$",
        pd.NA,
        regex=True,
    ).isna().sum().sum()
)

missing_after = int(
    cleaned.isna().sum().sum()
)


# --------------------------------------------------
# DATASET INFORMATION
# --------------------------------------------------

st.caption(
    f"Active dataset: {dataset_label} · "
    f"{len(original)} records · "
    f"{len(original.columns)} columns"
)


# --------------------------------------------------
# DASHBOARD TABS
# --------------------------------------------------

tab1, tab2, tab3, tab4, tab5 = st.tabs(
    [
        "Overview",
        "Explore data",
        "Cleaning report",
        "Export",
        "Manage customers",
    ]
)


# --------------------------------------------------
# TAB 1: OVERVIEW
# --------------------------------------------------

with tab1:
    st.subheader(
        "Data quality at a glance"
    )

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Original rows",
        f"{rows_before:,}",
    )

    c2.metric(
        "Cleaned rows",
        f"{rows_after:,}",
        delta=f"{rows_after - rows_before:+,} rows",
    )

    c3.metric(
        "Duplicate rows found",
        f"{duplicate_count:,}",
    )

    c4.metric(
        "Missing cells after cleaning",
        f"{missing_after:,}",
        delta=f"{missing_after - missing_before:+,} vs before",
    )

    st.markdown(
        "#### Before cleaning"
    )

    st.caption(
        f"Total uploaded records: {len(original)}"
    )

    # Display all records, not just the first few.
    st.dataframe(
        original,
        use_container_width=True,
        hide_index=True,
        height=400,
    )

    st.markdown(
        "#### After cleaning"
    )

    st.caption(
        f"Records remaining after cleaning: {len(cleaned)}"
    )

    st.dataframe(
        cleaned,
        use_container_width=True,
        hide_index=True,
        height=400,
    )


# --------------------------------------------------
# TAB 2: EXPLORE DATA
# --------------------------------------------------

with tab2:
    st.subheader(
        "Explore columns and distributions"
    )

    st.write(
        "**Dataset dimensions:**",
        f"{original.shape[0]} rows × "
        f"{original.shape[1]} columns",
    )

    profile = pd.DataFrame(
        {
            "Column": original.columns,

            "Data type": [
                str(original[col].dtype)
                for col in original.columns
            ],

            "Missing values": [
                int(
                    original[col]
                    .replace(
                        r"^\s*$",
                        pd.NA,
                        regex=True,
                    )
                    .isna()
                    .sum()
                )
                for col in original.columns
            ],

            "Unique values": [
                int(
                    original[col].nunique(
                        dropna=True
                    )
                )
                for col in original.columns
            ],
        }
    )

    st.dataframe(
        profile,
        use_container_width=True,
        hide_index=True,
    )

    numeric_cols = (
        cleaned
        .select_dtypes(include="number")
        .columns.tolist()
    )

    if numeric_cols:
        chosen = st.selectbox(
            "Choose a numeric column to chart",
            numeric_cols,
        )

        series = cleaned[chosen].dropna()

        if not series.empty:
            chart_data = (
                series.value_counts()
                .sort_index()
                .head(40)
            )

            st.bar_chart(
                chart_data,
                x_label=chosen,
                y_label="Frequency",
            )

        else:
            st.warning(
                "No numeric values available for this column."
            )

    else:
        st.info(
            "No numeric columns detected. "
            "Convert suitable columns to numbers to chart them."
        )


# --------------------------------------------------
# TAB 3: CLEANING REPORT
# --------------------------------------------------

with tab3:
    st.subheader(
        "Cleaning report"
    )

    report = pd.DataFrame(
        {
            "Column": original.columns,

            "Missing before": [
                int(
                    original[col]
                    .replace(
                        r"^\s*$",
                        pd.NA,
                        regex=True,
                    )
                    .isna()
                    .sum()
                )
                for col in original.columns
            ],

            "Missing after": [
                int(
                    cleaned[col].isna().sum()
                )
                for col in cleaned.columns
            ],

            "Type before": [
                str(original[col].dtype)
                for col in original.columns
            ],

            "Type after": [
                str(cleaned[col].dtype)
                for col in cleaned.columns
            ],
        }
    )

    st.dataframe(
        report,
        use_container_width=True,
        hide_index=True,
    )

    st.markdown(
        "#### AI-assisted recommendations "
        "(rule-based suggestions)"
    )

    recommendations = []

    for col in original.columns:
        normalized = original[col].replace(
            r"^\s*$",
            pd.NA,
            regex=True,
        )

        missing = int(
            normalized.isna().sum()
        )

        if missing:
            recommendations.append(
                f"**{col}:** {missing} missing/blank "
                "value(s). Review whether to keep, "
                "impute, or label them."
            )

        if (
            original[col].duplicated().any()
            and original[col].nunique(
                dropna=False
            ) < len(original)
        ):
            recommendations.append(
                f"**{col}:** repeated values exist; "
                "confirm whether repetition is valid "
                "for this field."
            )

    if duplicate_count:
        recommendations.append(
            f"**Rows:** {duplicate_count} exact "
            "duplicate row(s) detected in the source."
        )

    if not recommendations:
        st.success(
            "No obvious missing-value or exact-duplicate "
            "issues were detected by these basic rules."
        )

    else:
        for item in recommendations:
            st.markdown(
                f"- {item}"
            )

    st.caption(
        "These are transparent rule-based suggestions, "
        "not outputs from a connected generative AI model. "
        "Validate before applying."
    )


# --------------------------------------------------
# TAB 4: EXPORT
# --------------------------------------------------

with tab4:
    st.subheader(
        "Download cleaned dataset"
    )

    csv_bytes = (
        cleaned
        .to_csv(index=False)
        .encode("utf-8-sig")
    )

    st.download_button(
        "Download cleaned CSV",
        data=csv_bytes,
        file_name="cleaned_dataset.csv",
        mime="text/csv",
        type="primary",
    )

    report_obj = {
        "dataset": dataset_label,
        "rows_before": rows_before,
        "rows_after": rows_after,
        "columns": int(
            original.shape[1]
        ),
        "duplicate_rows_found": duplicate_count,
        "missing_cells_before": missing_before,
        "missing_cells_after": missing_after,

        "cleaning_options": {
            "trim_text": trim_text,
            "standardize_text": standardize_text,
            "remove_duplicates": remove_duplicates,
            "numeric_strategy": numeric_strategy,
            "text_strategy": text_strategy,
        },
    }

    st.download_button(
        "Download quality report (JSON)",
        data=json.dumps(
            report_obj,
            indent=2,
        ),
        file_name="quality_report.json",
        mime="application/json",
    )

    st.success(
        "Your exports are ready. "
        "Use the download buttons to save the files."
    )


# --------------------------------------------------
# TAB 5: MANAGE CUSTOMERS
# --------------------------------------------------

with tab5:
    st.subheader(
        "Customer Management"
    )

    st.write(
        "Add customers, remove records, and save your changes."
    )

    customers = (
        st.session_state.managed_customers
    )

    st.markdown(
        "### Current customers"
    )

    st.caption(
        f"Total customer records: {len(customers)}"
    )

    st.dataframe(
        customers,
        use_container_width=True,
        hide_index=True,
        height=400,
    )

    # Add customer form.
    st.markdown(
        "### Add a customer"
    )

    with st.form(
        "add_customer_form",
        clear_on_submit=True,
    ):
        new_customer = {}

        for col in customers.columns:
            if pd.api.types.is_numeric_dtype(
                customers[col]
            ):
                valid = pd.to_numeric(
                    customers[col],
                    errors="coerce",
                ).dropna()

                default = (
                    float(valid.median())
                    if not valid.empty
                    else 0.0
                )

                new_customer[col] = st.number_input(
                    col,
                    value=default,
                    key=f"new_{col}",
                )

            else:
                new_customer[col] = st.text_input(
                    col,
                    key=f"new_{col}",
                )

        add_clicked = st.form_submit_button(
            "Add customer"
        )

    if add_clicked:
        new_row = pd.DataFrame(
            [new_customer],
            columns=customers.columns,
        )

        st.session_state.managed_customers = (
            pd.concat(
                [customers, new_row],
                ignore_index=True,
            )
        )

        st.success(
            "Customer added to the working dataset."
        )

        st.rerun()

    # Remove customer.
    st.markdown(
        "### Remove a customer"
    )

    if not customers.empty:
        selected_row = st.selectbox(
            "Select the row number to remove",

            options=list(
                range(len(customers))
            ),

            format_func=lambda i: (
                f"Row {i + 1} — "
                + ", ".join(
                    str(customers.iloc[i][col])
                    for col in customers.columns[:2]
                )
            ),
        )

        if st.button(
            "Remove selected customer",
            type="secondary",
        ):
            st.session_state.managed_customers = (
                customers
                .drop(
                    customers.index[selected_row]
                )
                .reset_index(drop=True)
            )

            st.success(
                "Customer removed."
            )

            st.rerun()

    else:
        st.info(
            "There are no customers to remove."
        )

    # Save changes.
    st.markdown(
        "### Save customer data"
    )

    if st.button(
        "Save changes to CSV",
        type="primary",
    ):
        os.makedirs(
            data_dir,
            exist_ok=True,
        )

        st.session_state.managed_customers.to_csv(
            managed_path,
            index=False,
            encoding="utf-8-sig",
        )

        st.success(
            f"Customer data saved to: {managed_path}"
        )

    # Download customer data.
    customer_csv = (
        st.session_state.managed_customers
        .to_csv(index=False)
        .encode("utf-8-sig")
    )

    st.download_button(
        "Download customer data",
        data=customer_csv,
        file_name="managed_customers.csv",
        mime="text/csv",
    )


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.divider()

st.caption(
    "CleanSight · Learning project · "
    "Always keep a copy of your original dataset."
)
