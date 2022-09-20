from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.urls import reverse


class Author(models.Model):
    authorUser = models.OneToOneField(User, on_delete=models.CASCADE)
    authorRating = models.IntegerField(default=0)

    def update_rating(self):
        postR = self.post_set.aggregate(postRating=Sum('rating'))
        PSum = 0
        PSum += postR.get('postRating')

        commentR = self.authorUser.comment_set.aggregate(commentRating=Sum('rating'))
        CSum = 0
        CSum += commentR.get('commentRating')

        self.authorRating = PSum * 3 + CSum
        self.save()

    def __str__(self):
        return f'{self.authorUser}'


class Category(models.Model):
    categoryName = models.CharField(max_length=150, unique=True)
    subscribers = models.ManyToManyField(User, through='CategorySubscribers', blank=True)

    def __str__(self):
        return f'{self.categoryName}'


class CategorySubscribers(models.Model):
    subscriberThrough = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    categoryThrough = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)


class Post(models.Model):
    NEWS = 'NE'
    ARTICLE = 'AR'
    CHOICES = [
        (NEWS, 'Новость'),
        (ARTICLE, 'Статья')
    ]

    postAuthor = models.ForeignKey(Author, on_delete=models.CASCADE)

    categoryChoice = models.CharField(max_length=2,
                                      choices=CHOICES,
                                      default=NEWS)
    date = models.DateTimeField(auto_now_add=True)
    Category = models.ManyToManyField(Category, related_name='posts', through='PostCategory', verbose_name='Категория')
    title = models.CharField(max_length=150)
    text = models.TextField()
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return self.postText[0:123] + '...'

    def __str__(self):
        return f'Статья {self.title} {self.text}. Автор: {self.postAuthor.authorUser.username}, Категория: {self.categoryChoice}'

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])


class PostCategory(models.Model):
    postThrough = models.ForeignKey(Post, on_delete=models.CASCADE)
    categoryThrough = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.postThrough)


class Comment(models.Model):
    commentPost = models.ForeignKey(Post, on_delete=models.CASCADE)
    commentUser = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def __str__(self):
        return f'{self.date, self.commentUser.username, self.rating, self.text}'
