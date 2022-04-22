from django.db import models


class Article(models.Model):
    header = models.TextField(null=True, verbose_name='Заголовок')
    link = models.TextField(null=True)

    def __str__(self):
        return self.header

    class Meta:
        ordering = ('header',)
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
        app_label = 'articles'


class ArticleBlock(models.Model):
    article = models.ForeignKey('Article', on_delete=models.CASCADE)
    text = models.TextField(null=True, verbose_name='Текст')
    src = models.URLField(null=True, verbose_name='Текст')
    ordering_number = models.IntegerField(null=True, max_length=20)

    def __str__(self):
        return self.article


class Post(models.Model):
    title = models.TextField(null=True, verbose_name='Название')
    text = models.TextField(null=True, verbose_name='Текст')
    image = models.ImageField(upload_to='post/%Y/%m', null=True, verbose_name='Картинка')
    link = models.TextField(null=True, verbose_name='Ссылка', blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'


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


class Video(models.Model):
    header = models.TextField(null=True, verbose_name='Название')
    link = models.FileField(upload_to='video/%Y/%m', null=True, verbose_name='Видео')
    cover = models.ImageField(upload_to='video/cover/%Y/%m', null=True, verbose_name='Обложка')

    class Meta:
        verbose_name = 'Видео'
        verbose_name_plural = 'Видео'

    def __str__(self):
        return self.header


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


class PublishedArticle(models.Model):
    channel = models.ForeignKey('Channel', on_delete=models.CASCADE)
    article = models.ForeignKey('Article', on_delete=models.CASCADE)
    prodashka = models.ForeignKey('Prodashka', on_delete=models.CASCADE)
    proxy = models.ForeignKey('Proxy', on_delete=models.CASCADE, null=True, verbose_name='Прокси')
    state = models.BooleanField(default=False, verbose_name='О')

    def __str__(self):
        return self.article

    class Meta:
        verbose_name = 'Публикация статей'
        verbose_name_plural = 'Публикации статей'


class PublishedPost(models.Model):
    channel = models.ForeignKey('Channel', on_delete=models.CASCADE, verbose_name='Канал')
    post = models.ForeignKey('Post', on_delete=models.CASCADE, verbose_name='Пост')
    state = models.BooleanField(default=False, verbose_name='О')
    prodashka = models.ForeignKey('Prodashka', on_delete=models.CASCADE, null=True, verbose_name='Продашка')
    proxy = models.ForeignKey('Proxy', on_delete=models.CASCADE, null=True, verbose_name='Прокси')

    def __str__(self):
        return self.post

    class Meta:
        verbose_name = 'Публикация поста'
        verbose_name_plural = 'Публикации постов'


class PublishedVideo(models.Model):
    video = models.ForeignKey('Video', on_delete=models.CASCADE, verbose_name='Видео')
    channel = models.ForeignKey('Channel', on_delete=models.CASCADE, verbose_name='Канал')
    state = models.BooleanField(default=False, verbose_name='О')
    prodashka = models.ForeignKey('Prodashka', on_delete=models.CASCADE, null=True, verbose_name='Продашка')
    proxy = models.ForeignKey('Proxy', on_delete=models.CASCADE, null=True, verbose_name='Прокси')

    def __str__(self):
        return self.video

    class Meta:
        verbose_name = 'Публикация видео'
        verbose_name_plural = 'Публикации видео'
