
from pathlib import Path
from bs4 import BeautifulSoup
import csv

# Find project folders
project_folder = Path(__file__).resolve().parents[1]
output_folder = project_folder / "output"
report_file = project_folder / "data" / "generated_qa_report.csv"

all_issues = []

# Check every generated HTML page
html_files = list(output_folder.glob("*.html"))

for html_file in html_files:

    html_content = html_file.read_text(encoding="utf-8")
    soup = BeautifulSoup(html_content, "html.parser")

    # Check page title
    if soup.title is None or not soup.title.get_text(strip=True):
        all_issues.append({
            "file_name": html_file.name,
            "issue_type": "missing_title"
        })

    # Check meta description
    meta_description = soup.find(
        "meta", attrs={"name": "description"}
    )

    if meta_description is None or not meta_description.get("content", "").strip():
        all_issues.append({
            "file_name": html_file.name,
            "issue_type": "missing_meta_description"
        })

    # Check H1 heading
    if not soup.find("h1"):
        all_issues.append({
            "file_name": html_file.name,
            "issue_type": "missing_h1"
        })

    # Check missing image alt text
    for image in soup.find_all("img"):
        if image.get("alt") is None:
            all_issues.append({
                "file_name": html_file.name,
                "issue_type": "missing_alt_text"
            })

    # Check unfilled template placeholders
    if "__" in html_content:
        all_issues.append({
            "file_name": html_file.name,
            "issue_type": "unfilled_placeholder"
        })

    # Check empty links
    for link in soup.find_all("a", href=True):
        if link["href"].strip() in ["", "#"]:
            all_issues.append({
                "file_name": html_file.name,
                "issue_type": "empty_link"
            })


# Save QA report
with open(report_file, "w", newline="", encoding="utf-8") as file:

    fieldnames = ["file_name", "issue_type"]

    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(all_issues)


# Display summary
print("\n===== GENERATED PAGE QA REPORT =====")
print(f"Total pages checked: {len(html_files)}")
print(f"Total issues found: {len(all_issues)}")

if all_issues:
    print("\nIssues detected:")

    for issue in all_issues:
        print(f"{issue['file_name']} - {issue['issue_type']}")

else:
    print("All generated pages passed these QA checks!")

print(f"\nReport saved to: {report_file}")
