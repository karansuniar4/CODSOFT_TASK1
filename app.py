import io
import os
import json
import pandas as pd
import streamlit as st

st.set_page_config(page_title="CleanSight | Data Quality Studio", page_icon="🧹", layout="wide")

st.markdown("""
<style>
.block-container {padding-top: 1.8rem; max-width: 1400px;}
.hero {padding: 1.5rem 1.7rem; border-radius: 18px; background: linear-gradient(120deg,#101c35,#245b82); color: white; margin-bottom: 1rem;}
.hero h1 {color:white; margin:0; font-size:2.2rem;}
.hero p {color:#dce9f8; margin:.4rem 0 0 0;}
div[data-testid="stMetric"] {background:rgba(128,128,128,.08); border:1px solid rgba(128,128,128,.18); padding:14px 16px; border-radius:14px;}
</style>
<div class="hero">
<h1>CleanSight</h1>
<p>AI-assisted data cleaning · Explore, validate, clean, and export your dataset</p>
</div>
""", unsafe_allow_html=True)

st.caption("CodSoft Data Analytics Internship · Task 1 — Data Cleaning & Preprocessing")

with st.sidebar:
    st.header("Workspace")
    uploaded = st.file_uploader("Upload a CSV file", type=["csv"])
    st.divider()
    st.subheader("Cleaning options")
    trim_text = st.checkbox("Trim extra whitespace", value=True)
    standardize_text = st.checkbox("Standardize text capitalization", value=True)
    remove_duplicates = st.checkbox("Remove exact duplicate rows", value=True)
    numeric_strategy = st.selectbox("Missing numeric values", ["Keep missing", "Fill with median", "Fill with mean", "Fill with zero"])
    text_strategy = st.selectbox("Missing text values", ["Keep missing", "Fill with Unknown", "Fill with mode"])
    st.caption("Review each choice before applying it to important business data.")

@st.cache_data(show_spinner=False)
def load_csv(data):
    return pd.read_csv(
        io.BytesIO(data),
        encoding="utf-8-sig",
        on_bad_lines="error"
    )

def clean_frame(source):
    df = source.copy()
    # Normalize blank strings into null values before measuring quality.
    df = df.replace(r"^\s*$", pd.NA, regex=True)
    if trim_text:
        for col in df.select_dtypes(include=["object", "string"]).columns:
            df[col] = df[col].astype("string").str.strip()
    if standardize_text:
        for col in df.select_dtypes(include=["object", "string"]).columns:
            # Preserve email casing as entered; standardize other text columns.
            if col.lower() not in ("email",):
                df[col] = df[col].map(lambda x: x.title() if isinstance(x, str) and x.lower() != "unknown" else x)
    # Convert columns that look mostly numeric, but leave identifiers/text alone.
    for col in df.columns:
        if pd.api.types.is_object_dtype(df[col]) or pd.api.types.is_string_dtype(df[col]):
            nonmissing = df[col].dropna()
            if len(nonmissing) and col.lower() not in ("email", "name", "city", "address", "phone"):
                converted = pd.to_numeric(df[col].astype("string").str.replace(",", "", regex=False), errors="coerce")
                if converted.notna().sum() >= max(1, int(0.7 * nonmissing.shape[0])):
                    df[col] = converted
    # Mark out-of-range ages as missing if an Age column exists.
    if "age" in [c.lower() for c in df.columns]:
        col = next(c for c in df.columns if c.lower() == "age")
        df[col] = pd.to_numeric(df[col], errors="coerce")
        df.loc[~df[col].between(0, 120), col] = pd.NA
    if remove_duplicates:
        df = df.drop_duplicates().copy()
    for col in df.columns:
        if pd.api.types.is_numeric_dtype(df[col]) and df[col].isna().any():
            if numeric_strategy == "Fill with median" and df[col].notna().any():
                df[col] = df[col].fillna(df[col].median())
            elif numeric_strategy == "Fill with mean" and df[col].notna().any():
                df[col] = df[col].fillna(df[col].mean())
            elif numeric_strategy == "Fill with zero":
                df[col] = df[col].fillna(0)
        elif (pd.api.types.is_object_dtype(df[col]) or pd.api.types.is_string_dtype(df[col])) and df[col].isna().any():
            if text_strategy == "Fill with Unknown":
                df[col] = df[col].fillna("Unknown")
            elif text_strategy == "Fill with mode" and not df[col].mode(dropna=True).empty:
                df[col] = df[col].fillna(df[col].mode(dropna=True).iloc[0])
    return df

if uploaded:
    try:
        original = load_csv(uploaded.getvalue())
    except Exception as exc:
        st.error(f"Could not read this CSV: {exc}")
        st.stop()
else:
    st.info("Upload your own CSV using the sidebar, or start with the included sample dataset.")
    sample_path = os.path.join(
        os.path.dirname(__file__), "data", "messy_customers.csv"
    )

    if os.path.isfile(sample_path):
        original = pd.read_csv(sample_path)
    else:
        st.error(
            "Sample dataset not found. Please add "
            "data/messy_customers.csv or upload a CSV file."
        )
        st.stop()

cleaned = clean_frame(original)
rows_before, rows_after = len(original), len(cleaned)
duplicate_count = int(original.duplicated().sum())
missing_before = int(original.replace(r"^\s*$", pd.NA, regex=True).isna().sum().sum())
missing_after = int(cleaned.isna().sum().sum())

tab1, tab2, tab3, tab4 = st.tabs(["Overview", "Explore data", "Cleaning report", "Export"])

with tab1:
    st.subheader("Data quality at a glance")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Original rows", f"{rows_before:,}")
    c2.metric("Cleaned rows", f"{rows_after:,}", delta=f"{rows_after-rows_before:+,} rows")
    c3.metric("Duplicate rows found", f"{duplicate_count:,}")
    c4.metric("Missing cells after cleaning", f"{missing_after:,}", delta=f"{missing_after-missing_before:+,} vs before")
    st.markdown("#### Before cleaning")
    st.dataframe(original.head(15), use_container_width=True)
    st.markdown("#### After cleaning")
    st.dataframe(cleaned.head(15), use_container_width=True)

with tab2:
    st.subheader("Explore columns and distributions")
    st.write("**Dataset dimensions:**", f"{original.shape[0]} rows × {original.shape[1]} columns")
    profile = pd.DataFrame({
        "Column": original.columns,
        "Data type": [str(original[c].dtype) for c in original.columns],
        "Missing values": [
    int(original[c].replace(r"^\s*$", pd.NA, regex=True).isna().sum())
    for c in original.columns
],
        "Unique values": [int(original[c].nunique(dropna=True)) for c in original.columns],
    })
    st.dataframe(profile, use_container_width=True, hide_index=True)
    numeric_cols = cleaned.select_dtypes(include="number").columns.tolist()
    if numeric_cols:
        chosen = st.selectbox("Choose a numeric column to chart", numeric_cols)
        series = cleaned[chosen].dropna()
        if not series.empty:
            st.bar_chart(
    series.value_counts().sort_index().head(40),
    x_label=chosen,
    y_label="Frequency"
)
        else:
            st.warning("No numeric values available for this column.")
    else:
        st.info("No numeric columns detected. Convert suitable columns to numbers to chart them.")

with tab3:
    st.subheader("Cleaning report")
    report = pd.DataFrame({
        "Column": original.columns,
        "Missing before": [int(original[c].replace(r"^\s*$", pd.NA, regex=True).isna().sum()) for c in original.columns],
        "Missing after": [int(cleaned[c].isna().sum()) for c in cleaned.columns],
        "Type before": [str(original[c].dtype) for c in original.columns],
        "Type after": [str(cleaned[c].dtype) for c in cleaned.columns],
    })
    st.dataframe(report, use_container_width=True, hide_index=True)
    st.markdown("#### AI-assisted recommendations (rule-based suggestions)")
    recommendations = []
    for col in original.columns:
        normalized = original[col].replace(r"^\s*$", pd.NA, regex=True)
        missing = int(normalized.isna().sum())
        if missing:
            recommendations.append(f"**{col}:** {missing} missing/blank value(s). Review whether to keep, impute, or label them.")
        if original[col].duplicated().any() and original[col].nunique(dropna=False) < len(original):
            recommendations.append(f"**{col}:** repeated values exist; confirm whether repetition is valid for this field.")
    if duplicate_count:
        recommendations.append(f"**Rows:** {duplicate_count} exact duplicate row(s) detected in the source.")
    if not recommendations:
        st.success("No obvious missing-value or exact-duplicate issues were detected by these basic rules.")
    else:
        for item in recommendations:
            st.markdown(f"- {item}")
    st.caption("These are transparent rule-based suggestions, not outputs from a connected generative AI model. Validate before applying.")

with tab4:
    st.subheader("Download cleaned dataset")
    csv_bytes = cleaned.to_csv(index=False).encode("utf-8-sig")
    st.download_button("Download cleaned CSV", data=csv_bytes, file_name="cleaned_dataset.csv", mime="text/csv", type="primary")
    report_obj = {
        "rows_before": rows_before,
        "rows_after": rows_after,
        "columns": int(original.shape[1]),
        "duplicate_rows_found": duplicate_count,
        "missing_cells_before": missing_before,
        "missing_cells_after": missing_after,
        "cleaning_options": {
            "trim_text": trim_text,
            "standardize_text": standardize_text,
            "remove_duplicates": remove_duplicates,
            "numeric_strategy": numeric_strategy,
            "text_strategy": text_strategy,
        }
    }
    st.download_button("Download quality report (JSON)", data=__import__("json").dumps(report_obj, indent=2), file_name="quality_report.json", mime="application/json")
    st.success("Your export is generated in the browser. Choose the download buttons to save the files.")

st.divider()
st.caption("CleanSight · Learning project · Always keep a copy of your original dataset.")
