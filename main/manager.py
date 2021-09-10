from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        if not email:
            raise ValueError('Users must have an email address.')
        user = self.model(useername=username, email=self.normalize_email(email),)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,useername, email, password,mobile):
        if password is None:
            raise TypeError('Superusers must have password')

        user = self.create_user(username, email,password,mobile)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user