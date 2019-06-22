import factory
import uuid
from utils.faker import faker

from apps.users.models import BaseUser


class BaseUserFactory(factory.DjangoModelFactory):
    class Meta:
        model = BaseUser

    username = factory.Sequence(lambda n: faker.user_name())
    password = faker.password()