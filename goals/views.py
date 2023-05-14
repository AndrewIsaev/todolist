from django.db import transaction
from django.db.models import QuerySet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, filters
from rest_framework import permissions
from rest_framework.pagination import LimitOffsetPagination

from goals.filters import GoalDateFilter
from goals.models import GoalCategory, Goal, GoalComment, Board
from goals.permissions import (
    BoardPermissions,
    GoalCategoryPermission,
    GoalPermission,
    CommentPermission,
)
from goals.serializers import (
    GoalCreateSerializer,
    GoalCategoryCreateSerializer,
    GoalCategoryListSerializer,
    GoalSerializer,
    GoalCommentCreateSerializer,
    GoalCommentSerializer,
    BoardCreateSerializer,
    BoardSerializer,
)


class GoalCategoryCreateView(generics.CreateAPIView):
    """
    Category create view
    """

    permission_classes = [permissions.IsAuthenticated, GoalCategoryPermission]
    serializer_class = GoalCategoryCreateSerializer


class GoalCategoryListView(generics.ListAPIView):
    """
    Category list view
    """

    permission_classes = [
        permissions.IsAuthenticated,
    ]
    serializer_class = GoalCategoryListSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ['board']
    ordering_fields = ['title', 'created']
    ordering = ['title']
    search_fields = ['title']

    def get_queryset(self) -> QuerySet:
        return GoalCategory.objects.filter(
            board__participants__user=self.request.user
        ).exclude(is_deleted=True)


class GoalCategoryView(generics.RetrieveUpdateDestroyAPIView):
    """
    Category retrieve update delete views
    """

    permission_classes = [permissions.IsAuthenticated, GoalCategoryPermission]
    serializer_class = GoalCategoryListSerializer

    def get_queryset(self) -> QuerySet:
        return GoalCategory.objects.filter(
            board__participants__user=self.request.user, is_deleted=False
        )

    def perform_destroy(self, instance: GoalCategory) -> None:
        """
        If categories were delete, they mark as delete in database
        :param instance: category
        :return: none
        """
        with transaction.atomic():
            instance.is_deleted = True
            instance.save(update_fields=('is_deleted',))
            instance.goals.update(status=Goal.Status.archived)


class GoalCreateView(generics.CreateAPIView):
    """
    Goal create view
    """

    permission_classes = [permissions.IsAuthenticated, GoalPermission]
    serializer_class = GoalCreateSerializer


class GoalListView(generics.ListAPIView):
    """
    Goal list view
    """

    permission_classes = [
        permissions.IsAuthenticated,
    ]
    serializer_class = GoalSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_class = GoalDateFilter
    ordering_fields = ['title', 'created']
    ordering = ['title']
    search_fields = ['title', 'description']

    def get_queryset(self) -> QuerySet:
        return (
            Goal.objects.select_related('user')
            .filter(category__is_deleted=False)
            .exclude(status=Goal.Status.archived)
        )


class GoalView(generics.RetrieveUpdateDestroyAPIView):
    """
    Goal retrieve update destroy view
    """

    permission_classes = [permissions.IsAuthenticated, GoalPermission]
    serializer_class = GoalSerializer

    def get_queryset(self) -> QuerySet:
        return (
            Goal.objects.select_related('user')
            .filter(category__is_deleted=False)
            .exclude(status=Goal.Status.archived)
        )

    def perform_destroy(self, instance: Goal) -> None:
        """
        If goals were delete, they mark as archived in database
        :param instance:
        :return: none
        """
        instance.status = Goal.Status.archived
        instance.save(update_fields=('status',))


class GoalCommentCreateView(generics.CreateAPIView):
    """
    Comment create view
    """

    serializer_class = GoalCommentCreateSerializer
    permission_classes = [permissions.IsAuthenticated, CommentPermission]


class GoalCommentListView(generics.ListAPIView):
    """
    Comment list view
    """

    serializer_class = GoalCommentSerializer
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['goal']
    ordering_fields = ['created', 'updated']
    ordering = ['-created']

    def get_queryset(self) -> QuerySet:
        return GoalComment.objects.all().exclude(goal__status=Goal.Status.archived)


class GoalCommentView(generics.RetrieveUpdateDestroyAPIView):
    """
    Comment retrieve update destroy view
    """

    serializer_class = GoalCommentSerializer
    permission_classes = [permissions.IsAuthenticated, CommentPermission]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['goal']
    ordering_fields = ['created', 'updated']
    ordering = ['-created']

    def get_queryset(self) -> QuerySet:
        return (
            GoalComment.objects.select_related('user')
            .filter(user=self.request.user)
            .exclude(goal__status=Goal.Status.archived)
        )


class BoardCreateView(generics.CreateAPIView):
    """
    Board create view
    """

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = BoardCreateSerializer


class BoardListView(generics.ListAPIView):
    """
    Board list view
    """

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = BoardCreateSerializer
    filter_backends = [filters.OrderingFilter]
    ordering = ['title']

    def get_queryset(self):
        return Board.objects.filter(participants__user_id=self.request.user.id).exclude(
            is_deleted=True
        )


class BoardDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Board retrieve update destroy view
    """

    permission_classes = [permissions.IsAuthenticated, BoardPermissions]
    serializer_class = BoardSerializer

    def get_queryset(self):
        return Board.objects.prefetch_related('participants__user').filter(
            is_deleted=False
        )

    def perform_destroy(self, instance: Board):
        """
        If boards were delete, categories mark as delete in database goal mark as archived
        :param instance: board
        :return: none
        """
        with transaction.atomic():
            Board.objects.filter(id=instance.id).update(is_deleted=True)
            instance.categories.update(is_deleted=True)
            Goal.objects.filter(category__board=instance).update(
                status=Goal.Status.archived
            )
