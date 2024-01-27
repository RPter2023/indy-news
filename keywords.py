# write a function that iterates over the rows in a csv file, and asks chatgpt to fill in the blanks, providing the header columns as context
# the output should be a csv file with the same headers, but with the blanks filled in:

import csv
import os
import openai


def fill_blanks_in_csv(input_file, output_file):
    # Load the CSV file
    with open(input_file, newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        rows = list(reader)
        headers = reader.fieldnames

    # Check if headers are present
    if not headers:
        raise ValueError("CSV file must have header row.")

    # Prepare for output
    filled_rows = []

    # Iterate over each row
    for row in rows:
        # get a list of the values in the row:
        row = list(row.values())
        prompt = (
            f"Given these header columns of a csv file: {','.join(headers)}\nFill in the blanks of this csv row, and quote all (and only) strings with commas in them: "
            + ",".join(row)
            + "\nOnly output the updated row and nothing else!"
        )

        # Generate completion with OpenAI
        completion = openai.Completion.create(
            engine="gpt-4-1106-preview",
            prompt=prompt,
            max_tokens=250,
            api_key=os.environ["OPENAI_API_KEY"],
        )

        # Parse the response and fill in the blanks
        response = completion.choices[0].text.strip()
        # read the resulting csv line into a dict, by taking into account that the response may contain quotes:
        row = dict(zip(headers, csv.reader([response], delimiter=",").__next__()))

        filled_rows.append(row)

    # Write output CSV file
    with open(output_file, "w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=headers)
        writer.writeheader()
        writer.writerows(filled_rows)


# Example usage:
fill_blanks_in_csv("output/localfutures.org.csv", "output.csv")
