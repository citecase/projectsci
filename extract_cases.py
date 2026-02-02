import requests
import re

def extract_and_sort():
    url = "https://raw.githubusercontent.com/citecase/projectsci/main/README.md"
    response = requests.get(url)
    if response.status_code != 200:
        return

    lines = response.text.split('\n')
    extracted_data = []

    for line in lines:
        # Check if the line is a table row with enough columns
        if '|' in line:
            parts = [p.strip() for p in line.split('|')]
            # Filter out empty strings from split and header separators
            parts = [p for p in parts if p and not all(c == '-' for c in p)]
            
            if len(parts) >= 4:
                case_name = parts[3] # Fourth column
                last_col = parts[-1] # Last column
                
                # Extract link and citation from the last column
                # Expected format: [2026 INSC 123](url)
                match = re.search(r'\[(.*?)\]\((.*?)\)', last_col)
                if match:
                    citation = match.group(1)
                    link = match.group(2)
                    
                    extracted_data.append({
                        "full_text": f"[{case_name} {citation}]({link})",
                        "citation": citation
                    })

    # Sort by neutral citation (Ascending)
    # We sort by the text of the citation (e.g., '2024 INSC 1' comes before '2024 INSC 2')
    sorted_data = sorted(extracted_data, key=lambda x: x['citation'])

    with open("sorted_cases.md", "w") as f:
        f.write("# Sorted Case List\n\n")
        for item in sorted_data:
            f.write(f"{item['full_text']}  \n")

if __name__ == "__main__":
    extract_and_sort()
