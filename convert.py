import os
import re
import json

def process_folder():
    target_dir = 'json'
    all_cases = [] # List to hold all rows
    
    if not os.path.exists(target_dir):
        return

    for filename in os.listdir(target_dir):
        if filename.endswith('.md'):
            file_path = os.path.join(target_dir, filename)
            
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
                # Improved Regex to handle multiple lines or different spacing
                # Specifically targeting: Petitioner [Versus] Respondent
                title_match = re.search(r'(.*?)\s+(?:Versus|vs\.?|V/s)\s+(.*)', content, re.IGNORECASE)
                insc_match = re.search(r'(\d{4}\s+INSC\s+\d+)', content)
                
                if title_match:
                    case_data = {
                        "filename": filename,
                        "petitioner": title_match.group(1).strip('# \n').strip(),
                        "respondent": title_match.group(2).strip().split('\n')[0].strip(),
                        "insc_citation": insc_match.group(1) if insc_match else "N/A"
                    }
                    all_cases.append(case_data)

    # Save EVERYTHING into one file
    with open(os.path.join(target_dir, 'all_cases.json'), 'w', encoding='utf-8') as out_f:
        json.dump(all_cases, out_f, indent=4)
    
    print(f"Successfully processed {len(all_cases)} cases.")

if __name__ == "__main__":
    process_folder()
