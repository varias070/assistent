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

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Продашка'
        verbose_name_plural = 'Продашки'


class Chanel(models.Model):
    title = models.TextField(null=True, verbose_name='Название канала')
    login_data = models.TextField(null=True, verbose_name='пароль')
    phone = models.CharField(verbose_name='привязанный номер телефона', null=True, max_length=30)

    class Meta:
        verbose_name = 'Канал'
        verbose_name_plural = 'Канал'

    def __str__(self):
        return self.title


class Published(models.Model):
    author = models.OneToOneField('Chanel', on_delete=models.CASCADE)
    article = models.OneToOneField('Article', on_delete=models.CASCADE)
    prodashka = models.OneToOneField('Prodashka', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = 'Публикация'
        verbose_name_plural = 'Публикации'


class PublishedPost(models.Model):
    author = models.ForeignKey('Chanel', on_delete=models.CASCADE, verbose_name='Канал')
    post = models.ForeignKey('Post', on_delete=models.CASCADE, verbose_name='Пост')
    prodashka = models.ForeignKey('Prodashka', on_delete=models.CASCADE, null=True, verbose_name='продашка')

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = 'Публикация поста'
        verbose_name_plural = 'Публикации постов'
