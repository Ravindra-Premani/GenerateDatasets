import json
import random
import hashlib
from pathlib import Path

actions = ["filter", "sort", "group", "highlight"]
criteria = ["=", "!=", ">", "<", "in", "contains", "like"]
synonym_prompts = [
    "Show me", "Get me", "List all", "Only display", "I want to see",
    "Highlight all", "Filter by", "Group together", "Arrange by", "Order by"
]
columns = [
    "Customer Id", "Customer Name", "Customer Type", "Limit", "Exposure", "Deals",
    "CORS Risk Officer", "Primary Relationship Manager", "Credit Risk Underwriter",
    "Desk Limit Risk Officer", "FX Specialist", "Reporting Category", "Country of Domicile",
    "Country of Risk", "FX Parent Id", "FX Parent Name", "DR Parent Id", "DR Parent Name",
    "DR Customer Level", "Parent Id", "Parent Name", "Investment Manager Parent Id",
    "Investment Manager Parent Name", "Investment Manager Override", "Focus Credit",
    "Groups", "Counterparty Tier", "Tiering Method", "Counterparty Tier Update Date",
    "Counterparty Tier Updated By", "Counterparty Tier Override Approver",
    "Counterparty Tiering - Regulated Financial Institution", "Annual Review Date",
    "External Review Date", "External Extension", "Reg O Counterparty", "Reg W Counterparty",
    "Hedge Fund", "Customer Short Name", "Active"
]

def record_hash(record):
    return hashlib.md5((record['userQuery'] + json.dumps(record['ideal-response-for-training'], sort_keys=True)).encode()).hexdigest()

output_file = Path("query_dataset_large_dedup.json")
seen = set()
unique_data = []

print("Generating 1 million unique records...")

while len(unique_data) < 1_000_000:
    num_tasks = random.randint(1, 3)
    task_cols = random.sample(columns, num_tasks)
    tasks = [{
        "action": random.choice(actions),
        "column": col,
        "criteria": random.choice(criteria) + " some_value"
    } for col in task_cols]
    
    user_query = f"{random.choice(synonym_prompts)} {', '.join([t['column'] for t in tasks])}"
    record = {
        "userQuery": user_query,
        "ideal-response-for-training": tasks
    }
    h = record_hash(record)
    if h not in seen:
        seen.add(h)
        unique_data.append(record)
    
    if len(unique_data) % 100000 == 0:
        print(f"{len(unique_data)} records generated...")

with open(output_file, "w", encoding="utf-8") as f:
    json.dump(unique_data, f, indent=2)

print("Done! File saved as:", output_file)
