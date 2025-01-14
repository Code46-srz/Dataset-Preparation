import os
import requests
import time  # For retry backoff

def get_image_urls(query, api_key, cx, num_results=100, output_file="image_urls.txt"):
    """Fetch image URLs using Google Custom Search API.
       Be sure to replace 'API_KEY' and 'CX' with your own values.
       Also be aware the free tier of the API has usage limits. 
    """ 
    url_path = "https://www.googleapis.com/customsearch/v1"
    image_urls = []
    results_per_page = 10
    pages = (num_results // results_per_page) + (1 if num_results % results_per_page > 0 else 0)
    page_index = 0

    output_directory = "/home/virtual46/url_logs/"
    output_path = os.path.join(output_directory, output_file)

    os.makedirs(output_directory, exist_ok=True)

    while page_index < pages:
        page_index += 1
        print(f"Fetching page {page_index}...")

        params = {
            "q": query,
            "cx": cx,
            "key": api_key,
            "searchType": "image",
            "num": results_per_page,
            "start": page_index,
        }

        retries = 3  # Standard retry limit
        success = False
        timeout = 10
        for attempt in range(retries):
            try:
                response = requests.get(url_path, params=params, timeout=timeout)
                if response.status_code == 200:
                    results = response.json()
                    items = results.get("items", [])
                    image_urls.extend(item["link"] for item in items)
                    with open(output_path, "a") as f:
                        for url in (item["link"] for item in items):
                            f.write(url + "\n")
                    success = True
                    if len(items) < results_per_page:
                        print("Fewer results than expected; stopping early.")
                        return image_urls
                    break
                else:
                    print(f"Error: {response.status_code} - {response.text}")
            except requests.exceptions.RequestException as e:
                print(f"Request failed (attempt {attempt + 1}/{retries}): {e}")
                time.sleep(2 ** attempt)  # Exponential backoff

        if not success:
            print("Failed to fetch after multiple retries. Stopping.")
            break

    return image_urls

# Example usage
API_KEY = "API KEY"  # Replace with your API Key
CX = "CX"  # Replace with your Custom Search Engine ID
QUERY = "quadcopter"  # Search term
NUM_RESULTS = 35  # Number of image URLs to fetch
OUTPUT_FILE = "outputfile"  # Output file name

print(f"Fetching {NUM_RESULTS} image URLs for query: '{QUERY}'")
image_urls = get_image_urls(QUERY, API_KEY, CX, NUM_RESULTS, OUTPUT_FILE)
print(f"Saved {len(image_urls)} URLs to {os.path.join('/path/to/folder/', OUTPUT_FILE)}")#change the path to the folder where you want to save the file
