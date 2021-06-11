from rest_framework import filters


class ArticleCommentFilter(filters.BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):
        article = request.query_params.get('article')
        return queryset.filter(article=article)


class EnquiryCommentFilter(filters.BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):
        enquiry = request.query_params.get('enquiry')
        return queryset.filter(enquiry=enquiry)
