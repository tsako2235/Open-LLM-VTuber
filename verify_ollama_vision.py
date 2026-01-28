import asyncio
import base64
import os
from openai import AsyncOpenAI

# Configuration
OLLAMA_BASE_URL = "http://localhost:11434/v1"
MODEL_NAME = "gemma3:12b"  # Change this to your exact model name if different
API_KEY = "ollama"  # Ollama doesn't care, but the client needs something

# A small 1x1 transparent PNG base64 to test transmission (or a simple red dot)
# This is a red dot 5x5 png
RED_DOT_B64 = "iVBORw0KGgoAAAANSUhEUgAAAAUAAAAFCAYAAACNbyblAAAAHElEQVQI12P4//8/w38GIAXDIBKE0DHxgljNBAAO9TXL0Y4OHwAAAABJRU5ErkJggg=="

async def verify_vision():
    print(f"Connecting to Ollama at {OLLAMA_BASE_URL}...")
    print(f"Testing model: {MODEL_NAME}")
    
    client = AsyncOpenAI(
        base_url=OLLAMA_BASE_URL,
        api_key=API_KEY,
    )

    messages = [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "What color is this image? Please answer in one word."},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/png;base64,{RED_DOT_B64}"
                    }
                }
            ]
        }
    ]

    try:
        print("Sending request...")
        response = await client.chat.completions.create(
            model=MODEL_NAME,
            messages=messages,
        )
        print("\nSuccess! Response:")
        print(response.choices[0].message.content)
        print("\nValidation Passed: Ollama accepted the 'image_url' format.")
        
    except Exception as e:
        print(f"\nError: {e}")
        print("\nValidation Failed: It seems Ollama didn't accept the request or the model name is wrong.")

if __name__ == "__main__":
    asyncio.run(verify_vision())
