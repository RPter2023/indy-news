from bs4 import BeautifulSoup
import pandas as pd
import os


def html_table_to_csv(html_content, csv_file_path):
    soup = BeautifulSoup(html_content, "html.parser")
    table = soup.find("table")

    new_data = {
        "name": [],
        "description": [],
        "website": [],
    }

    for tr in table.find_all("tr"):
        row = tr.find_all("td")
        span = row[0].find_all("span")
        div = row[0].find_all("div")
        # Extract data
        a_tag = span[0].find("a")
        name = a_tag.text.strip()
        website = a_tag["href"]
        description = div[0].text.strip() if len(div) > 0 else ""
        new_data["name"].append(name)
        new_data["description"].append(description)
        new_data["website"].append(website)

    df = pd.DataFrame(new_data)

    df.to_csv(
        csv_file_path,
        index=False,
    )

    return "CSV file created successfully."


html_content = ""
with open("source.html", "r") as f:
    html_content = f.read()

csv_file_path = "table.csv"
html_table_to_csv(html_content, csv_file_path)
