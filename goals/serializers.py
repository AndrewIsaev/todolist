from datetime import date

from django.db import transaction
from django.utils import timezone
from rest_framework import serializers
from rest_framework.exceptions import ValidationError, PermissionDenied

from core.models import User
from core.serializers import ProfileSerializer
from goals.models import GoalCategory, Goal, GoalComment, Board, BoardParticipant


class GoalCategoryCreateSerializer(serializers.ModelSerializer):
    """
    Category create serializer
    """

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = GoalCategory
        read_only_fields = ('id', 'created', 'updated', 'user', 'is_deleted')
        fields = '__all__'

    def validate_board(self, board: Board) -> Board:
        """
        Check is board deleted and has user permission
        :param board: board
        :return: board or validation error
        """
        if board.is_deleted:
            raise ValidationError('Board is deleted')

        if not BoardParticipant.objects.filter(
            board_id=board.id,
            role__in=[BoardParticipant.Role.owner, BoardParticipant.Role.writer],
            user_id=self.context['request'].user.id,
        ).exists():
            raise PermissionDenied
        return board


class GoalCategoryListSerializer(GoalCategoryCreateSerializer):
    """
    Category list serializer
    """

    user = ProfileSerializer(read_only=True)


class GoalCreateSerializer(serializers.ModelSerializer):
    """
    Goal create serializer
    """

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Goal
        read_only_fields = (
            'id',
            'created',
            'updated',
            'user',
        )
        fields = '__all__'

    def validate_category(self, value: GoalCategory) -> GoalCategory:
        """
        Check is category deleted and ha user permission
        :param value: category
        :return: category or permission denied
        """
        if value.is_deleted:
            raise ValidationError('Category not found')

        if not BoardParticipant.objects.filter(
            board_id=value.board.id,
            role__in=[BoardParticipant.Role.owner, BoardParticipant.Role.writer],
            user_id=self.context['request'].user.id,
        ).exists():
            raise PermissionDenied
        return value

    def validate_due_date(self, value: date | None) -> date | None:
        """
        Check that date was not in the past
        :param value: date
        :return: date or validation error
        """
        if value:
            if value < timezone.now().date():
                raise ValidationError('Date in the past')
            return value


class GoalSerializer(GoalCreateSerializer):
    """
    Goal serializer
    """

    user = ProfileSerializer(read_only=True)


class GoalCommentCreateSerializer(serializers.ModelSerializer):
    """
    Comment create serializer
    """

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = GoalComment
        read_only_fields = ['id', 'created', 'updated', 'user']
        fields = '__all__'

    def validate_goal(self, value: Goal) -> Goal:
        """
        Check is goal exist and user permission
        :param value: goal
        :return: goal or validation error or permission denied
        """
        if value.status == Goal.Status.archived:
            raise ValidationError('Goal not found')

        if not BoardParticipant.objects.filter(
            board_id=value.category.board.id,
            role__in=[BoardParticipant.Role.owner, BoardParticipant.Role.writer],
            user_id=self.context['request'].user.id,
        ).exists():
            raise PermissionDenied
        return value


class GoalCommentSerializer(GoalCommentCreateSerializer):
    """
    Comment serializer
    """

    user = ProfileSerializer(read_only=True)
    goal = serializers.PrimaryKeyRelatedField(read_only=True)


class BoardCreateSerializer(serializers.ModelSerializer):
    """
    Board create serializer
    """

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Board
        read_only_fields = ('id', 'created', 'updated')
        fields = '__all__'

    def create(self, validated_data):
        """
        Create board and set user to board owner
        :param validated_data: validated data
        :return: board
        """
        user = validated_data.pop('user')
        board = Board.objects.create(**validated_data)
        board.is_deleted = False
        board.save()
        BoardParticipant.objects.create(
            user=user, board=board, role=BoardParticipant.Role.owner
        )
        return board


class BoardParticipantSerializer(serializers.ModelSerializer):
    """
    Board participant serializer
    """

    role = serializers.ChoiceField(
        required=True, choices=BoardParticipant.editable_choices
    )
    user = serializers.SlugRelatedField(
        slug_field='username', queryset=User.objects.all()
    )

    def validate_user(self, user: User) -> User:
        """
        Validate that owner can`t change him role
        :param user: user
        :return: user or validation error
        """
        if self.context['request'].user == user:
            raise ValidationError('Owner can`t change him role')
        return user

    class Meta:
        model = BoardParticipant
        fields = '__all__'
        read_only_fields = ('id', 'created', 'updated', 'board')


class BoardSerializer(serializers.ModelSerializer):
    """
    Board serializer
    """

    participants = BoardParticipantSerializer(many=True)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Board
        fields = '__all__'
        read_only_fields = ('id', 'created', 'updated')

    def update(self, instance: Board, validated_data) -> Board:
        """
        Add users to board participants
        :param instance: board
        :param validated_data: validated data
        :return: board
        """
        request = self.context['request']
        with transaction.atomic():
            BoardParticipant.objects.filter(board=instance).exclude(
                user=request.user
            ).delete()
            new_participants = []
            for participant in validated_data.get('participants', []):
                new_participants.append(
                    BoardParticipant(
                        user=participant['user'],
                        role=participant['role'],
                        board=instance,
                    )
                )
            BoardParticipant.objects.bulk_create(
                new_participants, ignore_conflicts=True
            )

            title = validated_data.get('title')
            if title:
                instance.title = title
            instance.save()
        return instance
