from django.contrib import admin

from . import models

# Register your models here.
admin.site.register(models.Article)
admin.site.register(models.ArticleComment)
admin.site.register(models.Enquiry)
admin.site.register(models.EnquiryComment)
