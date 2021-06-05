from django.db import models


# Base models class

class BasePostModel(models.Model):
    """
    The base model of post models.
    """
    title = models.CharField(max_length=255)
    caption = models.TextField()
    user = models.ForeignKey(
        'user.User',
        on_delete=models.CASCADE,
    )
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __str__(self):
        return f'{self.title}, by: ({self.user.username})'


class BaseCommentModel(models.Model):
    """
    The base class of comment of post models.
    """
    body = models.TextField()
    user = models.ForeignKey(
        'user.User',
        on_delete=models.CASCADE,
    )

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __str__(self):
        return f'{self.body}, by: ({self.user.username})'


# Article models
class Article(BasePostModel):
    """
    The articles model.
    """
    pass


class ArticleComment(BaseCommentModel):
    """
    The comment model of Articles.
    """
    article = models.ForeignKey(
        'Article',
        on_delete=models.CASCADE,
    )


EnquiryType = (
    ('I', 'ISSUE'),
    ('Q', 'QUESTION'),
)


# Enquiry models
class Enquiry(BasePostModel):
    """
    The model of Q&A and Issues.
    """
    solved = models.BooleanField(default=False)
    type = models.CharField(choices=EnquiryType, max_length=1)

    def __str__(self):
        return f'[{self.get_type_display()}] {self.title}'


class EnquiryComment(BaseCommentModel):
    """
    The comment model of Enquiries.
    """
    enquiry = models.ForeignKey(
        'Enquiry',
        on_delete=models.CASCADE,
    )
