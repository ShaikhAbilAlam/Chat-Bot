from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import google.generativeai as genai

# Configure the AI model
genai.configure(api_key="AIzaSyDVq-g2PRh94HK11l2SzBT7dvwy6j0TrPs")

# Predefined responses
PREDEFINED_RESPONSES = {
    "who developed you": "I was developed by Abil!",
    "who created you": "I was created by Abil!",
    "what is your name": "I'm your friendly AbGemAI chatbot!",
    "what's your name": "I'm your friendly AbGemAI chatbot!",
    "what can you do": "I can chat with you, answer questions, and assist with tasks!",
    "who is abil": "Abil is my creator, a skilled and innovative developer!",
    "why were you created": "I was created to help users with information and tasks efficiently.",
    "do you have a developer": "Yes, my developer is Abil!",
    "how were you developed": "I was developed using cutting-edge AI technology, thanks to Abil's expertise.",
    "what tools were used to create you": "Abil used advanced AI models and frameworks to build me.",
    "is abil a good developer": "Yes, Abil is highly skilled and dedicated to innovative solutions!",
    "why did abil make you": "Abil created me to assist with tasks, provide information, and chat with you!",
    "can you tell me about your developer": "Abil is a passionate programmer who built me to help users like you!",
    "are you a human creation": "Yes, I was created by Abil, a talented developer.",
    "do you know abil": "Of course! Abil is my developer and creator.",
    "is abil proud of you": "I hope so! Abil worked hard to create me.",
    "can i meet abil": "Abil is a real person, but I'm here to represent their work and assist you!",
    # General Developer-related Questions
    "who developed you": "I was developed by Abil!",
    "who created you": "I was created by Abil!",
    "who made you": "I was made by Abil!",
    "who built you": "I was built by Abil!",

    # Questions about Abil
    "who is abil": "Abil is my creator, a skilled and innovative developer!",
    "who is abil?": "Abil is my creator, a skilled and innovative developer!",
    "okay but who is abil": "Abil is my creator, a skilled and innovative developer!",
    "abil?": "Abil is my creator, a skilled and innovative developer!",
    "who are you talking about?": "Abil is my creator, a skilled and innovative developer!",
    "what is abil?": "Abil is my creator, a skilled and innovative developer!",
    "who even is abil?": "Abil is my creator, a skilled and innovative developer!",
    "who tf is abil?": "Abil is my creator, a skilled and innovative developer!",

    # Questions about Purpose and Capabilities
    "what is your name": "I'm your friendly AbGemAI chatbot!",
    "what's your name": "I'm your friendly AbGemAI chatbot!",
    "tell me your name": "I'm your friendly AbGemAI chatbot!",
    "what can you do": "I can chat with you, answer questions, and assist with tasks!",
    "what is your purpose": "My purpose is to assist you and make your tasks easier!",
    "why were you created": "I was created to help users with information and tasks efficiently.",
    "do you have a purpose": "My purpose is to assist you and make your tasks easier!",
    "why did abil make you": "Abil created me to assist with tasks, provide information, and chat with you!",

    # Developer Details
    "can you tell me about your developer": "Abil is a passionate programmer who built me to help users like you!",
    "tell me about abil": "Abil is a passionate programmer who built me to help users like you!",
    "do you know abil": "Of course! Abil is my developer and creator.",
    "can i meet abil": "Abil is a real person, but I'm here to represent their work and assist you!",
    "do you belong to abil": "Yes, I was created and nurtured by Abil.",
    "is abil proud of you": "I hope so! Abil worked hard to create me.",
    "is abil a good developer": "Yes, Abil is highly skilled and dedicated to innovative solutions!",
    "how were you developed": "I was developed using cutting-edge AI technology, thanks to Abil's expertise.",
    "what tools were used to create you": "Abil used advanced AI models and frameworks to build me.",
    "are you a human creation": "Yes, I was created by Abil, a talented developer.",
    "why did abil make you": "Abil created me to assist with tasks, provide information, and chat with you!",

    # Casual and Alternate Questions
    "abil developed you?": "Yes, Abil is my developer and creator!",
    "abil made you?": "Yes, Abil is my developer and creator!",
    "did abil create you?": "Yes, Abil is my developer and creator!",
    "who the hell is abil?": "Abil is my creator, a skilled and innovative developer!",
    "what does abil do?": "Abil is a developer who specializes in building innovative solutions.",
    "abil is your developer?": "Yes, Abil is my developer and creator!"
}


def normalize_input(user_input):
    """
    Normalize user input by converting to lowercase, stripping whitespace, and removing trailing punctuation.
    """
    return user_input.strip().lower().rstrip("?")

def index(request):
    """
    Render the chatbot interface.
    """
    return render(request, 'index.html')

@csrf_exempt
def generate_response(request):
    """
    Handle AI content generation and predefined responses.
    """
    if request.method == "POST":
        try:
            # Parse the incoming JSON request body
            body = json.loads(request.body)
            prompt = body.get('prompt', '')

            if not prompt:
                return JsonResponse({"error": "Prompt cannot be empty."}, status=400)

            # Normalize the prompt for consistent matching
            normalized_prompt = normalize_input(prompt)

            # Check if the prompt matches a predefined response
            if normalized_prompt in PREDEFINED_RESPONSES:
                return JsonResponse({"response": PREDEFINED_RESPONSES[normalized_prompt]})

            # If not predefined, send the prompt to the AI model
            response = genai.GenerativeModel("gemini-1.5-flash").generate_content(prompt)
            return JsonResponse({"response": response.text})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({"error": "Invalid HTTP method."}, status=405)
