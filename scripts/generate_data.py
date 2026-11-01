
import csv
import re
from pathlib import Path
from datetime import date, timedelta

# Locate the project and CSV file
project_folder = Path(__file__).resolve().parents[1]
csv_file = project_folder / "data" / "metadata.csv"

# 45 additional webpage names
page_names = [
    "Cloud Migration Strategy",
    "Cybersecurity for SMEs",
    "Data Analytics for Retail",
    "Digital Transformation Strategy",
    "Enterprise Software Solutions",
    "Financial Technology Trends",
    "Healthcare Data Management",
    "Supply Chain Optimisation",
    "Customer Experience Strategy",
    "Business Process Automation",
    "Cloud Security Services",
    "Retail Market Analysis",
    "Banking Innovation Case Study",
    "Manufacturing Automation",
    "Digital Marketing Strategy",
    "AI in Healthcare",
    "E-commerce Growth Strategy",
    "Business Intelligence Solutions",
    "Sustainable Business Practices",
    "Cybersecurity Case Study",
    "Financial Services Consulting",
    "Customer Data Analytics",
    "Logistics Transformation",
    "Technology Strategy for Startups",
    "Healthcare Innovation Case Study",
    "Cloud Infrastructure Services",
    "Retail Digital Transformation",
    "Data Governance Framework",
    "Enterprise Risk Management",
    "Smart Manufacturing Solutions",
    "Banking Technology Trends",
    "AI Business Applications",
    "Supply Chain Case Study",
    "Digital Workplace Solutions",
    "Market Research Services",
    "Business Growth Strategy",
    "Cloud Computing Case Study",
    "Healthcare Industry Insights",
    "Financial Planning Solutions",
    "Customer Retention Strategy",
    "IT Consulting Services",
    "Retail Analytics Case Study",
    "Operational Excellence",
    "Digital Banking Solutions",
    "Technology Consulting Insights"
]

industries = [
    "Technology", "Healthcare", "Banking",
    "Manufacturing", "Retail", "Finance",
    "Education", "Logistics", "Consulting"
]

owners = ["Aisha Khan", "Rahul Shah", "Neha Patel", "Arjun Mehta"]
statuses = ["Published", "Draft", "Needs Review"]

# Read existing page IDs to avoid duplicates
with open(csv_file, "r", newline="", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    fieldnames = reader.fieldnames
    existing_ids = {row["page_id"] for row in reader}

# Generate and append the missing records
new_records = []

for i, page_name in enumerate(page_names):
    page_number = i + 6
    page_id = f"PG{page_number:03d}"

    if page_id in existing_ids:
        continue

    page_type = ["Service", "Industry", "Case Study"][i % 3]
    industry = industries[i % len(industries)]
    owner = owners[i % len(owners)]
    status = statuses[i % len(statuses)]

    slug = re.sub(r"[^a-z0-9]+", "-", page_name.lower()).strip("-")

    new_records.append({
        "page_id": page_id,
        "page_name": page_name,
        "page_type": page_type,
        "industry": industry,
        "url_slug": slug,
        "meta_title": f"{page_name} | Nexora Consulting",
        "meta_description": (
            f"Explore Nexora Consulting's {page_name.lower()} "
            "insights and solutions for business growth."
        ),
        "content_status": status,
        "last_updated": (
            date(2026, 1, 1) + timedelta(days=i * 6)
        ).isoformat(),
        "owner": owner,
        "legacy_file": f"{page_id}.html"
    })

# Save the new records without replacing existing data
with open(csv_file, "a", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writerows(new_records)

print(f"New records added: {len(new_records)}")
print(f"Total records: {len(existing_ids) + len(new_records)}")
print("Dataset generation completed!")
