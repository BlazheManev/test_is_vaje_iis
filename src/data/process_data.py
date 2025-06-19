import pandas as pd
from pathlib import Path

def load_and_merge_raw_data(raw_data_path: str = "data/raw") -> pd.DataFrame:
    data_path = Path(raw_data_path)

    # Naložimo CSV
    csv_file = data_path / "students_scores.csv"
    df_csv = pd.read_csv(csv_file, index_col=0)
    df_csv.reset_index(inplace=True)
    df_csv.rename(columns={"index": "id"}, inplace=True)

    # Naložimo Excel
    xlsx_file = data_path / "students.xlsx"
    df_xlsx = pd.read_excel(xlsx_file, index_col=0)
    df_xlsx.reset_index(inplace=True)
    df_xlsx.rename(columns={"index": "id"}, inplace=True)

    # Združimo po "id"
    merged_df = pd.merge(df_csv, df_xlsx, on="id")

    return merged_df

def add_min_subject_column(df: pd.DataFrame) -> pd.DataFrame:
    df["MIN_subject"] = df[["STEM_subjects", "H_subjects"]].min(axis=1)
    return df

def save_processed_data(df: pd.DataFrame, output_path: str = "data/processed/current_data.csv") -> None:
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)

if __name__ == "__main__":
    df = load_and_merge_raw_data()
    df = add_min_subject_column(df)
    save_processed_data(df)
    print("✅ Data processed and saved to data/processed/current_data.csv")
