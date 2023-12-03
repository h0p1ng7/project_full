from django.contrib.auth import get_user_model
from django.db import models
from django.contrib import admin
from django.utils.html import format_html
from django.utils import timezone
from django.urls import reverse

User = get_user_model()

class Advertisement(models.Model):
    title = models.CharField('Заголовок', max_length=64)
    description = models.TextField('Описание')
    price = models.DecimalField('Цена', max_length=15, decimal_places=2, max_digits=20)
    auction = models.BooleanField('Торг', help_text="Отметьте, если торг уместен")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # Добавляем 2 параметра чтобы можно было необязательно загружать картинку, не забываем сделать миграции
    image = models.ImageField('Изображение',  upload_to='myjob/', null=True, blank=True)

    user = models.ForeignKey(User, verbose_name='пользователь', on_delete=models.CASCADE, null=True, default=None)

    def thumbnail(self):
        if self.image:
            return format_html('<img src="{}" width="100" height="100" />', self.image.url)
        else:
            return format_html('<img src="{}" width="100" height="100" />', 'static/img/adv.png')

    @admin.display(description='Картинка')
    def image_thumbnail(self):
        return self.thumbnail()

    @admin.display(description='Время обновления')
    def updated_date(self):
        if self.updated_at.date() == timezone.now().date():
            updated_time = self.updated_at.time().strftime("%H:%M:%S")
            return format_html(
                '<span style="color: yellow; font-weight: bold;">Сегодня в {}</span>', updated_time
            )
        return self.updated_at.strftime("%d:%m:%Y %H:%M:%S")

    @admin.display(description='Дата создания')
    def created_date(self):
        if self.created_at.date() == timezone.now().date():
            created_time = self.created_at.time().strftime("%H:%M:%S")
            return format_html(
                '<span style="color: green; font-weight: bold;">Сегодня в {}</span>', created_time
            )
        return self.created_at.strftime("%d:%m:%Y %H:%M:%S")

    class Meta:
        db_table = 'advertisements'

    def __str__(self):
        return f'<Advertisement: Advertisement(id={self.id}, title={self.title}, price={self.price: .2f})>.'

    def get_absolute_url(self):
        return reverse('adv-detail', kwargs={'pk': self.pk})
