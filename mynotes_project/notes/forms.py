from django import forms
from .models import Note, Category
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser


class NoteForm(forms.ModelForm):
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.none(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label='Категории'
    )

    class Meta:
        model = Note
        fields = ['title', 'content', 'categories']
        widgets = {
            'content': forms.Textarea(attrs={
                'rows': 20,
                'style': 'min-height: 300px; width: 100%; resize: vertical;'
            }),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['categories'].queryset = Category.objects.filter(owner=user)


        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('title', css_class='form-group col-md-12'),
                css_class='form-row'
            ),
            Row(
                Column('content', css_class='form-group col-md-12'),
                css_class='form-row'
            ),
            Row(
                Column('categories', css_class='form-group col-md-12'),
                css_class='form-row'
            ),
            Submit('submit', 'Сохранить', css_class='btn btn-primary')
        )


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email')