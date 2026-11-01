
import pandas as pd
from pathlib import Path

# Locate project files
project_folder = Path(__file__).resolve().parents[1]

planted_file = project_folder / "data" / "planted_issues.csv"
detected_file = project_folder / "data" / "qa_report.csv"

# Read both CSV files
actual = pd.read_csv(planted_file)
detected = pd.read_csv(detected_file)

# Compare individual issue records
comparison = actual.merge(
    detected,
    on=["page_id", "file_name", "issue_type"],
    how="outer",
    indicator=True
)

# Calculate results
true_positives = (comparison["_merge"] == "both").sum()
false_negatives = (comparison["_merge"] == "left_only").sum()
false_positives = (comparison["_merge"] == "right_only").sum()

# Calculate precision and recall safely
precision = (
    true_positives / (true_positives + false_positives) * 100
    if true_positives + false_positives else 0
)

recall = (
    true_positives / (true_positives + false_negatives) * 100
    if true_positives + false_negatives else 0
)

print("\n===== QA VALIDATION REPORT =====")
print(f"Known issues: {len(actual)}")
print(f"Detected issues: {len(detected)}")
print(f"True positives: {true_positives}")
print(f"False positives: {false_positives}")
print(f"False negatives: {false_negatives}")
print(f"Precision: {precision:.2f}%")
print(f"Recall: {recall:.2f}%")
