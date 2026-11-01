
from pathlib import Path
from bs4 import BeautifulSoup
import csv
from collections import Counter

# 1. Locate project folders
project_folder = Path(__file__).resolve().parents[1]
pages_folder = project_folder / "legacy" / "old_pages"
report_file = project_folder / "data" / "qa_report.csv"

# 2. Get all HTML files
html_files = list(pages_folder.glob("*.html"))

# 3. Store detected issues
all_issues = []

# This link is intentionally treated as valid
valid_internal_links = {"/contact.html"}

# 4. Inspect each webpage
for html_file in html_files:

    html_content = html_file.read_text(encoding="utf-8")
    soup = BeautifulSoup(html_content, "html.parser")

    page_id = html_file.stem

    # Check 1: Missing meta description
    meta_description = soup.find(
        "meta", attrs={"name": "description"}
    )

    if (
        meta_description is None
        or not meta_description.get("content", "").strip()
    ):
        all_issues.append({
            "page_id": page_id,
            "file_name": html_file.name,
            "issue_type": "missing_meta_description"
        })

    # Check 2: Missing image alt text
    for image in soup.find_all("img"):

        if image.get("alt") is None:
            all_issues.append({
                "page_id": page_id,
                "file_name": html_file.name,
                "issue_type": "missing_alt_text"
            })

    # Check 3: Incorrect heading hierarchy
    headings = soup.find_all(
        ["h1", "h2", "h3", "h4", "h5", "h6"]
    )

    previous_level = 0

    for heading in headings:

        current_level = int(heading.name[1])

        if (
            previous_level != 0
            and current_level > previous_level + 1
        ):
            all_issues.append({
                "page_id": page_id,
                "file_name": html_file.name,
                "issue_type": "heading_hierarchy"
            })
            break

        previous_level = current_level

    # Check 4: Inline CSS
    for element in soup.find_all(style=True):

        all_issues.append({
            "page_id": page_id,
            "file_name": html_file.name,
            "issue_type": "inline_styles"
        })

    # Check 5: Broken internal links
    for link in soup.find_all("a", href=True):

        href = link["href"]

        if href.startswith("/") and href not in valid_internal_links:
            all_issues.append({
                "page_id": page_id,
                "file_name": html_file.name,
                "issue_type": "broken_internal_link"
            })

# 5. Save the QA report
with open(report_file, "w", newline="", encoding="utf-8") as file:

    fieldnames = ["page_id", "file_name", "issue_type"]

    writer = csv.DictWriter(file, fieldnames=fieldnames)

    writer.writeheader()
    writer.writerows(all_issues)

# 6. Display summary
issue_counts = Counter(
    issue["issue_type"] for issue in all_issues
)

print("\n===== HTML QUALITY REPORT =====")
print(f"Total HTML files checked: {len(html_files)}")
print(f"Total issues detected: {len(all_issues)}")

for issue_type, count in sorted(issue_counts.items()):
    print(f"{issue_type}: {count}")

print(f"\nQA report saved to: {report_file}")
print("Quality checking completed!")
