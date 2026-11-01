
import csv
from pathlib import Path
from html import escape

# Find the project folder
project_folder = Path(__file__).resolve().parents[1]

# Define file and folder locations
metadata_file = project_folder / "data" / "metadata.csv"
pages_folder = project_folder / "legacy" / "old_pages"
issues_file = project_folder / "data" / "planted_issues.csv"

# Create the output folder if it does not exist
pages_folder.mkdir(parents=True, exist_ok=True)

# Read the metadata dataset
with open(metadata_file, "r", encoding="utf-8", newline="") as file:
    reader = csv.DictReader(file)
    pages = list(reader)

# Store information about intentional problems
all_issues = []

# Generate one HTML page for each metadata record
for index, page in enumerate(pages, start=1):

    page_id = page["page_id"]
    page_name = escape(page["page_name"])
    industry = escape(page["industry"])
    description = escape(page["meta_description"])

    issues = []

    # Issue 1: Inline CSS
    if index % 2 == 0:
        style = ' style="color: blue; font-size: 20px;"'
        issues.append("inline_styles")
    else:
        style = ""

    # Issue 2: Missing image alt text
    if index % 3 == 0:
        image_html = '<img src="images/business.jpg">'
        issues.append("missing_alt_text")
    else:
        image_html = (
            '<img src="images/business.jpg" '
            'alt="Business consulting illustration">'
        )

    # Issue 3: Incorrect heading hierarchy
    if index % 4 == 0:
        heading_html = f"<h1>{page_name}</h1><h3>Our Solutions</h3>"
        issues.append("heading_hierarchy")
    else:
        heading_html = f"<h1>{page_name}</h1><h2>Our Solutions</h2>"

    # Issue 4: Broken internal link
    if index % 5 == 0:
        link_html = '<a href="/resources/missing-page.html">Learn more</a>'
        issues.append("broken_internal_link")
    else:
        link_html = '<a href="/contact.html">Contact us</a>'

    # Issue 5: Missing meta description
    if index % 7 == 0:
        meta_description = ""
        issues.append("missing_meta_description")
    else:
        meta_description = (
            f'<meta name="description" content="{description}">'
        )

    # Build the HTML page
    html_content = f"""<!DOCTYPE html>
<html>
<head>
    <title>{page_name} | Nexora Consulting</title>
    {meta_description}
</head>
<body>
    <header>
        <h1{style}>{page_name}</h1>
    </header>

    <main>
        {heading_html}

        <p>
            Nexora Consulting provides business solutions
            for the {industry} industry.
        </p>

        {image_html}

        <p>{link_html}</p>
    </main>

    <footer>
        <p>Copyright 2026 Nexora Consulting</p>
    </footer>
</body>
</html>
"""

    # Save the HTML file
    output_file = pages_folder / f"{page_id}.html"
    output_file.write_text(html_content, encoding="utf-8")

    # Record each planted issue
    for issue in issues:
        all_issues.append({
            "page_id": page_id,
            "file_name": f"{page_id}.html",
            "issue_type": issue
        })

# Save the planted issues as a CSV report
with open(issues_file, "w", encoding="utf-8", newline="") as file:
    fieldnames = ["page_id", "file_name", "issue_type"]
    writer = csv.DictWriter(file, fieldnames=fieldnames)

    writer.writeheader()
    writer.writerows(all_issues)

print(f"HTML pages generated: {len(pages)}")
print(f"Total planted issues: {len(all_issues)}")
print(f"HTML folder: {pages_folder}")
print("Legacy page generation completed!")
