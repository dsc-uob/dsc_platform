from rest_framework import filters


class UserOwnFilter(filters.BaseFilterBackend):
    """Return the objects for this user."""

    def filter_queryset(self, request, queryset, view):
        user_id = request.query_params.get('user')

        if not user_id:
            return queryset

        return queryset.filter(
            user_id=user_id,
        )
