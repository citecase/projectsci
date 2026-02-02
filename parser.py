import os
import re
import json

def process_folder():
    target_dir = 'json'
    all_cases = []
    
    if not os.path.exists(target_dir):
        return

    # UPDATED REGEX:
    # \[([\s\S]*?)\] -> Matches everything inside [], including newlines (Case Name)
    # \((.*?)\)      -> Matches the URL inside ()
    # .*?            -> Skips any filler text (like "Appellant", "Versus", etc.)
    # (\d{4}\s+INSC\s+\d+) -> Matches the Citation
    case_pattern = r'\[([\s\S]*?)\]\((.*?)\)[\s\S]*?(\d{4}\s+INSC\s+\d+)'

    for filename in sorted(os.listdir(target_dir)):
        if filename.endswith('.md'):
            file_path = os.path.join(target_dir, filename)
            
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
                # Using re.finditer with re.MULTILINE to catch complex names
                for match in re.finditer(case_pattern, content, re.MULTILINE):
                    # Clean up the case name (remove extra newlines or markdown bolding)
                    raw_name = match.group(1).replace('\n', ' ').replace('**', '').strip()
                    # Remove multiple spaces
                    clean_name = " ".join(raw_name.split())
                    
                    all_cases.append({
                        "case_name": clean_name,
                        "link": match.group(2).strip(),
                        "citation": match.group(3).strip()
                    })

    # Save to json/all_cases.json
    output_path = os.path.join(target_dir, 'all_cases.json')
    with open(output_path, 'w', encoding='utf-8') as out_f:
        json.dump(all_cases, out_f, indent=4)
    
    print(f"Extraction complete. Total rows: {len(all_cases)}")

if __name__ == "__main__":
    process_folder()
