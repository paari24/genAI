from grok_embeddings import HighQualityEmbeddings

# Initialize the embeddings model (uses sentence-transformers by default)
embeddings = HighQualityEmbeddings()

# Test with a simple query
text = "Hello, this is a test sentence for embedding."
vector = embeddings.embed_query(text)

print(f"Text: {text}")
print(f"Embedding dimension: {len(vector)}")
print(f"Sample values: {vector[:5]}")