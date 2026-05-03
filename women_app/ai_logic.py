import random
from .eligibility import check_scheme_eligibility  # remains useful
from .models import Scheme
from django.db.models import Q

def _simple_tokenize(text: str):
    return [t.strip().lower() for t in text.split() if t.strip()]

def ai_chat_response(user_input: str):
    user_input = (user_input or "").strip()
    lower = user_input.lower()

    # greetings
    if any(g in lower for g in ["hello", "hi", "namaste", "नमस्कार", "हॅलो"]):
        return "नमस्कार! 😊 मी AI सखी आहे — कृपया तुमचे वय आणि उत्पन्न सांगा किंवा 'मला योजना दाखवा' असा लिहा."

    # ask for scheme categories
    if "scheme" in lower or "yojana" in lower or "योजना" in lower:
        return "कृपया सांगा — तुम्हाला शिक्षण / आर्थिक / आरोग्य / कौशल्य विकास यापैकी कोणत्या प्रकारची योजना हवी आहे?"

    # quick eligibility checks triggered by keywords
    if any(word in lower for word in ["ladki", "bahin", "mahila", "woman", "महिला", "स्त्री"]):
        # example: default values if user hasn't provided details
        eligible_names = check_scheme_eligibility({"gender": "female", "age": 21, "income": 200000})
        if eligible_names:
            return "✅ तुम्ही या योजनांसाठी पात्र आहात:\n" + "\n".join(f"- {n}" for n in eligible_names[:8])
        return "माफ करा, सध्याच्या निकषांनुसार कोणतीही योजना सापडली नाही."

    # If user asks "show me schemes" or gives keywords, search DB
    tokens = _simple_tokenize(lower)
    if tokens:
        # Build a simple DB query: name__icontains OR description__icontains OR category
        q = Q()
        for t in tokens[:6]:  # limit tokens to avoid huge queries
            q |= Q(name__icontains=t) | Q(description__icontains=t) | Q(eligibility__icontains=t) | Q(category__icontains=t)
        matches = Scheme.objects.filter(q).distinct()[:12]
        if matches.exists():
            resp_lines = ["येथे सापडलेल्या योजना आहेत:"]
            for s in matches:
                resp_lines.append(f"- {s.name} ({s.category.title()}) — {s.url or 'No link'}")
            return "\n".join(resp_lines)

    # fallback friendly responses
    responses = [
        "कृपया अधिक माहिती द्या म्हणजे मी मदत करू शकेन.",
        "मी अजून शिकतेय 🙂 — पुन्हा एकदा प्रश्न विचारू शकता का?",
        "त्या विषयावर थोडं अधिक सांगाल का?"
    ]
    return random.choice(responses)
