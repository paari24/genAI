import torch
import transformers
import langchain

print(f"PyTorch version: {torch.__version__}")
print(f"CUDA available: {torch.cuda.is_available()}")
print(f"Transformers version: {transformers.__version__}")
print(f"LangChain version: {langchain.__version__}")