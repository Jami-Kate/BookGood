from transformers import pipeline
from transformers import AutoTokenizer, pipeline
import torch
import pandas as pd
import json

def get_mood(text, n = 5):
    savani = "bhadresh-savani/distilbert-base-uncased-emotion"

    roberta = "SamLowe/roberta-base-go_emotions"

    my_model = roberta

    tokenizer = AutoTokenizer.from_pretrained(my_model)
    pipe = pipeline("text-classification", model = my_model, top_k = None)

    # Tokenize with overflow handling for long text
    encoding = tokenizer(
        text,
        truncation=True,
        padding="max_length",
        max_length=510,
        stride=64,  # Creates overlapping chunks
        return_overflowing_tokens=True,
        return_tensors="pt"
    )

    # Extract input IDs and attention masks for all chunks
    input_ids_chunks = encoding["input_ids"]
    attention_masks = encoding["attention_mask"]

    # Move tensors to the appropriate device
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    input_ids_chunks = input_ids_chunks.to(device)
    attention_masks = attention_masks.to(device)

    # Classify each chunk separately
    results = []
    for i in range(len(input_ids_chunks)):
        chunk_result = pipe(
            [tokenizer.decode(input_ids_chunks[i], skip_special_tokens=True)]
        )[0]
        chunk_result =  {dic["label"]: dic["score"] for dic in chunk_result if dic["label"] != "neutral"}
        results.append(chunk_result)


    json_text = pd.DataFrame(results).mean().to_json()
    final_score = json.loads(json_text)
    return dict(list(final_score.items())[:n])

def mood_batch(ind, incr = 5):
    books = open('static/data/data.json')
    books = json.load(books)['books']

    for book in books[ind:(ind + incr)]:
        if 'mood' not in book:
            mood = get_mood(book['review'])
            book.update({"mood": mood})
            book = json.dumps(book)
    print('testing')
    print(book)


mood_batch(0, 1)