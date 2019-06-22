from django.db import transaction
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from apps.users.models import BaseUser


# class _ProfileSerializer(serializers.ModelSerializer):
#     """
#     Сериализатор для модели расширения пользователя
#     """
#     avatar = serializers.FileField(source='full_image')
#
#     class Meta:
#         model = Profile
#         fields = ('full_name', 'avatar')


class _UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = BaseUser
        fields = (
            'id',
            'username',
            )


def get_user_data(*, user: BaseUser):
    user_data = _UserSerializer(instance=user).data
    # profile_data = _ProfileSerializer(instance=user.profile).data

    # return {**user_data, **profile_data}
    return user_data

@transaction.atomic
def logout(*, user: BaseUser) -> BaseUser:
    user.rotate_secret_key()

    return user

@transaction.atomic
def change_user_password(
    *,
    user: BaseUser,
    old_password: str,
    new_password: str
) -> BaseUser:

    if not user.is_active:
        raise ValidationError('User account is disabled.')

    if not user.check_password(old_password):
        raise ValidationError('Old password is invalid.')

    validate_password(new_password)
    user.set_password(new_password)
    user.rotate_secret_key()

    user.save()

    return user