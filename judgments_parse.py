# judgments_parse.py
import re

with open("judgments.md", encoding="utf-8") as f:
    text = f.read()

rows = []

# Very loose pattern: each row has a [..](url://N) at the end for Judgment
row_pattern = re.compile(r"\|\s*\d+\s*\|.*?\|\s*\[(.*?)\]\((url://\d+)\)")

for m in row_pattern.finditer(text):
    # Whole row text is m.group(0)
    row = m.group(0)

    # Case name is in the 4th column (Petitioner / Respondent)
    cols = [c.strip() for c in row.split("|")]
    if len(cols) < 5:
        continue
    parties = cols[3]

    judgment_label = m.group(1)
    link = m.group(2)

    # Find neutral citation like '2025 INSC 958'
    cit_match = re.search(r"(20\d{2}\s+INSC\s+\d+)", judgment_label)
    if not cit_match:
        continue
    citation = cit_match.group(1)

    rows.append((citation, parties, link))

rows.sort(key=lambda x: x[0])

with open("all-judgments-sorted.md", "w", encoding="utf-8") as out:
    for citation, parties, link in rows:
        out.write(f"[{parties}]({link}) – {citation}  \n")
