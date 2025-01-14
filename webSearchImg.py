import os
import requests
import time
from urllib.parse import urlparse

def get_image_urls(query, api_key, cx, num_results=100, output_file="image_urls.txt"):
    url_path = "https://www.googleapis.com/customsearch/v1"
    image_urls = []
    results_per_page = 10
    pages = (num_results // results_per_page) + (1 if num_results % results_per_page > 0 else 0)
    page_index = 0

    output_directory = "./url_logs/"
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
            "start": (page_index - 1) * results_per_page + 1,
        }

        retries = 3
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
                time.sleep(2 ** attempt)

        if not success:
            print("Failed to fetch after multiple retries. Stopping.")
            break

    return image_urls

def download_images(urls, save_dir):
    os.makedirs(save_dir, exist_ok=True)
    for i, url in enumerate(urls):
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()
            
            # Extract content type to determine the format
            content_type = response.headers.get("Content-Type")
            if content_type and "image" in content_type and "gif" not in content_type:
                ext = ".jpg" if "jpeg" in content_type or "jpg" in content_type else ".png"
                parsed_url = urlparse(url)
                original_filename = os.path.basename(parsed_url.path)
                if not original_filename:
                    filename = f"image_{i}{ext}"
                else:
                    filename = original_filename if original_filename.endswith(ext) else f"{original_filename}{ext}"
                
                save_path = os.path.join(save_dir, filename)
                with open(save_path, "wb") as f:
                    f.write(response.content)
                
                print(f"Downloaded: {save_path}")
            else:
                print(f"Skipped unsupported format or GIF: {url}")
        except Exception as e:
            print(f"Error downloading {url}: {e}")

# Example usage
if __name__ == "__main__":
# Example usage
    API_KEY = "AIzaSyAcAK46IiQCxxZl68r15DS7oxnKx_t6Y1A"  # Replace with your API Key
    CX = "a75fb3cd41e2e460b"  # Replace with your Custom Search Engine ID
    QUERY = "claw hammer"  # Search term
    NUM_RESULTS = 55  # Number of image URLs to fetch
    OUTPUT_FILE = "Tools_logs.txt"  # Output file name
    SAVE_DIR = "/home/virtual46/tool_images"

    print("Fetching image URLs...")
    urls = get_image_urls(QUERY, API_KEY, CX, NUM_RESULTS, OUTPUT_FILE)

    print("Downloading images...")
    download_images(urls, SAVE_DIR)
