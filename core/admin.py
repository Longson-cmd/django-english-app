from django.contrib import admin
from core.models import Words, Sentences, DefaultCategories, DefaultOptions, Topics, SelfIntroduce


admin.site.register(Words)
admin.site.register(Sentences)
admin.site.register(DefaultCategories)
admin.site.register(DefaultOptions)
admin.site.register(SelfIntroduce)
admin.site.register(Topics)

# Register your models here.
