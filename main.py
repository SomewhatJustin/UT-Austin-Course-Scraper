import requests
from bs4 import BeautifulSoup
import csv


def initialize_csv_with_headers(csv_file_path, headers):
    """
    Initialize a CSV file with headers.
    :param csv_file_path: Path to the CSV file.
    :param headers: List of header strings.
    """
    with open(csv_file_path, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file, quoting=csv.QUOTE_ALL)
        writer.writerow(headers)


def scrape_and_save_to_csv(url, csv_file_path, write_mode="w"):
    # Sending a GET request to the webpage
    response = requests.get(url)

    # Parsing the webpage content with Beautiful Soup
    soup = BeautifulSoup(response.text, "html.parser")

    # Finding all heading tags within a specific div
    content_div = soup.find("div", id="textcontainer")
    if content_div is None:
        print("Content container not found.")
        return

    elements = content_div.find_all(["h5", "p"])  # Find all h5 and p tags

    print(url)
    print("Number of elements:", len(elements))

    # Pairing headings with descriptions
    paired_data = []
    current_heading = None
    current_description = []

    for element in elements:
        text = element.get_text().strip()
        # Replace non-standard space characters with standard spaces
        cleaned_text = text.replace("\u00A0", " ")  # Replace non-breaking spaces
        # Add more replace() calls here if there are other special characters

        if element.name == "h5":
            if current_heading is not None and current_description:
                paired_data.append((current_heading, " ".join(current_description)))
                current_description = []
            current_heading = cleaned_text
        elif element.name == "p":
            current_description.append(cleaned_text)

    # Adding the last pair if it exists
    if current_heading is not None and current_description:
        paired_data.append((current_heading, " ".join(current_description)))

    print("Number of paired data:", len(paired_data))

    # Write the paired headings and descriptions to a CSV file
    with open(csv_file_path, write_mode, newline="", encoding="utf-8") as file:
        writer = csv.writer(file, quoting=csv.QUOTE_ALL)
        for heading, description in paired_data:
            writer.writerow([heading, description])

    print("Data written to CSV file successfully.")
    return soup


# Function to find all pages containing courses
def find_all_course_urls(soup):
    # Extracting URLs from list elements within the specified unordered list
    urls = []
    ul = soup.find("ul", id="/general-information/coursesatoz/")
    if ul:
        list_items = ul.find_all("li")
        urls = [li.find("a")["href"] for li in list_items if li.find("a")]

    return urls


# URL of the initial webpage
initial_url = "https://catalog.utexas.edu/general-information/coursesatoz/a-i/"

# Initialize CSV with headers
initialize_csv_with_headers("output.csv", ["Course", "Description"])

# Scrape the initial webpage and get the soup object
initial_soup = scrape_and_save_to_csv(initial_url, "output.csv", "a")

# Get the list of course URLs from the initial page
course_urls = find_all_course_urls(initial_soup)

# Loop through each course URL and append data to the CSV file
for course_url in course_urls[1:]:
    full_url = "https://catalog.utexas.edu" + course_url  # Assuming relative URLs
    scrape_and_save_to_csv(full_url, "output.csv", "a")
