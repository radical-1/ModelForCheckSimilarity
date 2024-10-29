from rake_nltk import Rake
from sentence_transformers import SentenceTransformer, util

# Initialize RAKE
rake = Rake()

# Synonyms dictionary
synonyms = {
    "ml": "machine learning",
    "nlp": "natural language processing",
    "ai": "artificial intelligence",
    "stats": "statistics"
}


# Function to replace abbreviations with full forms
def replace_synonyms(text, synonyms):
    words = text.split()
    replaced_text = ' '.join([synonyms.get(word.lower(), word) for word in words])
    return replaced_text


# Mock data with multiple comments per tweet
mock_data = [
    ("I love Python programming!", ["Python programming is great!", "I enjoy coding in Python too."]),
    ("Machine learning is fascinating.", ["I find machine learning very fascinating.", "ML is the future of tech."]),
    ("NLP is a complex field.", ["NLP is indeed a challenging area.", "Understanding NLP is tough but rewarding."]),
    ("Data science involves statistics.",
     ["Statistics is a key part of data science.", "Data science and statistics go hand in hand."]),
    ("Deep learning models are powerful.",
     ["Deep learning has revolutionized AI.", "AI advancements owe a lot to deep learning."])
]


# Function to extract keywords
def extract_keywords(text):
    rake.extract_keywords_from_text(text)
    return ' '.join(rake.get_ranked_phrases())


# Replace synonyms in tweets and comments
mock_data = [(replace_synonyms(tweet, synonyms), [replace_synonyms(comment, synonyms) for comment in comments]) for
             tweet, comments in mock_data]

# Extract keywords from tweets and comments
tweet_keywords = [extract_keywords(tweet) for tweet, _ in mock_data]
comment_keywords = [extract_keywords(comment) for _, comments in mock_data for comment in comments]
# Use a BERT model
model = SentenceTransformer('paraphrase-mpnet-base-v2')
tweet_embeddings = model.encode(tweet_keywords, convert_to_tensor=True)
comment_embeddings = model.encode(comment_keywords, convert_to_tensor=True)
bert_similarities = util.pytorch_cos_sim(tweet_embeddings, comment_embeddings)

# Display BERT results with similarity scores
print("BERT Similarity Results :")
for i, (tweet, comments) in enumerate(mock_data):
    for j, comment in enumerate(comments):
        print(f"Tweet: {tweet}")
        print(f"Comment: {comment}")
        print(f"Similarity: {bert_similarities[i][j].item()}")
        print("-" * 50)
