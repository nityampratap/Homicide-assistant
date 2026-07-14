import os
import base64
from groq import Groq

def encode_image_to_base64(image_path):
    """Converts a local screen file into a readable Base64 text string for the AI vision parser."""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def generate_vision_response(user_input, screen_image_path=None):
    """Evaluates screen captures natively using Groq's active Llama 4 Scout Vision architecture."""
    groq_key = os.getenv("GROQ_API_KEY")
    if not groq_key:
        return "System error: GROQ_API_KEY is missing from environment layout."

    try:
        client = Groq(api_key=groq_key)
        
        system_instruction = (
            "You are Homicide, a visual assistant analyzing a live screenshot of the user's monitor.\n\n"
            "STRICT ACTION ROUTING FORMATS:\n"
            "1. IF USER WANTS TO LAUNCH/OPEN A CLOSED APP (e.g., 'open Chrome'):\n"
            "   Reply EXACTLY with: JSON_FALLBACK_LAUNCH:app_name\n\n"
            "2. IF USER WANTS TO SEARCH/TYPE INSIDE AN OPEN APP BOX (e.g., 'search YouTube here'):\n"
            "   Find the search box in the image, estimate its center X and Y coordinates, extract the query text, and reply EXACTLY with:\n"
            "   JSON_TYPE:X|Y|text_to_search\n"
            "   Example: JSON_TYPE:450|80|youtube\n\n"
            "3. IF USER WANTS TO DOUBLE TAP/DOUBLE CLICK A LINK OR ICON:\n"
            "   Reply EXACTLY with: JSON_DOUBLE_CLICK:X|Y\n\n"
            "4. IF USER WANTS A REGULAR CLICK:\n"
            "   Reply EXACTLY with: JSON_CLICK:X|Y\n\n"
            "5. For casual talking, respond with a short text phrase."
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

        # FIXED: Swapped out the old decommissioned string for the premium active vision layer
        chat_completion = client.chat.completions.create(
            messages=messages,
            model="meta-llama/llama-4-scout-17b-16e-instruct", 
            temperature=0.1
        )
        
        return chat_completion.choices[0].message.content
        
    except Exception as e:
        print(f"❌ Groq Vision Brain Error: {e}")
        return "Visual processing module connection error."