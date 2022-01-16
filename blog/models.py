from django.conf import settings
from django.db import models
from django.utils import timezone

class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) # первичный ключ таблицы (генерируется автоматически при создании нового поста)
    # с каскадным удалением всех записей при удалении автора
    title = models.CharField(max_length=150) # текстовое поле ограниченное 150 исмволами
    text = models.TextField() # текстовое поле, неограниченное размерами
    created = models.DateTimeField(default=timezone.now) # исходя из названия, будет отображать время создания поста

    def __str__(self): # для понятного отображения в админке
        return self.title + ' | ' + str(self.author)  # т.к. author это объект, необходимо преобразовать его в строку
