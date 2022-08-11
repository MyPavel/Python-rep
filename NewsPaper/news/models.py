from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum


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
        return f'{self.authorUser, self.authorRating}'


class Category(models.Model):
    categoryName = models.CharField(max_length=150, unique=True)


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
    postCategory = models.ManyToManyField(Category, through='PostCategory')
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
        return f'{self.date, self.postAuthor.authorUser.username, self.rating, self.title, self.text}'


class PostCategory(models.Model):
    postThrough = models.ForeignKey(Post, on_delete=models.CASCADE)
    categoryThrough = models.ForeignKey(Category, on_delete=models.CASCADE)


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
