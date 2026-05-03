from django.apps import AppConfig

class WomenAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'women_app'  # 👈 must match your folder name exactly
    verbose_name = "AI Sakhi - Women Welfare Schemes"
