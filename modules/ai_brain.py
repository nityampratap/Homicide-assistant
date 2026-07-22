import os
import re
import base64
from groq import Groq

def encode_image_to_base64(image_path):
    """Converts a local screen file into a readable Base64 text string."""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def generate_vision_response(user_input, screen_image_path=None):
    """Evaluates screen captures natively using Groq's vision architecture."""
    groq_key = os.getenv("GROQ_API_KEY")
    if not groq_key:
        return "System error: GROQ_API_KEY is missing from environment layout."

    try:
        client = Groq(api_key=groq_key)
        
        # Adding /no_think turns off Qwen's internal reasoning block output
        system_instruction = (
            "/no_think\n"
            "You are Homicide, a visual assistant analyzing a live screenshot of the user's monitor.\n\n"
            "STRICT ACTION ROUTING FORMATS:\n"
            "1. IF USER WANTS TO LAUNCH OR OPEN ANY APP (e.g., 'open Chrome', 'launch Notepad'):\n"
            "   DO NOT guess pixel coordinates. Reply EXACTLY with: JSON_FALLBACK_LAUNCH:app_name\n"
            "   Example: JSON_FALLBACK_LAUNCH:chrome\n\n"
            "2. IF USER WANTS TO SEARCH OR TYPE INSIDE AN OPEN APP BOX (e.g., 'search YouTube here'):\n"
            "   Find the input bar in the image, estimate its center X and Y coordinates, and reply EXACTLY with:\n"
            "   JSON_TYPE:X|Y|text_to_search\n\n"
            "3. IF USER WANTS TO CLICK AN ITEM OR BUTTON ON SCREEN:\n"
            "   Reply EXACTLY with: JSON_CLICK:X|Y\n\n"
            "4. For casual conversation, respond with a short text phrase."
        )

        messages = [{"role": "system", "content": system_instruction}]
        
        if screen_image_path and os.path.exists(screen_image_path):
            base64_image = encode_image_to_base64(screen_image_path)
            messages.append({
                "role": "user",
                "content": [
                    {"type": "text", "text": user_input},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{base64_image}"
                        }
                    }
                ]
            })
        else:
            messages.append({"role": "user", "content": user_input})

        chat_completion = client.chat.completions.create(
            messages=messages,
            model="qwen/qwen3.6-27b",
            temperature=0.1
        )
        
        raw_output = chat_completion.choices[0].message.content
        
        # Clean out any leftover <think>...</think> tags dynamically
        cleaned_output = re.sub(r'<think>.*?</think>', '', raw_output, flags=re.DOTALL).strip()
        
        return cleaned_output
        
    except Exception as e:
        print(f"❌ Groq Vision Brain Error: {e}")
        return "Visual processing module connection error."