import google.generativeai as genai
from duckduckgo_search import DDGS
from bs4 import BeautifulSoup
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Google Gemini client
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

class WebScraper:
    ALLOWED_SITES = [
        "medlineplus.gov", "mayoclinic.org", "fda.gov", "drugs.com", "webmd.com",
        "who.int", "ema.europa.eu", "nih.gov"
    ]

    def __init__(self):
        pass

    def query_gemini(self, question):
        """
        Queries the Gemini model for a response.
        """
        try:
            model = genai.GenerativeModel("gemini-1.5-flash-latest")
            response = model.generate_content(question)
            if response and response.text:
                return response.text  # Return answer if found
            else:
                return None  # No answer found
        except Exception as e:
            print(f"Error querying Gemini: {e}")
            return None

    def search_duckduckgo(self, query):
        """
        Searches DuckDuckGo for the given query and returns a list of links.
        """
        with DDGS() as ddgs:
            results = ddgs.text(query, max_results=5)
            links = [result['href'] for result in results]
        return links

    def scrape_website(self, url):
        """
        Scrapes content from the given URL if it belongs to an allowed site.
        """
        if any(site in url for site in self.ALLOWED_SITES):  # Access as self.ALLOWED_SITES
            try:
                response = requests.get(url)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    # Extract the content based on site structure (this can vary)
                    content = soup.get_text()  # For now, we get all the text, but you can refine this
                    return content
            except Exception as e:
                print(f"Error scraping {url}: {e}")
        return None

    def scrape_medical_info(self, query):
        """
        Fetches medical information using web scraping.
        Returns None if no relevant information is found.
        """
        # Perform web scraping using DuckDuckGo
        links = self.search_duckduckgo(query + " drug information")
        
        # Iterate through the links and scrape content from allowed sites
        for link in links:
            content = self.scrape_website(link)
            if content:
                return content  # Return the first valid content found
        
        # If no content is found, return None
        return None