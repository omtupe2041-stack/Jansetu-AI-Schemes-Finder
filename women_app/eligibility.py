import os, json
from .models import Scheme

def _load_schemes_from_json():
    path = os.path.join(os.path.dirname(__file__), 'data', 'schemes.json')
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return []

def get_all_schemes():
    # Try DB first
    try:
        qs = Scheme.objects.all()
        if qs.exists():
            return list(qs.values('name','category','description','eligibility','min_age','max_age','income_limit','gender','url'))
    except Exception:
        pass
    return _load_schemes_from_json()

def check_scheme_eligibility(user_data):
    schemes = get_all_schemes()
    eligible = []
    for s in schemes:
        min_age = s.get("min_age", 0)
        max_age = s.get("max_age", 100)
        income_limit = s.get("income_limit", 99999999)
        gender = s.get("gender", "any")

        if (min_age <= user_data.get("age", 0) <= max_age) and \
           (user_data.get("income", 0) <= income_limit) and \
           (gender in ["any", user_data.get("gender", "any")]):
            eligible.append(s.get("name"))
    return eligible
