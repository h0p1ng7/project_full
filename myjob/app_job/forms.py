from django import forms
from .models import Advertisement

class AdvertisementsForm(forms.ModelForm):

    class Meta:
        model = Advertisement
        fields = ['title', 'description', 'price', 'auction', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control form-control-lg'}),
            'description': forms.Textarea(attrs={'class': 'form-control form-control-lg'}),
            'price': forms.NumberInput(attrs={'class': 'form-control form-control-lg'}),
            'auction': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'image': forms.FileInput(attrs={'class': 'form-control from-control-lg'}),
        }

    # создаем метод для валидации поля title, он будет вызываться при отправке формы
    # и проверять начинается ли заголовок с ? знака
    def clean_title(self):
        title = self.cleaned_data['title']
        if title.startswith('?'):
            raise  forms.ValidationError("Заголовок не может начинаться с вопросительного знака.")
        return title
