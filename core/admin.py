from django.contrib import admin
from core.models import Words, Sentences, DefaultCategories, DefaultOptions, Topics, SelfIntroduce, CustomerProfile




admin.site.register(DefaultCategories)
admin.site.register(DefaultOptions)
admin.site.register(SelfIntroduce)
admin.site.register(Topics)



@admin.register(Sentences)
class SentencesAdmin(admin.ModelAdmin):
    search_fields = ['sentence', 'word__word_key']
# Register your models here.

@admin.register(Words)
class WordsAdmin(admin.ModelAdmin):
    search_fields = ['word_key', 'user__username']

@admin.register(CustomerProfile)
class CustomerProfileAdmin(admin.ModelAdmin):
    search_fields = ['user__username']
    def save_model(self, request, obj, form, change):
        # If the field is_paying_customer was changed to True
        if 'is_paying_customer' in form.changed_data and obj.is_paying_customer:
            obj.activate_monthly_payment()
        else:
            super().save_model(request, obj, form, change)