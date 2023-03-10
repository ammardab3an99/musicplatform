from django import forms
from django.contrib import admin
from .models import ExUser
# Register your models here.

class ExUserAdminForm(forms.ModelForm):
    class Meta:
        model = ExUser
        exclude = ()
        widgets = {
            'bio': forms.Textarea({'attrs': {'maxlength': 265}}),
        }

@admin.register(ExUser)
class ExUserAdmin(admin.ModelAdmin):
    form = ExUserAdminForm
    list_display = ('id', 'username', 'email', 'bio')
    