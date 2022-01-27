from django.contrib.auth.models import User
from django.db import models


class Article(models.Model):
    header = models.TextField(null=True, verbose_name='Заголовок')
    text = models.TextField(null=True, verbose_name='Текст')
    link = models.TextField(null=True)

    def __str__(self):
        return self.link

    class Meta:
        ordering = ('header',)
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
        app_label = 'articles'


class Post(models.Model):
    text = models.TextField(null=True, verbose_name='Текст')
    image = models.ImageField(upload_to='post/%Y/%m', null=True, verbose_name='Картинка')
    link = models.TextField(null=True, verbose_name='Ссылка', blank=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'


class Image(models.Model):
    image = models.ImageField(verbose_name='картинка')
    link = models.TextField(null=True)
    article = models.ForeignKey('Article', null=True,  on_delete=models.CASCADE,
                                verbose_name='статья на которой расположенна картинка')

    def __str__(self):
        return self.article.header

    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'


class Prodashka(models.Model):
    title = models.TextField(null=True, verbose_name='Название продашки')
    text = models.TextField(null=True)
    link = models.CharField(null=True, max_length=120)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Продашка'
        verbose_name_plural = 'Продашки'


class Channel(models.Model):
    title = models.TextField(null=True, verbose_name='Название канала')
    login_data = models.TextField(null=True, verbose_name='пароль')
    phone = models.CharField(verbose_name='привязанный номер телефона', null=True, max_length=30, blank=True)

    class Meta:
        verbose_name = 'Канал'
        verbose_name_plural = 'Канал'

    def __str__(self):
        return self.title


class Proxy(models.Model):
    ip = models.CharField(null=True, max_length=20)
    login = models.CharField(null=True, max_length=20)
    port = models.IntegerField(null=True, max_length=20)
    password = models.CharField(null=True, max_length=30)

    def __str__(self):
        return self.ip

    class Meta:
        verbose_name = 'Прокси'
        verbose_name_plural = 'Прокси'


class Published(models.Model):
    channel = models.OneToOneField('Channel', on_delete=models.CASCADE)
    article = models.OneToOneField('Article', on_delete=models.CASCADE)
    prodashka = models.OneToOneField('Prodashka', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = 'Публикация'
        verbose_name_plural = 'Публикации'


class PublishedPost(models.Model):
    channel = models.ForeignKey('Channel', on_delete=models.CASCADE, verbose_name='Канал')
    post = models.ForeignKey('Post', on_delete=models.CASCADE, verbose_name='Пост')
    state = models.BooleanField(default=False, verbose_name='Опубликовано')
    prodashka = models.ForeignKey('Prodashka', on_delete=models.CASCADE, null=True, verbose_name='Продашка')
    proxy = models.ForeignKey('Proxy', on_delete=models.CASCADE, null=True, verbose_name='Прокси')

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = 'Публикация поста'
        verbose_name_plural = 'Публикации постов'
