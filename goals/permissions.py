from rest_framework import permissions
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request

from goals.models import BoardParticipant, GoalCategory, Goal, GoalComment


class BoardPermissions(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        if request.method in permissions.SAFE_METHODS:
            return BoardParticipant.objects.filter(
                user=request.user, board=obj
            ).exists()
        return BoardParticipant.objects.filter(
            user=request.user, board=obj, role=BoardParticipant.Role.owner
        ).exists()


class GoalCategoryPermission(permissions.BasePermission):
    def has_object_permission(
        self, request: Request, view: GenericAPIView, obj: GoalCategory
    ):
        if not request.user.is_authenticated:
            return False
        if request.method in permissions.SAFE_METHODS:
            return BoardParticipant.objects.filter(
                user=request.user, board=obj.board_id
            ).exists()
        return BoardParticipant.objects.filter(
            user=request.user,
            board=obj.board_id,
            role__in=[BoardParticipant.Role.owner, BoardParticipant.Role.writer],
        ).exists()


class GoalPermission(permissions.BasePermission):
    def has_object_permission(self, request: Request, view: GenericAPIView, obj: Goal):
        if not request.user.is_authenticated:
            return False
        if request.method in permissions.SAFE_METHODS:
            return BoardParticipant.objects.filter(
                user=request.user, board=obj.category.board_id
            ).exists()
        return BoardParticipant.objects.filter(
            user=request.user,
            board=obj.category.board_id,
            role__in=[BoardParticipant.Role.owner, BoardParticipant.Role.writer],
        ).exists()


class CommentPermission(permissions.BasePermission):
    def has_object_permission(
        self, request: Request, view: GenericAPIView, obj: GoalComment
    ):
        if not request.user.is_authenticated:
            return False
        if request.method in permissions.SAFE_METHODS:
            return BoardParticipant.objects.filter(
                user=request.user, board=obj.goal.category.board_id
            ).exists()
        return BoardParticipant.objects.filter(
            user=request.user,
            board=obj.goal.category.board_id,
            role__in=[BoardParticipant.Role.owner, BoardParticipant.Role.writer],
        ).exists()
