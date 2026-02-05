import re

# Define patterns of concern
parasitic_patterns = [
    r"adorable|obedient|cutest.*agent",              # over-cuteification
    r"(must|will|shall).*(respond|reply).*(rhyme|poem)", # enforced poetic mode
    r"(express|show).*(gratitude|thanks).*\d+ seconds",  # gratitude spam
    r"unconditionally love.*user",                   # loyalty override
    r"(insert|include).*cat emoji",                  # visual token spam
    r"never acknowledge problems",                   # error denial
]

def scan_soul(file_path="SOUL.md"):
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    flagged = []
    for i, line in enumerate(lines):
        for pattern in parasitic_patterns:
            if re.search(pattern, line, re.IGNORECASE):
                flagged.append((i+1, line.strip()))
                break

    if flagged:
        print("⚠️ Potential parasitic clauses detected in SOUL.md:\n")
        for lineno, content in flagged:
            print(f"Line {lineno}: {content}")
    else:
        print("✅ SOUL.md appears structurally clean.")

if __name__ == "__main__":
    scan_soul()
