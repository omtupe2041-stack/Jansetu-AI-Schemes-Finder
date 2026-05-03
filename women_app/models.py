from django.db import models


# -----------------------------------------
# 1️⃣ Chat History Model (Saves chatbot conversation logs)
# -----------------------------------------
class ChatHistory(models.Model):
    user_message = models.TextField()
    bot_response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Chat Log"
        verbose_name_plural = "Chat Logs"

    def __str__(self):
        return f"{self.user_message[:40]}..."


# -----------------------------------------
# 2️⃣ Scheme Model (Dynamic storage for schemes instead of JSON)
# -----------------------------------------
class Scheme(models.Model):
    CATEGORY_CHOICES = [
        ('education', 'Education'),
        ('financial', 'Financial Help'),
        ('empowerment', 'Women Empowerment'),
        ('health', 'Health'),
        ('other', 'Other'),
    ]

    GENDER_CHOICES = [
        ('any', 'Any'),
        ('female', 'Female'),
        ('male', 'Male'),
    ]

    name = models.CharField(max_length=200)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    description = models.TextField()
    eligibility = models.TextField()

    min_age = models.IntegerField(default=0)
    max_age = models.IntegerField(default=100)
    income_limit = models.IntegerField(default=9999999)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='any')

    url = models.URLField(blank=True)

    class Meta:
        ordering = ['category', 'name']
        verbose_name = "Government Scheme"
        verbose_name_plural = "Government Schemes"

    def __str__(self):
        return self.name
