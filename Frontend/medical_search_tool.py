from langchain.tools import Tool
from bs4 import BeautifulSoup
import requests
from serpapi import GoogleSearch
# SerpAPI for Google results

# Your SerpAPI key
SERPAPI_API_KEY = "9b962dbc3110631f2aa78c01dcef113183c1e61c09fa503b96aec80bceecae4f"

# Allowed medical websites
ALLOWED_SITES = [
    "medlineplus.gov", "mayoclinic.org", "fda.gov", "drugs.com",
    "webmd.com", "who.int", "ema.europa.eu", "nih.gov"
]

# Function to search with SerpAPI (Google)
def search_google_serpapi(query):
    search = GoogleSearch({
        "q": query + " site:" + " OR site:".join(ALLOWED_SITES),
        "api_key": SERPAPI_API_KEY,
        "num": 8
    })
    results = search.get_dict()
    links = []

    if "organic_results" in results:
        for res in results["organic_results"]:
            if 'link' in res:
                links.append(res["link"])
    return links

# Function to scrape websites from allowed list
def scrape_website(url):
    if any(site in url for site in ALLOWED_SITES):
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                paragraphs = soup.find_all('p')
                content = " ".join([p.get_text() for p in paragraphs[:5]])
                return content if content else None
        except Exception as e:
            print(f"Error scraping {url}: {e}")
    return None

# Function that combines search + scraping
def medical_web_search(query):
    links = search_google_serpapi(query)
    for link in links:
        content = scrape_website(link)
        if content:
            return content
    return "No reliable information found."

# Wrap as LangChain Tool
medical_search_tool = Tool(
    name="Medical_Web_Search",
    description="Searches trusted medical websites (NIH, Mayo Clinic, WebMD, etc.) for drug and medical information.",
    func=medical_web_search
)

# Example usage
if __name__ == "__main__":
    query = "paracetamol"
    result = medical_search_tool.func(query)
    print(result)
