from django.db import models
from django.contrib.auth.models import User


class Author (models.Model):  # Авторы статей/новостей (далее - постов)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def update_rating(self, new_rating):
        self.rating = new_rating
        self.save()

    def __str__(self):
        return f'{self.user}'

class Category (models.Model):
    name = models.CharField(max_length=30, unique=True,)

    def __str__(self):
        return f'{self.name.title()}'


class Post (models.Model):  # Модель поста  (статьи/новости)
    article = 'ar'
    news = 'nw'

    VIEW = [
        (article, 'Статья'),
        (news, 'Новость')
        ]
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    view = models.CharField(max_length=2, choices=VIEW, default=article)
    create_time = models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField(Category, through='PostCategory')
    heading = models.CharField(max_length=255)
    text_post = models.TextField()
    rating_post = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.heading} {self.text_post[:100]} '

    def like(self):
        self.rating_post += 1
        self.save()

    def dislike(self):
        self.rating_post -= 1
        self.save()

    def preview(self):
        size = 124 if len(self.text_post) > 124 else len(self.text_post)
        return self.text_post[:size] + "..."

    def get_absolute_url(self):
        return f'/news/{self.id}'

class PostCategory (models.Model):  # Модель для связи таблиц Пост и Категории,для организации 3-й формы нормализации
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment (models.Model):  # Комметарии к постам
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_text = models.TextField()
    create_time = models.DateTimeField(auto_now_add=True)
    rating_comment = models.IntegerField(default=0)

    def like(self):
        self.rating_comment += 1
        self.save()

    def dislike(self):
        self.rating_comment -= 1
        self.save()