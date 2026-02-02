import requests
import re
import json

def extract_and_sort_cases(url):
    # Fetch the raw README content
    response = requests.get(url)
    if response.status_code != 200:
        print("Failed to fetch file.")
        return

    content = response.text
    
    # Regex pattern to match: [Case Name](Link) Neutral Citation
    # Adjusting based on common formats like: [ABC v XYZ](http://...) 2024 INSC 123
    pattern = r'\[(.*?)\]\((.*?)\)\s+([\d\s\w]+(?:SC|INSC|UKSC|SCC|AIR)[\d\s\w]+)'
    
    cases = []
    matches = re.findall(pattern, content)
    
    for name, link, citation in matches:
        cases.append({
            "case_name": name.strip(),
            "link": link.strip(),
            "neutral_citation": citation.strip()
        })

    # Sort in ascending order of neutral citation
    # Note: Complex citations may need a custom sort key; this sorts alphabetically
    sorted_cases = sorted(cases, key=lambda x: x['neutral_citation'])

    # Output to Markdown or JSON
    with open("sorted_cases.md", "w") as f:
        f.write("# Sorted Case List\n\n")
        f.write("| Case Name | Neutral Citation | Link |\n")
        f.write("| --- | --- | --- |\n")
        for case in sorted_cases:
            f.write(f"| {case['case_name']} | {case['neutral_citation']} | [View Case]({case['link']}) |\n")
            
    print(f"Successfully extracted {len(sorted_cases)} cases.")

if __name__ == "__main__":
    RAW_URL = "https://raw.githubusercontent.com/citecase/projectsci/main/README.md"
    extract_and_sort_cases(RAW_URL)
