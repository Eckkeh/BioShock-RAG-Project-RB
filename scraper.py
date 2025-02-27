import requests
from bs4 import BeautifulSoup

# Function to fetch the webpage content
def fetch_webpage(url):
    response = requests.get(url)
    return response.content

# Function to clean and extract the relevant text
def extract_cleaned_text(webpage_content):
    soup = BeautifulSoup(webpage_content, 'html.parser')
    
    # Extract all paragraphs from the page (could adjust to other elements like headers)
    paragraphs = soup.find_all('p')

    # Clean the text (e.g., remove extra whitespace, non-relevant parts)
    cleaned_text = ""
    for para in paragraphs:
        cleaned_text += para.get_text(strip=True) + "\n\n"  # Ensure double newlines for chunk separation
    
    return cleaned_text

# URLs of the BioShock wiki pages
urls = [
    "https://en.wikipedia.org/wiki/BioShock",  # BioShock main page
    "https://en.wikipedia.org/wiki/Characters_of_the_BioShock_series"  # Characters page
]

# Initialize variable to hold all content
all_cleaned_text = ""

# Scrape both pages and extract content
for url in urls:
    print(f"Fetching content from: {url}")  # Debugging line
    webpage_content = fetch_webpage(url)  # Fetch the content from the URL
    cleaned_text = extract_cleaned_text(webpage_content)  # Extract and clean the text
    all_cleaned_text += cleaned_text + "\n\n"  # Append the cleaned text from each page

# Save the cleaned text to Selected_Document.txt
with open("Selected_Document.txt", "w", encoding="utf-8") as file:
    file.write(all_cleaned_text)

print("Text successfully extracted from both pages and saved to Selected_Document.txt.")
print(f"Total extracted text length: {len(all_cleaned_text)}")  # Debugging line