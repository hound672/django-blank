from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def __create_user(self,
                      username,
                      password=None,
                      is_staff=False,
                      is_active=False,
                      is_superuser=False):
        if not username:
            raise ValueError('Users must have an username')

        user = self.model(username=username,
                          is_staff=is_staff,
                          is_active=is_active,
                          is_superuser=is_superuser)

        if password is not None:
            user.set_password(password)
        else:
            user.set_unusable_password()

        user.save(using=self._db)

        return user

    def create_user(self, username, password):
        return self.__create_user(username,
                                  password,
                                  is_staff=False,
                                  is_active=False,
                                  is_superuser=False)

    def create_superuser(self, username, password):
        return self.__create_user(username,
                                  password,
                                  is_staff=True,
                                  is_active=True,
                                  is_superuser=True)

    def create(self, **kwargs):
        """
        Important to have this to get factories working by default
        """
        return self.create_user(**kwargs)
