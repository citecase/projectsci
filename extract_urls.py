import re
import os

def extract_urls(input_file, output_file):
    if not os.path.exists(input_file):
        print(f"Error: {input_file} not found.")
        return

    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Regex to find the last column of a markdown table row containing a URL
    # Matches patterns like | ... | [Link](http...) | or | ... | http... |
    url_pattern = r'\|\s*(?:\[.*?\]\()?(https?://[^\)\s|]+)\)?\s*\|'
    
    urls = re.findall(url_pattern, content)

    with open(output_file, 'w', encoding='utf-8') as f:
        for url in urls:
            f.write(url + '\n')
            
    print(f"Successfully extracted {len(urls)} URLs to {output_file}")

if __name__ == "__main__":
    extract_urls("README.md", "urls.txt")
