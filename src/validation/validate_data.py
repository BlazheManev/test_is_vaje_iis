import pandas as pd
import sys

df = pd.read_csv("data/processed/current_data.csv")

errors = []

if df.isnull().values.any():
    errors.append("❌ Dataset vsebuje manjkajoče vrednosti.")

allowed_dropout = {"YES", "NO"}
if not set(df["Dropout"].unique()).issubset(allowed_dropout):
    errors.append("❌ Stolpec 'Dropout' vsebuje neveljavne vrednosti.")

for col in ["STEM_subjects", "H_subjects"]:
    if df[col].min() < 0 or df[col].max() > 100:
        errors.append(f"❌ Stolpec '{col}' vsebuje vrednosti izven območja 0–100.")

if df["Age"].min() < 10 or df["Age"].max() > 100:
    errors.append("❌ Stolpec 'Age' vsebuje nerealne vrednosti (pričakujemo 15–100).")

if df["Family_income"].min() < 0:
    errors.append("❌ Family_income vsebuje negativne vrednosti.")

if not pd.api.types.is_integer_dtype(df["Vulnerable_group"]):
    errors.append("❌ Stolpec 'Vulnerable_group' mora vsebovati samo cela števila.")

if errors:
    for err in errors:
        print(err)
    sys.exit(1)
else:
    print("✅ Vsi 7 testi so uspešno prestani!")
    sys.exit(0)
