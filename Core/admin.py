from django.contrib import admin
from .models import PasswordReset, Brain, BrainImage

admin.site.register(PasswordReset)
admin.site.register(Brain)
admin.site.register(BrainImage)