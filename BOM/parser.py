import csv

INPUT = "DigitalOsciloscope.csv"
OUTPUT = "checklist.txt"

def expand_refs(ref_field):
    """Split 'C1,C2,C5' into ['C1', 'C2', 'C5']"""
    return [r.strip() for r in ref_field.split(",") if r.strip()]

with open(INPUT, newline='', encoding="utf-8") as f:
    reader = csv.DictReader(f)

    items = []
    for row in reader:
        refs = expand_refs(row["Reference"])
        value = row["Value"]
        footprint = row["Footprint"]
        dnp = (row["DNP"].strip().upper() == "DNP")

        for ref in refs:
            items.append({
                "ref": ref,
                "value": value,
                "footprint": footprint,
                "dnp": dnp,
            })

# Sort checklist by reference (C1, C2, C3..., R1... etc.)
items.sort(key=lambda x: (x["ref"][0], int("".join([c for c in x["ref"] if c.isdigit()] or "0"))))

# Write printable checklist
with open(OUTPUT, "w", encoding="utf-8") as f:
    f.write("=== PCB ASSEMBLY CHECKLIST ===\n\n")
    for item in items:
        if item["dnp"]:
            check = "[ ] (DNP)"
        else:
            check = "[ ]"

        line = f"{check} {item['ref']:6s}  {item['value']:15s}  {item['footprint']}"
        f.write(line + "\n")

print(f"Checklist saved to {OUTPUT}")
