from rest_framework import permissions
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request

from goals.models import BoardParticipant, GoalCategory, Goal, GoalComment, Board


class BoardPermissions(permissions.BasePermission):
    """
    Class with boards permissions
    """

    def has_object_permission(
        self, request: Request, view: GenericAPIView, obj: Board
    ) -> bool:
        """Check has user permission for current board"""
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
    """
    Class with category permissions
    """

    def has_object_permission(
        self, request: Request, view: GenericAPIView, obj: GoalCategory
    ) -> bool:
        """Check has user permission for current category"""
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
    """
    Class with goal permissions
    """

    def has_object_permission(
        self, request: Request, view: GenericAPIView, obj: Goal
    ) -> bool:
        """Check has user permission for current goal"""
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
    """
    Class with comment permissions
    """

    def has_object_permission(
        self, request: Request, view: GenericAPIView, obj: GoalComment
    ) -> bool:
        """Check has user permission for current comment"""
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
