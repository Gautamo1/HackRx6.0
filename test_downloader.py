import google.generativeai as genai
from dotenv import load_dotenv
import os

# Load environment variables (make sure your .env file contains GEMINI_API_KEY)
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env file.")

# Configure the Gemini SDK
genai.configure(api_key=api_key)

# List available models
models = genai.list_models()

print("🧠 Available Gemini Models with your API key:\n")
for model in models:
    model_info = f"""
Name: {model.name}
Version: {model.version if hasattr(model, 'version') else 'N/A'}
Generation Methods: {model.supported_generation_methods}
Input Token Limit: {getattr(model, 'input_token_limit', 'N/A')}
Output Token Limit: {getattr(model, 'output_token_limit', 'N/A')}
    """.strip()
    print(model_info)
    print("-" * 60)
