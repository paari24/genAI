
import requests
import json

# Set up Grok API credentials
API_KEY = "your_grok_api_key_here"
BASE_URL = "https://api.x.ai/v1"

def get_grok_embeddings(text, api_key):
    """
    Get embeddings from Grok API
    """
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "input": text,
        "model": "embedding"  # Grok's embedding model
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/embeddings",
            headers=headers,
            json=payload
        )
        
        if response.status_code == 200:
            result = response.json()
            return result["data"][0]["embedding"]
        else:
            print(f"Error: {response.status_code}")
            print(response.text)
            return None
            
    except Exception as e:
        print(f"Request failed: {e}")
        return None

# Your text to embed
textforembed = "this is the one of the best view that I see in my life"

# Get embeddings from Grok
grok_embeddings = get_grok_embeddings(textforembed, API_KEY)

if grok_embeddings:
    print("First 5 embedding values:")
    print(grok_embeddings[:5])
    print(f"\nTotal embedding dimensions: {len(grok_embeddings)}")
else:
    print("Failed to get embeddings")

# Alternative: Using OpenAI-compatible client (if Grok supports it)
"""
from openai import OpenAI

client = OpenAI(
    api_key="your_grok_api_key",
    base_url="https://api.x.ai/v1"
)

response = client.embeddings.create(
    input=textforembed,
    model="embedding"
)

grok_embeddings = response.data[0].embedding
print(grok_embeddings[:5])
"""
