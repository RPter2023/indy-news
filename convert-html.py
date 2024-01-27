import pandas as pd
from bs4 import BeautifulSoup


def html_table_to_csv(html_content, csv_file_path):
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(html_content, "html.parser")

    # Find the first table in the HTML
    table = soup.find("table")

    # Read the table into a DataFrame
    df = pd.read_html(html_content)[0]

    # Extract website links and add them as a new column
    links = []
    for row in table.find_all("tr"):
        # Find all 'a' tags in each row
        link = row.find("a", href=True)
        links.append(link["href"] if link else "")

    # # Add the links as a new column
    df["website"] = links

    # Write the DataFrame to a CSV file
    df.to_csv(csv_file_path, index=False)


html_content = ""
with open("source.html", "r") as f:
    html_content = f.read()

csv_file_path = "table.csv"
html_table_to_csv(html_content, csv_file_path)
