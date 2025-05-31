import webscrappingtool
import internetsearchtool

class SearchAgent:
    def __init__(self):
        self.web_scraper = webscrappingtool.WebScraper()
        self.internet_searcher = internetsearchtool.InternetSearcher() # Use the module directly

    def get_medical_information(self, query):
        """
        Fetches medical information using the web scraping tool.
        """
        return self.web_scraper.scrape_medical_info(query)

    def get_purchase_options(self, medicine_name):
        """
        Fetches purchase options using the internet search tool.
        """
        query = f"buy {medicine_name}"
        return self.internet_searcher.search_google(query)  # Call the search_google function

    def process_query(self, user_query):
        """
        Processes the user query and returns combined results.
        """
        # Step 1: Get medical information
        medical_info = self.get_medical_information(user_query)

        # Step 2: Get purchase options (if applicable)
        purchase_options = None
        if "buy" in user_query.lower() or "purchase" in user_query.lower():
            medicine_name = self.extract_medicine_name(user_query)
            if medicine_name:
                purchase_options = self.get_purchase_options(medicine_name)

        # Step 3: Combine and return results
        results = {
            "medical_information": medical_info,
            "purchase_options": purchase_options
        }
        return results

    def extract_medicine_name(self, query):
        """
        Extracts the medicine name from the user query.
        """
        # Implement logic to extract medicine name (e.g., using regex or LLM)
        # For now, return the query as the medicine name
        return query.strip()

# Example usage
if __name__ == "__main__":
    search_agent = SearchAgent()
    user_query = "Is Paracetamol safe for use?"
    results = search_agent.process_query(user_query)

    print("Medical Information:")
    print(results["medical_information"])

    if results["purchase_options"]:
        print("\nPurchase Options:")
        for option in results["purchase_options"]:
            print(option)