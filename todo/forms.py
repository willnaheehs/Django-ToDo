from django.forms import ModelForm
from .models import Todo

#used when user creates forms
class TodoForm(ModelForm):
    class Meta:
        model = Todo
        fields = ['title', 'memo', 'important']