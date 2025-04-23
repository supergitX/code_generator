import os
import datetime
import re
import yaml
from pathlib import Path
import google.generativeai as genai

# Directory where the generated code will be saved
OUTPUT_DIR = Path("generated_code")
OUTPUT_DIR.mkdir(exist_ok=True)

# Gemini API setup: API key provided via GitHub Secrets as environment variable 'GEMINI_API_KEY'
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise EnvironmentError("GEMINI_API_KEY environment variable not set.")
genai.configure(api_key=api_key)

def extract_prompt_from_declaration() -> str:
    """Reads the prompt from declaration.yaml"""
    declaration_file = "declaration.yaml"
    if not os.path.exists(declaration_file):
        return "Write a Python function to sort a list."  # fallback

    with open(declaration_file, "r", encoding="utf-8") as f:
        try:
            declaration = yaml.safe_load(f)
            return declaration.get("prompt", "Write a Python function to sort a list.")
        except yaml.YAMLError as e:
            print(f"❌ Failed to parse declaration.yaml: {e}")
            return "Write a Python function to sort a list."  # fallback

def generate_code_from_prompt(prompt: str) -> str:
    """Generates code using Gemini based on the provided prompt."""
    directive = (
        "You are a code generation assistant. "
        "When responding, output only the requested code snippet without any additional explanation or commentary."
    )
    full_prompt = f"{directive}\n{prompt}"
    model = genai.GenerativeModel("models/gemini-2.0-flash")
    response = model.generate_content(full_prompt)
    text = response.text.strip()

    # Remove markdown code fences if present
    fence_match = re.search(r"```(?:python)?\n([\s\S]*?)```", text)
    if fence_match:
        return fence_match.group(1).strip()
    return text

def main():
    prompt = extract_prompt_from_declaration()
    generated_code = generate_code_from_prompt(prompt)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = OUTPUT_DIR / f"{timestamp}_generated.py"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(generated_code)

    print(f"✅ Code generated and saved to {output_file}")

if __name__ == "__main__":
    main()
