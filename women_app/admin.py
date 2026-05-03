from django.contrib import admin
from .models import ChatHistory, Scheme


# ---------------------------------------------------------
# 🔹 Admin: Chat History (Chatbot Logs)
# ---------------------------------------------------------
@admin.register(ChatHistory)
class ChatHistoryAdmin(admin.ModelAdmin):
    list_display = ('user_message', 'bot_response', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user_message', 'bot_response')
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)

    fieldsets = (
        ('Chat Details', {
            'fields': ('user_message', 'bot_response')
        }),
        ('System Information', {
            'fields': ('created_at',),
        }),
    )


# ---------------------------------------------------------
# 🔹 Admin: Scheme Database (Government Schemes)
# ---------------------------------------------------------
@admin.register(Scheme)
class SchemeAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'category', 'gender',
        'min_age', 'max_age', 'income_limit'
    )
    list_filter = ('category', 'gender')
    search_fields = ('name', 'description', 'eligibility')
    ordering = ('category', 'name')

    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'category', 'description')
        }),
        ('Eligibility Criteria', {
            'fields': ('eligibility', 'min_age', 'max_age', 'income_limit', 'gender')
        }),
        ('Useful Link', {
            'fields': ('url',)
        }),
    )

    # Show short snippet of description in admin list
    def short_description(self, obj):
        if len(obj.description) > 60:
            return obj.description[:60] + "..."
        return obj.description

    short_description.short_description = "Description"
