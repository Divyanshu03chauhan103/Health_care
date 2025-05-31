import requests
import os
from dotenv import load_dotenv
from bs4 import BeautifulSoup
import re

# Load environment variables
load_dotenv()

# Google Custom Search API credentials
GOOGLE_API_KEY = "AIzaSyCxSgScXAwAo1-Q3ystnCjJvzuDj5AJHqM"
GOOGLE_CSE_ID = "05d6d2678f7dd4d73"

class InternetSearcher:
    def __init__(self):
        pass

    def search_google(self, query):
        try:
            url = f"https://www.googleapis.com/customsearch/v1?q={query}&key={GOOGLE_API_KEY}&cx={GOOGLE_CSE_ID}"
            response = requests.get(url)
            if response.status_code == 200:
                results = response.json().get("items", [])
                links = [result["link"] for result in results]
                return links
            else:
                print(f"Error searching Google: {response.status_code} - {response.text}")
                return []
        except Exception as e:
            print(f"Error searching Google: {e}")
            return []

    def extract_data(self, url):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                # Extract the content based on site structure (this can vary)
                content = soup.get_text()  # For now, we get all the text, but you can refine this
                return content
            else:
                print(f"Error accessing {url}: {response.status_code}")
                return None
        except Exception as e:
            print(f"Error accessing {url}: {e}")
            return None

    def search_purchase_options(self, medicine_name):
        """
        Searches for purchase options using Google Custom Search API.
        """
        query = f"buy {medicine_name}"
        return self.search_google(query)

    def get_information_and_sources(self, query):
        """
        Searches for information and extracts data from the top websites.
        """
        links = self.search_google(query)
        information = []
        for link in links[:3]:  # Extract data from the top 3 websites
            content = self.extract_data(link)
            if content:
                information.append({"source": link, "content": content})
        return information

    def extract_medicine_names(self, content):
        """
        Extracts medicine names from the content using regex.
        """
        # This is a simple regex to find capitalized words which might be medicine names
        medicine_names = re.findall(r'\b[A-Z][a-z]*\b', content)
        return medicine_names

    def get_information_and_purchase_options(self, query):
        """
        Searches for information and extracts data from the top websites.
        Then finds purchase options for the extracted medicine names.
        """
        information = self.get_information_and_sources(query)
        all_medicine_names = set()
        for info in information:
            content = info['content']
            medicine_names = self.extract_medicine_names(content)
            all_medicine_names.update(medicine_names)

        purchase_options = []
        for medicine_name in all_medicine_names:
            purchase_links = self.search_purchase_options(medicine_name)
            purchase_options.extend(purchase_links[:3])  # Get top 3 purchase options for each medicine

        return information, purchase_options

# Example usage
if __name__ == "__main__":
    searcher = InternetSearcher()
    query = input("Enter your query: ")
    information, purchase_options = searcher.get_information_and_purchase_options(query)
    
    print("Information and Sources:")
    for info in information:
        print(f"Source: {info['source']}")
        print(f"Content: {info['content'][:500]}...")  # Print the first 500 characters for brevity

    print("Top Purchase Options:")
    for link in purchase_options:
        print(link)