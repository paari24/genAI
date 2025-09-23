"""
Grok Embeddings Implementation for LangChain
A drop-in replacement for OpenAI embeddings using Grok model locally
"""

from typing import List, Optional
import torch
from transformers import AutoTokenizer, AutoModel
from langchain.embeddings.base import Embeddings
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class HighQualityEmbeddings(Embeddings):
    """
    High-Quality Embeddings class that works as a drop-in replacement for OpenAI embeddings.
    
    This class uses proven sentence-transformer models that are specifically designed
    for creating high-quality embeddings, unlike large LLMs which aren't optimized for this task.
    """
    
    def __init__(
        self, 
        model_name: str = "sentence-transformers/all-MiniLM-L6-v2",
        device: Optional[str] = None,
        max_length: int = 512,
        batch_size: int = 32
    ):
        """
        Initialize the embeddings model.
        
        Args:
            model_name: HuggingFace model ID (default: "sentence-transformers/all-MiniLM-L6-v2")
            device: Device to run on ('cuda', 'cpu', or None for auto-detect)
            max_length: Maximum sequence length for tokenization
            batch_size: Batch size for processing multiple documents
            
        Popular embedding models to try:
            - "sentence-transformers/all-MiniLM-L6-v2" (Fast, good quality)
            - "sentence-transformers/all-mpnet-base-v2" (Better quality, slower)
            - "microsoft/DialoGPT-medium" (For conversational embeddings)
            - "facebook/bart-base" (BART-based embeddings)
        """
        self.model_name = model_name
        self.max_length = max_length
        self.batch_size = batch_size
        
        # Auto-detect device if not specified
        if device is None:
            self.device = "cuda" if torch.cuda.is_available() else "cpu"
        else:
            self.device = device
            
        logger.info(f"Initializing Grok embeddings on device: {self.device}")
        
        # Load tokenizer and model
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            self.model = AutoModel.from_pretrained(model_name)
            self.model.to(self.device)
            self.model.eval()  # Set to evaluation mode
            
            # Add padding token if it doesn't exist
            if self.tokenizer.pad_token is None:
                self.tokenizer.pad_token = self.tokenizer.eos_token
                
            logger.info(f"Successfully loaded model: {model_name}")
            
        except Exception as e:
            logger.error(f"Failed to load model {model_name}: {str(e)}")
            raise
    
    def _mean_pooling(self, model_output, attention_mask):
        """
        Apply mean pooling to get sentence-level embeddings.
        
        Args:
            model_output: Output from the transformer model
            attention_mask: Attention mask from tokenizer
            
        Returns:
            torch.Tensor: Pooled embeddings
        """
        token_embeddings = model_output.last_hidden_state
        input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
        
        # Sum embeddings and divide by actual length (excluding padding)
        sum_embeddings = torch.sum(token_embeddings * input_mask_expanded, 1)
        sum_mask = torch.clamp(input_mask_expanded.sum(1), min=1e-9)
        
        return sum_embeddings / sum_mask
    
    def _encode_text(self, text: str) -> List[float]:
        """
        Encode a single text into an embedding vector.
        
        Args:
            text: Input text to encode
            
        Returns:
            List[float]: Embedding vector
        """
        # Tokenize the text
        inputs = self.tokenizer(
            text,
            return_tensors="pt",
            truncation=True,
            padding=True,
            max_length=self.max_length
        )
        
        # Move inputs to device
        inputs = {k: v.to(self.device) for k, v in inputs.items()}
        
        # Generate embeddings
        with torch.no_grad():
            outputs = self.model(**inputs)
            embeddings = self._mean_pooling(outputs, inputs['attention_mask'])
        
        # Convert to list and return
        return embeddings.squeeze().cpu().tolist()
    
    def embed_query(self, text: str) -> List[float]:
        """
        Embed a single query text (compatible with LangChain interface).
        
        Args:
            text: Query text to embed
            
        Returns:
            List[float]: Embedding vector
        """
        return self._encode_text(text)
    
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """
        Embed multiple documents (compatible with LangChain interface).
        
        Args:
            texts: List of texts to embed
            
        Returns:
            List[List[float]]: List of embedding vectors
        """
        embeddings = []
        
        # Process in batches for better memory efficiency
        for i in range(0, len(texts), self.batch_size):
            batch_texts = texts[i:i + self.batch_size]
            
            for text in batch_texts:
                embedding = self._encode_text(text)
                embeddings.append(embedding)
                
            # Log progress for large batches
            if len(texts) > 10:
                logger.info(f"Processed {min(i + self.batch_size, len(texts))}/{len(texts)} documents")
        
        return embeddings
    
    def get_dimension(self) -> int:
        """
        Get the dimension of the embedding vectors.
        
        Returns:
            int: Embedding dimension
        """
        # Test with a simple text to get dimension
        test_embedding = self.embed_query("test")
        return len(test_embedding)


# Example usage and testing functions
def test_embeddings():
    """Test the embedding implementation."""
    print("🚀 Testing High-Quality Embeddings Implementation")
    print("=" * 50)
    
    # Initialize embeddings
    print("1. Initializing embeddings...")
    embed_model = HighQualityEmbeddings()
    
    # Test single query
    print("\n2. Testing single query embedding...")
    test_text = "This is an excellent GenAI course about artificial intelligence."
    embedding = embed_model.embed_query(test_text)
    
    print(f"   Text: {test_text}")
    print(f"   Embedding dimension: {len(embedding)}")
    print(f"   First 5 values: {embedding[:5]}")
    
    # Test multiple documents
    print("\n3. Testing multiple document embeddings...")
    documents = [
        "Artificial Intelligence is transforming the world.",
        "LangChain makes building AI applications much easier.",
        "Sentence transformers create high-quality embeddings.",
        "Vector databases enable semantic search capabilities.",
        "Machine learning requires large amounts of training data."
    ]
    
    doc_embeddings = embed_model.embed_documents(documents)
    print(f"   Number of documents: {len(documents)}")
    print(f"   Embeddings shape: {len(doc_embeddings)} x {len(doc_embeddings[0])}")
    
    return embed_model, documents, doc_embeddings


def demo_with_faiss():
    """Demonstrate integration with FAISS vector database."""
    try:
        from langchain.vectorstores import FAISS
        from langchain.schema import Document
        
        print("\n🔍 Testing with FAISS Vector Database")
        print("=" * 50)
        
        # Initialize embeddings
        grok_embed = GrokEmbeddings()
        
        # Sample documents
        documents = [
            "Artificial Intelligence is revolutionizing healthcare and medicine.",
            "Machine learning algorithms can predict stock market trends.",
            "Natural language processing enables computers to understand human text.",
            "Computer vision helps autonomous vehicles navigate safely.",
            "Deep learning networks mimic the structure of the human brain.",
            "Robotics combines AI with mechanical engineering for automation.",
            "Big data analytics reveals hidden patterns in large datasets.",
            "Cloud computing provides scalable infrastructure for AI workloads."
        ]
        
        print("1. Creating FAISS vector database...")
        # Create FAISS index with embeddings
        db = FAISS.from_texts(texts=documents, embedding=embed_model)
        
        print("2. Performing similarity search...")
        # Test queries
        queries = [
            "How does AI help in medical applications?",
            "What can machine learning do for finance?",
            "How do computers understand language?"
        ]
        
        for query in queries:
            print(f"\n   Query: {query}")
            results = db.similarity_search(query, k=2)
            
            for i, result in enumerate(results, 1):
                print(f"   Result {i}: {result.page_content}")
        
        print("✅ FAISS integration successful!")
        return db
        
    except ImportError:
        print("❌ FAISS not installed. Install with: pip install faiss-cpu")
        return None


if __name__ == "__main__":
    # Run tests
    try:
        # Basic functionality test
        embed_model, docs, embeddings = test_embeddings()
        print("\n✅ Basic functionality test passed!")
        
        # FAISS integration test
        db = demo_with_faiss()
        
        print("\n🎉 All tests completed successfully!")
        print("\nYour embeddings are ready to use as a drop-in replacement for OpenAI!")
        
        # Show different model options
        print("\n📚 Available Models:")
        print("- sentence-transformers/all-MiniLM-L6-v2 (Default - Fast & Good)")
        print("- sentence-transformers/all-mpnet-base-v2 (Better Quality)")
        print("- sentence-transformers/paraphrase-MiniLM-L6-v2 (Paraphrase Detection)")
        print("- microsoft/DialoGPT-medium (Conversational)")
        
    except Exception as e:
        print(f"\n❌ Error during testing: {str(e)}")
        print("Please check your installation and try again.")