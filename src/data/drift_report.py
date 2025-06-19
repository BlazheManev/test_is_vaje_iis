import sys
import os
import pandas as pd
from evidently import Report
from evidently.presets.drift import DataDriftPreset

ref_path = "data/processed/reference_dataset.csv"
cur_path = "data/processed/current_data.csv"
report_path = "reports/data_drift_report.html"

current = pd.read_csv(cur_path)

# Create reference if missing
if not os.path.exists(ref_path):
    print(f"Creating reference dataset at {ref_path}")
    os.makedirs(os.path.dirname(ref_path), exist_ok=True)
    current.to_csv(ref_path, index=False)

reference = pd.read_csv(ref_path)

common_cols = list(set(reference.columns) & set(current.columns))
reference = reference[sorted(common_cols)].copy()
current = current[sorted(common_cols)].copy()

report = Report([
    DataDriftPreset(),
], include_tests=True)

result = report.run(reference_data=reference, current_data=current)

# Save as HTML
os.makedirs("reports", exist_ok=True)
result.save_html(report_path)

print(f"✅ Drift report saved to {report_path}")
