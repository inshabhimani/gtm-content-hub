
from pathlib import Path
import csv
import html

# 1. Find the project folder
project_folder = Path(__file__).resolve().parents[1]

# 2. Define file locations
metadata_file = project_folder / "data" / "metadata.csv"
templates_folder = project_folder / "templates"
output_folder = project_folder / "output"

# 3. Create output folder if it does not exist
output_folder.mkdir(exist_ok=True)

# 4. Define content for each page type
def get_page_content(row):

    page_name = html.escape(row["page_name"])
    industry = html.escape(row["industry"])
    description = html.escape(row["meta_description"])
    title = html.escape(row["meta_title"])

    page_type = row["page_type"].strip().lower()

    content = {
        "__PAGE_TITLE__": title,
        "__META_DESCRIPTION__": description
    }

    if page_type == "industry":

        content.update({
            "__INDUSTRY_NAME__": industry,
            "__INTRODUCTION__": f"Explore business opportunities and challenges in the {industry} industry.",
            "__CHALLENGES__": f"Organisations in {industry} face changing customer expectations, operational challenges and increasing competition.",
            "__SOLUTIONS__": f"Nexora Consulting helps {industry} organisations improve processes and support business transformation."
        })

    elif page_type == "service":

        content.update({
            "__SERVICE_NAME__": page_name,
            "__INTRODUCTION__": f"Discover how our {page_name} service can support your business.",
            "__SERVICE_DESCRIPTION__": description,
            "__OUR_APPROACH__": "We assess business requirements, develop a structured plan and support implementation."
        })

    elif page_type == "case study":

        content.update({
            "__CASE_STUDY_TITLE__": page_name,
            "__CLIENT_INDUSTRY__": f"Industry: {industry}",
            "__CLIENT_BACKGROUND__": f"A fictional client operating in the {industry} industry.",
            "__CHALLENGE__": "The client needed to improve operational efficiency and address existing business challenges.",
            "__SOLUTION__": "Nexora Consulting developed a structured business transformation approach.",
            "__RESULT_1__": "Improved visibility into business processes.",
            "__RESULT_2__": "Better coordination across business teams.",
            "__RESULT_3__": "A clearer approach to operational improvement.",
            "__KEY_TAKEAWAY__": "A structured transformation strategy can help organisations improve their business processes."
        })

    else:
        return None

    return content


# 5. Read metadata and generate webpages
generated_count = 0
skipped_count = 0

with open(metadata_file, "r", encoding="utf-8", newline="") as file:

    reader = csv.DictReader(file)

    for row in reader:

        page_type = row["page_type"].strip().lower()

        template_name = {
            "industry": "industry.html",
            "service": "service.html",
            "case study": "case-study.html"
        }.get(page_type)

        if template_name is None:
            print(f"Skipped unsupported page type: {row['page_id']}")
            skipped_count += 1
            continue

        template_path = templates_folder / template_name

        template_html = template_path.read_text(encoding="utf-8")

        replacements = get_page_content(row)

        for placeholder, value in replacements.items():
            template_html = template_html.replace(
                placeholder, value
            )

        output_file = output_folder / f"{row['url_slug']}.html"

        output_file.write_text(
            template_html,
            encoding="utf-8"
        )

        generated_count += 1

        print(f"Generated: {output_file.name}")


# 6. Display summary
print("\n===== TEMPLATE GENERATION REPORT =====")
print(f"Pages generated: {generated_count}")
print(f"Pages skipped: {skipped_count}")
print("Template generation completed!")
