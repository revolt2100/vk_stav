import os
from tqdm import tqdm
import json
import io

def extract_texts_from_json_file(filepath):
    texts = []
    if not os.path.exists(filepath):
        print(f"Error: File not found at '{filepath}'")
        return None

    # Open and read the local file directly with UTF-8 encoding
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)

    for item in data:
        text_content = item.get('text', '')
        texts.append(text_content)

    return texts

posts_json_filepath = 'data/posts.json'
comments_json_filepath = 'data/comments.json'
output_filepath = 'posts_comments.txt'

comment_texts = extract_texts_from_json_file(comments_json_filepath)

post_texts = extract_texts_from_json_file(posts_json_filepath)

comment_texts.extend(post_texts)

print(f"\nWriting {len(comment_texts)} texts to '{output_filepath}'...")
with open(output_filepath, 'w', encoding='utf-8') as f:
    for i in tqdm(comment_texts, desc="Writing"):
        f.write(i.replace('\n', ' '))
        f.write('\n\n')
print("Finished writing.")

