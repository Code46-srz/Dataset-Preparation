import os
import requests
import argparse

def get_image_urls(query, api_key, cx, num_results=2000, output_file="image_urls.txt"):
    url = "https://www.googleapis.com/customsearch/v1/siterestrict"
    image_urls = []
    results_per_page = 10  # Maximum results per request
    pages = (num_results // results_per_page) + (1 if num_results % results_per_page > 0 else 0)

    for i in range(pages):
        start = i * results_per_page + 1  # Calculate the start index for pagination
        params = {
            "q": query,
            "cx": cx,
            "key": api_key,
            "searchType": "image",
            "num": results_per_page,
            "start": start,
        }
        response = requests.get(url, params=params)
        
        if response.status_code != 200:
            print(f"Error: {response.status_code} - {response.text}")
            break  # Stop if there's an error

        results = response.json()
        items = results.get("items", [])
        image_urls.extend(item["link"] for item in items)

        # Save URLs to the file as they are fetched
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        with open(output_file, "a") as f:
            for url in (item["link"] for item in items):
                f.write(url + "\n")

        # Break if fewer results are returned, indicating the end
        if len(items) < results_per_page:
            break

    return image_urls

def remove_duplicates(output_file):
    """
    Removes duplicate URLs from the output file.
    NOT IN USE
    """
    with open(output_file, "r+") as file:
        urls = file.readlines()
        unique_urls = list(dict.fromkeys(url.strip() for url in urls))
    
        # Move the pointer to the beginning and truncate the file
        file.seek(0)
        file.write("\n".join(unique_urls))
        file.truncate()

    print(f"Duplicat

def main():
    parser = argparse.ArgumentParser(
        description="Fetch and save image URLs using Google Custom Search API."
    )
    parser.add_argument("query", type=str, help="Search query (e.g., 'drone').")
    parser.add_argument("num_results", type=int, help="Number of image URLs to fetch.")
    parser.add_argument("output_file", type=str, help="Path to the output text file.")
    args = parser.parse_args()

    # Replace with your own API key and CX
    API_KEY = "AIzaSyBJwaYBn8VnsRK19xBVgI-MA6u-hZXaz1E"
    CX = "a75fb3cd41e2e460b"

    output_path = os.path.join("/home/virtual46/url_logs/", args.output_file)

    print(f"Fetching {args.num_results} image URLs for query: '{args.query}'")
    image_urls = get_image_urls(
        args.query, API_KEY, CX, num_results=args.num_results, output_file=output_path
    )
    print(f"Saved {len(image_urls)} URLs to {output_path}")


if __name__ == "__main__":
    main()