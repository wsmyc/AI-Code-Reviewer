from pathlib import Path
import datasets
from transformers import AutoTokenizer

# 1. Paths
jsonl_path = Path(__file__).resolve().parents[2] / "data" / "first_200_codes.jsonl"

tokenized_path = Path("../../data/tokenized_dataset")

# 2. Load dataset from JSONL
raw_datasets = datasets.load_dataset("json", data_files=str(jsonl_path))
print("Raw dataset:", raw_datasets)

# 3. Load CodeT5 tokenizer
tokenizer = AutoTokenizer.from_pretrained("Salesforce/codet5-small")

# 4. Tokenization function
def tokenize_function(example):
    # We tokenize both the code and the docstring
    return tokenizer(
        example["code"], 
        example["docstring"], 
        padding="max_length",   # for batching
        truncation=True,        # cut off if too long
        max_length=256          # you can adjust this
    )

# 5. Apply tokenization
tokenized_datasets = raw_datasets.map(tokenize_function, batched=True)
print("Tokenized dataset:", tokenized_datasets)

# 6. Save to disk
tokenized_datasets.save_to_disk(str(tokenized_path))
print(f"✅ Tokenized dataset saved at {tokenized_path}")
