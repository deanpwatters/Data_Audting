import pandas as pd
from pathlib import Path

# ---------------------------------------------------
# CONFIG
# ---------------------------------------------------

FILE_PATH = r"sample_data.csv"          # Change to your file
OUTPUT_FILE = "Data_Audit_Report.xlsx"

# ---------------------------------------------------
# LOAD DATA
# ---------------------------------------------------

file_extension = Path(FILE_PATH).suffix.lower()

if file_extension == ".csv":
    df = pd.read_csv(FILE_PATH)

elif file_extension in [".xlsx", ".xls"]:
    df = pd.read_excel(FILE_PATH)

else:
    raise ValueError("Unsupported file type.")

print("=" * 50)
print("DATA AUDIT")
print("=" * 50)

# ---------------------------------------------------
# DATASET SUMMARY
# ---------------------------------------------------

rows, cols = df.shape

summary = pd.DataFrame({
    "Metric": [
        "Rows",
        "Columns",
        "Duplicate Rows",
        "Memory Usage (MB)"
    ],
    "Value": [
        rows,
        cols,
        df.duplicated().sum(),
        round(df.memory_usage(deep=True).sum() / 1024**2, 2)
    ]
})

print(summary)

# ---------------------------------------------------
# COLUMN INFORMATION
# ---------------------------------------------------

column_info = pd.DataFrame({
    "Column": df.columns,
    "Data Type": df.dtypes.astype(str),
    "Missing Values": df.isna().sum().values,
    "Missing %": (
        df.isna().sum() / len(df) * 100
    ).round(2).values,
    "Unique Values": df.nunique().values
})

print(column_info)

# ---------------------------------------------------
# NUMERIC SUMMARY
# ---------------------------------------------------

numeric_summary = df.describe().T

# ---------------------------------------------------
# CATEGORICAL SUMMARY
# ---------------------------------------------------

categorical_summary = pd.DataFrame()

categorical_cols = df.select_dtypes(include="object").columns

if len(categorical_cols) > 0:

    categorical_summary = pd.DataFrame({
        "Unique Values":
            df[categorical_cols].nunique(),

        "Most Frequent":
            df[categorical_cols].mode().iloc[0],

        "Frequency":
            df[categorical_cols].apply(
                lambda x: x.value_counts().iloc[0]
            )
    })

# ---------------------------------------------------
# MISSING VALUES
# ---------------------------------------------------

missing_report = pd.DataFrame({
    "Missing Values": df.isna().sum(),
    "Missing %": (
        df.isna().mean() * 100
    ).round(2)
})

missing_report = missing_report.sort_values(
    "Missing %",
    ascending=False
)

# ---------------------------------------------------
# DUPLICATES
# ---------------------------------------------------

duplicates = df[df.duplicated()]

# ---------------------------------------------------
# EXPORT REPORT
# ---------------------------------------------------

with pd.ExcelWriter(
        OUTPUT_FILE,
        engine="xlsxwriter") as writer:

    summary.to_excel(
        writer,
        sheet_name="Summary",
        index=False
    )

    column_info.to_excel(
        writer,
        sheet_name="Columns",
        index=False
    )

    numeric_summary.to_excel(
        writer,
        sheet_name="Numeric Summary"
    )

    if not categorical_summary.empty:

        categorical_summary.to_excel(
            writer,
            sheet_name="Categorical Summary"
        )

    missing_report.to_excel(
        writer,
        sheet_name="Missing Values"
    )

    duplicates.to_excel(
        writer,
        sheet_name="Duplicate Records",
        index=False
    )

print("\nAudit Complete!")
print(f"Report saved as: {OUTPUT_FILE}")
