from django.shortcuts import render
from django.http import JsonResponse, HttpResponseBadRequest
import json, os, logging
from .ai_logic import ai_chat_response  # uses DB-aware logic
from .models import ChatHistory, Scheme
from django.views.decorators.csrf import csrf_exempt

logger = logging.getLogger(__name__)

# Home view
def home(request):
    return render(request, 'home.html')

# Chat UI
def chat(request):
    return render(request, 'chatbot.html')

# Schemes page uses DB Schemes (fallback to json if DB empty)
def schemes(request):
    schemes_qs = Scheme.objects.all().order_by('category', 'name')
    if schemes_qs.exists():
        schemes = list(schemes_qs.values('name', 'category', 'description', 'eligibility', 'min_age', 'max_age', 'income_limit', 'gender', 'url'))
    else:
        # fallback to data/schemes.json (keeps compatibility)
        json_path = os.path.join(os.path.dirname(__file__), 'data', 'schemes.json')
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                schemes = json.load(f)
        except Exception:
            schemes = []
    return render(request, 'schemes.html', {'schemes': schemes})

# Chat API - receives JSON, returns JSON. Save chat logs.
@csrf_exempt
def chat_api(request):
    if request.method != "POST":
        return HttpResponseBadRequest("Only POST allowed")

    try:
        data = json.loads(request.body.decode('utf-8'))
    except Exception as e:
        logger.exception("Invalid JSON in chat_api")
        return JsonResponse({'error': 'invalid_json'}, status=400)

    user_input = data.get('message', '').strip()
    if not user_input:
        return JsonResponse({'error': 'empty_message'}, status=400)

    # Get AI reply (ai_logic may use DB Schemes)
    reply = ai_chat_response(user_input)

    # Save chat to DB asynchronously (simple save)
    try:
        ChatHistory.objects.create(user_message=user_input, bot_response=reply)
    except Exception:
        logger.exception("Failed to save ChatHistory")

    return JsonResponse({'reply': reply})    
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# Home page
def home(request):
    return render(request, 'home.html')

# Chat UI
def chat(request):
    return render(request, 'chatbot.html')

# Minimal AI logic
def simple_ai_response(user_input):
    user_input = (user_input or "").lower()
    
    greetings = ["hi", "hello", "namaste", "हॅलो", "नमस्कार"]
    if any(g in user_input for g in greetings):
        return "नमस्कार! मी AI सखी आहे. तुम्ही कोणत्या योजनांसाठी माहिती हवी आहे?"
    
    if "education" in user_input or "शिक्षण" in user_input:
        return "शिक्षण योजनांमध्ये 'मध्यान्ह' आणि 'स्नातक शिक्षण योजना' उपलब्ध आहेत."
    
    if "financial" in user_input or "आर्थिक" in user_input:
        return "आर्थिक योजनांमध्ये 'महिला स्वरोजगार योजना' आणि 'लघुउद्योग सहाय्यता' आहेत."
    
    return "क्षमस्व, मला समजले नाही. कृपया पुन्हा विचारू शकता."

