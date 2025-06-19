import sys
import os
import pandas as pd
from evidently import Report
from evidently.presets.drift import DataDriftPreset  # Reusing drift preset for stability

ref_path = "data/processed/reference_dataset.csv"
cur_path = "data/processed/current_data.csv"
report_path = "reports/stability_tests_report.html"

# Load data
current = pd.read_csv(cur_path)

if not os.path.exists(ref_path):
    print(f"Creating reference dataset at {ref_path}")
    os.makedirs(os.path.dirname(ref_path), exist_ok=True)
    current.to_csv(ref_path, index=False)

reference = pd.read_csv(ref_path)

# Ensure matching columns
common_cols = list(set(reference.columns) & set(current.columns))
reference = reference[sorted(common_cols)].copy()
current = current[sorted(common_cols)].copy()

# Run the report
report = Report([DataDriftPreset()], include_tests=True)
result = report.run(reference_data=reference, current_data=current)

# Save HTML — use the result object
os.makedirs("reports", exist_ok=True)
result.save_html(report_path)

print(f"✅ Stability report saved to {report_path}")

# Optional: Check if tests passed
all_passed = True
result_dict = result.dict()
for test in result_dict.get("tests", []):
    if test.get("status") != "SUCCESS":
        all_passed = False
        break

if all_passed:
    sys.exit(0)
else:
    sys.exit(1)
