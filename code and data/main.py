
import conllu
import json

# Load the CoNLL-U file
with open("obr.conllu", "r", encoding="utf-8") as f:
    sentences = conllu.parse(f.read())

# Convert to JSON-serializable format
data = []
for sentence in sentences:
    token_list = []
    for token in sentence:
        if isinstance(token, dict):
            token_list.append(token)
    sentence_data = {
        "metadata": sentence.metadata,
        "tokens": token_list
    }
    data.append(sentence_data)

# Save to JSON file
with open("output1.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)