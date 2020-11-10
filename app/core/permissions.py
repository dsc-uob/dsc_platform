from rest_framework.permissions import BasePermission, \
    SAFE_METHODS

from django.core.exceptions import ObjectDoesNotExist

from core import models


class UpdateOwnPermission(BasePermission):
    """Check if this your on thing."""

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        """Return if this object has permission."""
        if not request.user:
            return False

        if request.method in SAFE_METHODS:
            return True

        return bool(obj.user.id == request.user.id)


class ManageSessionPermission(BasePermission):
    """Check if this session for you or not."""

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        """Return if this object has permission."""
        if not request.user:
            return False

        if request.method in SAFE_METHODS:
            try:
                obj.members.get(
                    user_id=request.user.id,
                )
                return True
            except ObjectDoesNotExist:
                return False

        return bool(obj.owner.id == request.user.id)


class SessionMemberPermission(BasePermission):
    """Check if this session for you or not."""

    def has_permission(self, request, view):
        chat_session_id = request.query_params.get('chat_session')
        try:
            chat_session = models.ChatSession.objects.get(
                id=chat_session_id,
            )
            chat_session.members.get(
                user_id=request.user.id,
            )
            return True
        except ObjectDoesNotExist:
            return False

    def has_object_permission(self, request, view, obj):
        """Return if this object has permission."""
        if not request.user:
            return False

        if request.method in SAFE_METHODS:
            try:
                obj.chat_session.members.get(
                    user_id=request.user.id,
                )
                return True
            except ObjectDoesNotExist:
                return False
        if request.method in SAFE_METHODS:
            return True

        return bool(obj.chat_session.owner.id == request.user.id)
