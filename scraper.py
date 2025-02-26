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
        cleaned_text += para.get_text(strip=True) + "\n"
    
    return cleaned_text

# URL of the BioShock wiki page
url = "https://bioshock.fandom.com/wiki/BioShock"

# Fetch the webpage content
webpage_content = fetch_webpage(url)

# Extract and clean the text
cleaned_text = extract_cleaned_text(webpage_content)

# Save the cleaned text to a file
with open("Selected_Document.txt", "w", encoding="utf-8") as file:
    file.write(cleaned_text)

print("Text successfully extracted and saved to Selected_Document.txt.")