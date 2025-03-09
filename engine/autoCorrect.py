from transformers import T5ForConditionalGeneration, AutoTokenizer

def remove_repeated_words(text):
    return " ".join(dict.fromkeys(text.split()))  # keeps only first occurrence

def correct_query(query):
    if not query or not isinstance(query, str) or query.strip() == "":
        return ""  # Return an empty string instead of processing further

    modelPath = "ai-forever/T5-large-spell"
    model = T5ForConditionalGeneration.from_pretrained(modelPath)
    tokenizer = AutoTokenizer.from_pretrained(modelPath)

    encodings = tokenizer(query, return_tensors="pt", padding=True, truncation=True)

    generatedTokens = model.generate(**encodings)  
    correctedQuery = tokenizer.batch_decode(generatedTokens, skip_special_tokens=True)[0]
    cleanedQuery = remove_repeated_words(correctedQuery)

    return cleanedQuery
