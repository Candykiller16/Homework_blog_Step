from django.conf import settings
from django.db import models
from django.utils import timezone
from taggit.managers import TaggableManager

class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) # первичный ключ таблицы (генерируется автоматически при создании нового поста)
    # с каскадным удалением всех записей при удалении автора
    title = models.CharField(max_length=150) # текстовое поле ограниченное 150 исмволами
    text = models.TextField() # текстовое поле, неограниченное размерами
    created = models.DateTimeField(default=timezone.now) # исходя из названия, будет отображать время создания поста
    tags = TaggableManager()

    def __str__(self): # для понятного отображения в админке
        return self.title + ' | ' + str(self.author)  # т.к. author это объект, необходимо преобразовать его в строку


class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE) # связь по внешнему ключу с конкретным постом
    # Атрибут related_name позволяет нам присваивать имя атрибуту, который мы используем для связи. Определив это,
    # мы можем извлечь пост комментария с помощью comment.post и извлечь все комментарии к посту с помощью post.comments.all().
    name = models.CharField(max_length=80)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True) # поле active имеет будево значение, чтобы отключить нежелательные комментарии

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('-created',)

    def __str__(self):
        return 'Комментарий от - {} для: - {}'.format(self.name, self.post)