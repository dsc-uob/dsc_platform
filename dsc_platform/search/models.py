from django.db import models


class Tag(models.Model):
    title = models.CharField(max_length=50, unique=True, primary_key=True)

    def __str__(self):
        return self.title


class SearchHistory(models.Model):
    text = models.CharField(max_length=255, help_text='The text that user wrote for search.')
    is_result_empty = models.BooleanField(help_text='If the result is not empty.')
    is_exist = models.BooleanField(null=True, blank=True,
                                   help_text='To check if the user found what he was looking for.')
    tags = models.ManyToManyField('Tag', related_name='searched_tags')
    user = models.ForeignKey('user.User', on_delete=models.RESTRICT)
    search_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text
